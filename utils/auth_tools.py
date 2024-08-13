from typing import Annotated, Callable
from fastapi import Cookie, HTTPException, Request
import os, requests, jwt
from models import User

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_ANON = os.environ.get("SUPABASE_ANON")


async def jwt_required(request: Request):
    access_token = request.cookies.get('access_token') if request.cookies.get('access_token') else request.headers.get('access_token').split(" ")[1] if request.headers.get('access_token') else None
    refresh_token = request.cookies.get('refresh_token') if request.cookies.get('refresh_token') else request.headers.get('refresh_token') if request.headers.get('refresh_token') else None
    if access_token is None:
        raise HTTPException(status_code=401, detail="Access token is required")
    try:
        payload = verify_token(access_token)
        return User(**payload), ( access_token, refresh_token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


def verify_token(token: str):
    try:
        headers = {
            "Authorization": f'Bearer {token}',
            "apikey": f'{SUPABASE_ANON}'
        }
        response = requests.request("GET", f"{SUPABASE_URL}/auth/v1/user", headers = headers).json()
        if response.get('code'):
            raise HTTPException(status_code=response.get('code'), detail=response.get("msg"))
        return response
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Session has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


