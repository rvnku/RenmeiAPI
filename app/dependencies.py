from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from app.env import Env


api_key_header = APIKeyHeader(name='X-Auth-Key', auto_error=False)


async def validate_api_key(api_key: str = Security(api_key_header)):
    if not api_key or api_key != Env.api_key:
        raise HTTPException(403, 'Invalid or missing X-Auth-Key header')
    return api_key
