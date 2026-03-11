from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends

from dependecy import get_request_user_id, get_task_service
from exception import TaskNotFound
from schema import Task, TaskCreateSchema, TaskStatusUpdateSchema
from service import TaskService

router = APIRouter(prefix="/task", tags=["task"])


@router.get(
    path="/all",
    response_model=list[Task]
)
async def get_task(
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id)
):
    return task_service.get_tasks(user_id=user_id)


@router.get("/{task_id}", response_model=Task)
async def get_single_task(
    task_id: int,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id)
):
    task = task_service.get_task(task_id=task_id, user_id=user_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")
    return task


@router.post(
    "/",
    response_model=Task
)
async def create_task(
    body: TaskCreateSchema,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id)
):
    return task_service.create_task(body, user_id)


@router.patch(
    "/{task_id}",
    response_model=Task
)
async def patch_task(
    task_id: int,
    name: str,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id)
):
    try:
        return task_service.update_task_name(task_id=task_id, name=name, user_id=user_id)
    except TaskNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)


@router.patch(
    "/{task_id}/status",
    response_model=Task
)
async def patch_task_status(
    task_id: int,
    body: TaskStatusUpdateSchema,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id)
):
    try:
        return task_service.update_task_state(task_id=task_id, user_id=user_id, payload=body)
    except TaskNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_task(
    task_id:int,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id)
):
    try:
        task_service.delete_task(task_id=task_id, user_id=user_id)
    except TaskNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
