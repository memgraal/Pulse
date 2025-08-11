from fastapi import APIRouter, Depends, HTTPException, status
from auth.config import security


UserRouter =APIRouter(
    prefix="/user",
    tags=['UserProfile'],   
)


@UserRouter.get("/profile", dependencies=[Depends(security.get_token_from_request)])
async def get_user_profile(token: str = Depends()) -> dict:
    try:
        security.verify_token(token) # - тяжелый случай, нужно сделать условие, а не подный обвал роута 
        return {"message": "User profile data"} # временный пример (сделать после слияния ветки feaature-database и user-registration)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    