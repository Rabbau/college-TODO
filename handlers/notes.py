from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi import status

from dependecy import get_note_service, get_request_user_id, get_task_service
from schema import NoteResponseSchema, NoteUpdateSchema, TaskStatusUpdateSchema
from service import NoteService, TaskService

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/{task_id}", response_model=NoteResponseSchema)
async def get_note(
    task_id: int,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    note_service: Annotated[NoteService, Depends(get_note_service)],
    user_id: int = Depends(get_request_user_id),
):
    task = task_service.get_task(task_id=task_id, user_id=user_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")
    return NoteResponseSchema(
        content=note_service.read(task_id),
        due=task.due,
        done=task.done,
        favorite=task.favorite,
        # made by kirill
        importance=task.importance,
        # made by kirill
    )


@router.put("/{task_id}", response_model=NoteResponseSchema)
async def update_note(
    task_id: int,
    body: NoteUpdateSchema,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    note_service: Annotated[NoteService, Depends(get_note_service)],
    user_id: int = Depends(get_request_user_id),
):
    task = task_service.get_task(task_id=task_id, user_id=user_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

    note_service.write(task_id, body.content or '')

    state_payload = TaskStatusUpdateSchema(
        due=body.due,
        done=body.done,
        favorite=body.favorite,
        # made by kirill
        importance=body.importance,
        # made by kirill
    )
    updated_task = task_service.update_task_state(task_id=task_id, user_id=user_id, payload=state_payload)

    return NoteResponseSchema(
        content=body.content or '',
        due=updated_task.due,
        done=updated_task.done,
        favorite=updated_task.favorite,
        # made by kirill
        importance=updated_task.importance,
        # made by kirill
    )
