from fastapi import APIRouter, HTTPException, status


DeskRouter = APIRouter(prefix="/Desk", tags=["Desk Tasks"])


@DeskRouter.get("/")
async def desk_home() -> dict:

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized access to Desk tasks",
    )

    return {"message": "Show desk with frontend tasks"}
