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