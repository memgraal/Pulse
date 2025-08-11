from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from .schemas import UserLoginCredentialsSchema, UserRegistrationCredentialsSchema
from .config import security
from .dependences import SessionDep
from database import UsersModel
from .service import verify_password, hash_password


AuthRouter = APIRouter(
    prefix="/auth",
    tags=['Athentication'],
)


@AuthRouter.post("/login")
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
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    
    
@AuthRouter.post("/register")
async def register(userCreds: UserRegistrationCredentialsSchema, session: SessionDep) -> dict:
    result = await session.execute(
        select(UsersModel).where(
            UsersModel.email == userCreds.email
        )
    )
    user = result.scalars().first()
    
    if not user:
        session.add(
            new_user := UsersModel(
                name=userCreds.username,
                email=userCreds.email,
                password=hash_password(userCreds.password),
                )
        )
        await session.commit()
        
        token = security.create_access_token(uid=str(new_user.id), username=new_user.name)
        return {"access_token": token}
    
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists")