from fastapi import Request

async def logging_middleware(request: Request, call_next):

    print(f"for debugging, printing the type of the request object: {type(request)}")
    print()
    print(f"the method is: {request.method}, and the path is: {request.url.path}")
    
    if request.url.path == "/health":
        return await call_next(request)

    response = await call_next(request)

    print(f"for debugging, printing the type of the Response object: {type(response)}")
    print(f"the status code is: {response.status_code}")

    return response


    
