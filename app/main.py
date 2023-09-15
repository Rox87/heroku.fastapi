from fastapi import FastAPI 
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import socket
app = FastAPI()

hostname = socket.gethostname()

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["*"] 
)


@app.get("/") 
async def main():
    return {"message": f"{hostname}"}