from typing import Annotated
from urllib.parse import quote

from fastapi import APIRouter, Depends, HTTPException, status
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
    "/login/google",
    name="auth.google_login"
)
# made by lesha
async def google_login(
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    redirect_url = auth_service.get_google_redirect_url()
    print(redirect_url)
    return RedirectResponse(redirect_url)
# made by lesha


@router.get(
    path="/google",
    name="auth.google_auth"
)
# made by lesha
async def google_auth(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    code: str
):
    try:
        login_data, profile = auth_service.google_auth(code=code)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie("access_token", login_data.access_token, httponly=True, samesite="lax")
    user_label = profile.get("name") or profile.get("email") or ""
    response.set_cookie("user_name", quote(user_label), httponly=False, samesite="lax")
    return response
# made by lesha
