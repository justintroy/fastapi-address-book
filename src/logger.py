import logging
import json

from fastapi import Request
from fastapi.responses import JSONResponse

# Create a logger
logger = logging.getLogger("my_logger")

# Set the logging level
logger.setLevel(logging.DEBUG)

# Create a file handler and set the formatter
file_handler = logging.FileHandler("app.log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)


# What we use for logging between requests
async def logging_middleware(request: Request, call_next):
    # Log the request
    log = f"Request: {request.method} {request.url.path}"

    if request.query_params:
        log += ", Parameters: " + str(request.query_params)

    body = await request.body()
    if body:
        json_body = await request.json()
        log += ", Body: " + json.dumps(json_body)
    
    logger.info(log)

    try:
        response = await call_next(request)
    except Exception as e:
        # Log the exception
        logger.exception(f"Exception occurred: {str(e)}")

    return response
