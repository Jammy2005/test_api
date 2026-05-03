# for AWS
import boto3, json, os

def get_api_key():
    # locally: use .env file as normal
    if os.path.exists('.env'):
        from dotenv import load_dotenv
        load_dotenv()
        return os.getenv('ANTHROPIC_API_KEY')

    # on EC2/Lambda: fetch from Secrets Manager
    client = boto3.client('secretsmanager', region_name='us-east-1')
    secret = client.get_secret_value(SecretId='prod/anthropic-api-key')
    data = json.loads(secret['SecretString'])
    return data['ANTHROPIC_API_KEY']

api_key = get_api_key()

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from middleware.logging import logging_middleware
from middleware.throttling import rate_limit
from routes.inference import router as inference_router

app = FastAPI()

# add middleware 
app.middleware("http")(logging_middleware) # what the (@) wrapper actually does
app.middleware("http")(rate_limit) 

# global error handling
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"unhandled error : {exc}")
    return JSONResponse(
        status_code=500,
        content={"details" : "Internal server error, being actively reviewed"}
        )

# add router
app.include_router(inference_router)

@app.get("/")
async def root():
    return {"message": "hello world"}

@app.get("/health")
async def health():
    return {"status": "ok"}