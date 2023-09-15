# Importando as bibliotecas necessárias

from fastapi import Depends,FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import logging
import uvicorn

# Inicializando o app
app = FastAPI()

# Autenticação
security = HTTPBasic()

# Configurações do CORS
origins = [
    "https://example.com",
    "https://google.com"
]

# Configurando o CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração de log
logging.basicConfig(filename='api.log', level=logging.INFO)

# Sanitize function
def sanitize(data: str) -> str:
    # Evita injeção de script
    data = data.replace("<script>", "")
    data = data.replace("</script>", "")
    return data

# Limite de request por cliente
MAX_REQUESTS = 1000
clients = {}

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    client_addr = request.client.host
    if client_addr not in clients:
        clients[client_addr] = 0
    if clients[client_addr] >= MAX_REQUESTS:
        raise HTTPException(429, "Too Many Requests")
    clients[client_addr] += 1
    response = await call_next(request)
    return response

# Rota raiz
@app.get("/")
async def root():
    return {"message": "API está rodando!"}

# Rota de exemplo
@app.post("/exemplo")
async def exemplo(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    # Validação de autenticação
    if credentials.username != "user" or credentials.password != "password":
        raise HTTPException(400, detail="Credenciais inválidas")
    # Validação e sanitização dos dados recebidos
    data = await request.json()
    if "name" not in data or not data["name"]:
        raise HTTPException(400, detail="Campo 'name' é obrigatório")
    name = sanitize(data["name"])
    logging.info(f"{credentials.username} executou a rota 'exemplo' com o nome {name}")
    return JSONResponse(content={"mensagem": "Olá, " + name + "!"})

if __name__ == "__main__":
        import subprocess
        #subprocess.Popen(['python', '-m', 'https_redirect'])  # Add this
        uvicorn.run(
           'main:app' 
           #port=443, 
           #host='127.0.0.1',
           #reload=True,
           #ssl_keyfile='/etc/letsencrypt/live/flyson.com.br/privkey.pem',
           #ssl_certfile='/etc/letsencrypt/live/flyson.com.br/fullchain.pem'
           )