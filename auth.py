from fastapi import APIRouter, Depends, HTTPException, Request
from utils.auth_tools import jwt_required
from utils.supabase_utils import supabase
from models import User
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.get("/get-user")
async def get_user(user: dict = Depends(jwt_required)):
    return { "User": user }

@router.post("/update")
async def update_user(session_data: tuple[User, tuple[str, str]] = Depends(jwt_required)):
    # TODO: This is where the user details will be updated
    print(session_data[0])
    try: 
        supabase.auth.set_session(session_data[1][0], session_data[1][1])
        supabase.auth.update_user(session_data[0])
    except Exception as e:
        raise HTTPException(status_code=401, detail=e)
    return JSONResponse(content={
        "status": "success",
        "message": "User updated",
        "user": session_data[0].__dict__
    })
