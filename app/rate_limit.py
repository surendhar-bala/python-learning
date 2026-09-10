from fastapi import Request, HTTPException
from .redis import redis_client

RATE_LIMIT = 2
WINDOW = 60


def rate_limit(request: Request):

    client_ip = request.client.host

    key = f"rate_limit:{client_ip}"

    count = redis_client.incr(key)

    if count == 1:
        redis_client.expire(key, WINDOW)

    if count > RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Too many requests"
        )