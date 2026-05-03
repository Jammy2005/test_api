import time
from fastapi import Request
from fastapi.responses import JSONResponse

user_requests = {}
RATE_LIMIT = 3       # max 3 requests
TIME_WINDOW = 60     # in a timeframe of 60 seconds

async def rate_limit(request: Request, call_next):

    user_id = request.client.host # assosiate users with their IP becuase we dont have a specific api keys as of know
    current_time = time.time()

    # updating our time array
    if user_id in user_requests: 
        times_array = user_requests[user_id]
        t = current_time - TIME_WINDOW
        for recorded_time in times_array[:]: # loop over shallow copy of list, it is dangerous to loop over a list while you are modifying it, this is a classical solution to that problem
            if recorded_time > t:
                continue
            else:
                times_array.remove(recorded_time)
          
    else: 
        # create it as a key and add an empty arr 
        user_requests[user_id] = []
    

    # checking if we can accept or not
    times_array = user_requests[user_id]
    if len(times_array) >= RATE_LIMIT:
        return JSONResponse(
            status_code = 429,
            content = {"detail": "Too many requests, slow down"}
        )
    else: 
        # accept (add to array) 
        times_array.append(current_time)
        return await call_next(request)

                
    
