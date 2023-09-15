from fastapi import FastAPI 
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["177.181.7.139"] 
)


@app.get("/") 
async def main():
    return {"message": "Hello World"}