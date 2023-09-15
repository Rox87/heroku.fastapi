from fastapi import FastAPI 
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["127.0.0.1"] 
)


@app.get("/") 
async def main():
    return {"message": "Hello World"}