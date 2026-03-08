from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from dependecy import get_user_service
from schema import UserLoginSchema, UserCreateSchema
from exception import UserAlreadyExistsException
from service import UserService

router = APIRouter(prefix="/user", tags=["user"])

@router.post("", response_model=UserLoginSchema)
async def create_user(body: UserCreateSchema, user_service: Annotated[UserService, Depends(get_user_service)]):
    try:
        return user_service.create_user(body.username, body.password)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.detail)
