from fastapi import FastAPI, Request
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import socket
app = FastAPI()

hostname = socket.gethostname()

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["*"] 
)


@app.get("/") 
async def main(request: Request):
    client_host = request.client.host
    return {"client_host": client_host}