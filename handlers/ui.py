from typing import Annotated
from datetime import datetime

from typing import Annotated
from urllib.parse import unquote

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from dependecy import get_note_service, get_request_user_id, get_task_service
from service import TaskService, NoteService

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def _format_due(due: datetime | None) -> str:
    if not due:
        return ''
    return due.strftime('%Y-%m-%dT%H:%M')


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    token = request.cookies.get("access_token")
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "access_token": token,
            "authenticated": bool(token),
        "user_name": unquote(request.cookies.get("user_name", "")),
        },
    )


@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    response.delete_cookie("user_name")
    return response


@router.get("/notes/{task_id}", response_class=HTMLResponse)
async def note_page(
    request: Request,
    task_id: int,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    note_service: Annotated[NoteService, Depends(get_note_service)],
    user_id: int = Depends(get_request_user_id),
):
    task = task_service.get_task(task_id=task_id, user_id=user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    note_text = note_service.read(task_id)
    token = request.cookies.get("access_token")

    return templates.TemplateResponse(
        "note.html",
        {
            "request": request,
            "task_id": task.id,
            "task_name": task.name,
            "note_text": note_text,
            "access_token": token,
            "due_value": _format_due(task.due),
            "done": task.done,
            "favorite": task.favorite,
            "importance": task.importance,
        },
    )


