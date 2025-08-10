from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from .schemas import UserLoginCredentialsSchema, UserRegistrationCredentialsSchema
from config import security
from dependences import SessionDep
from database import UsersModel
from service import verify_password, hash_password


router = APIRouter(
    prefix="/auth",
    tags=['Athentication'],
)


@router.post("/login")
async def loggining(userCreds: UserLoginCredentialsSchema, session: SessionDep) -> dict:
    result = await session.execute(
        select(UsersModel).where(
            UsersModel.email == userCreds.email
        )
    )
    user = result.scalars().first()
    
    if user and verify_password(userCreds.password, user.password):
        token = security.create_access_token(uid=user.id, username=user.name)
        return {"access_token": token}
    
    raise HTTPException(status_code=401, detail="Incorrect credentials")
    
    
@router.post("/register")
async def register(userCreds: UserRegistrationCredentialsSchema, session: SessionDep) -> dict:
    result = await session.execute(
        select(UsersModel).where(
            UsersModel.email == userCreds.email
        )
    )
    
    if not result.first():
        ...