from dataclasses import dataclass

from exception import TaskNotFound
from repository import TaskRepository
from schema import Task, TaskCreateSchema, TaskStatusUpdateSchema

from service.note import NoteService


@dataclass
class TaskService:
    task_repository: TaskRepository
    note_service: NoteService

    def get_tasks(self, user_id: int) -> list[Task]:
        tasks = self.task_repository.get_tasks(user_id=user_id)
        return [self._map_task(task) for task in tasks]

    def create_task(self, body: TaskCreateSchema, user_id: int) -> Task:
        category_id = body.category_id or self.task_repository.ensure_default_category()
        task_id = self.task_repository.create_task(body, user_id, category_id)
        task = self.task_repository.get_task(task_id)
        return self._map_task(task)

    def update_task_name(self, task_id: int, name: str, user_id: int) -> Task:
        task = self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFound
        updated = self.task_repository.update_task_name(task_id=task_id, name=name)
        return self._map_task(updated)

    def update_task_state(self, task_id: int, user_id: int, payload: TaskStatusUpdateSchema) -> Task:
        task = self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFound
        updates = payload.model_dump(exclude_none=True)
        updated = self.task_repository.update_task_state(task_id=task_id, **updates)
        return self._map_task(updated)

    def delete_task(self, task_id: int, user_id: int) -> None:
        task = self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFound
        self.task_repository.delete_task(task_id=task_id, user_id=user_id)

    def get_task(self, task_id: int, user_id: int) -> Task | None:
        task = self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            return None
        return self._map_task(task)

    def _map_task(self, task) -> Task:
        preview = self.note_service.preview(self.note_service.read(task.id))
        return Task(
            id=task.id,
            name=task.name,
            pomodoro=task.pomodoro,
            category_id=task.category_id,
            user_id=task.user_id,
            due=task.due,
            done=task.done,
            favorite=task.favorite,
            # made by kirill
            importance=task.importance,
            # made by kirill
            notes_preview=preview,
        )
