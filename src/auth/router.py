from fastapi import APIRouter, HTTPException, status, Response
from sqlalchemy import select

from .schemas import UserLoginCredentialsSchema, UserRegistrationCredentialsSchema
from .config import security, config
from .dependences import SessionDep
from database import UsersModel
from .service import verify_password, hash_password


AuthRouter = APIRouter(
    prefix="/auth",
    tags=["Athentication"],
)


@AuthRouter.post("/login")
async def loggining(
    userCreds: UserLoginCredentialsSchema, session: SessionDep, responce: Response
) -> dict:
    result = await session.execute(
        select(UsersModel).where(UsersModel.email == userCreds.email)
    )
    user = result.scalars().first()

    if user and verify_password(userCreds.password, user.password):

        responce.set_cookie(
            config.JWT_ACCESS_COOKIE_NAME,
            token := security.create_access_token(uid=str(user.id)),
            secure=True,
        )

        return {"access_token": token}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials"
    )


@AuthRouter.post("/register")
async def register(
    userCreds: UserRegistrationCredentialsSchema, session: SessionDep
) -> dict:
    result = await session.execute(
        select(UsersModel).where(UsersModel.email == userCreds.email)
    )
    user = result.scalars().first()

    if not user:
        session.add(
            new_user := UsersModel(
                user_name=userCreds.username,
                display_name=userCreds.display_name,
                email=userCreds.email,
                password=hash_password(userCreds.password),
            )
        )
        await session.commit()

        token = security.create_access_token(uid=str(new_user.id))
        return {"access_token": token}

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="User with this email already exists",
    )
