from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from dependecy import get_auth_service
from exception import UserNotCorrectPasswordExpcection, UserNotFoundExpcection
from schema.user import UserCreateSchema, UserLoginSchema
from service.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
    "/login", 
    response_model=UserLoginSchema
)
async def login(
    body: UserCreateSchema,
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    try:
        user_login_data = auth_service.login(body.username, body.password)
    except UserNotFoundExpcection as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )
    except UserNotCorrectPasswordExpcection as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )
    return user_login_data

@router.get(
    "/login/google"
)
async def google_login(
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    redirect_url = auth_service.get_google_redirect_url()
    print(redirect_url)
    return RedirectResponse(redirect_url)


@router.get(
    path="/google"
)
async def google_auth(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    code: str
):
    return auth_service.google_auth(code=code)
