from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session

from models import Tasks, Categories
from schema.task import TaskCreateSchema
from settings import Settings


class TaskRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_tasks(self, user_id: int):
        with self.db_session() as session:
            query = select(Tasks).where(Tasks.user_id == user_id)
            tasks: list[Tasks] = session.execute(query).scalars().all()
        return tasks
    
    def get_task(self, task_id: int) -> Tasks | None:
        with self.db_session() as session:
            task: Tasks = session.execute(select(Tasks).where(Tasks.id == task_id)).scalar_one_or_none()
        return task

    def get_user_task(self, task_id: int, user_id: int) -> Tasks | None:
        query = select(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id)
        with self.db_session() as session:
            return session.execute(query).scalar_one_or_none()
    
    def ensure_default_category(self) -> int:
        with self.db_session() as session:
            category = session.execute(select(Categories)).scalars().first()
            if category:
                return category.id
            settings = Settings()
            default = Categories(name=settings.DEFAULT_CATEGORY_NAME, type=settings.DEFAULT_CATEGORY_TYPE)
            session.add(default)
            session.commit()
            session.refresh(default)
            return default.id
    
    def create_task(self, task: TaskCreateSchema, user_id: int, category_id: int) -> int:
        task_model = Tasks(
            name=task.name,
            pomodoro=task.pomodoro or 1,
            category_id=category_id,
            user_id=user_id,
            due=task.due,
            done=False,
            favorite=False,
            # made by kirill
            importance=task.importance or "нейтрально",
            # made by kirill
        )
        with self.db_session() as session:
            session.add(task_model)
            session.commit()
            return task_model.id

    def update_task_name(self, task_id: int, name: str) -> Tasks:
        query = update(Tasks).where(Tasks.id == task_id).values(name=name).returning(Tasks.id)
        with self.db_session() as session:
            task_id: int = session.execute(query).scalar_one_or_none()
            session.commit()
            session.flush()
            return self.get_task(task_id)
    
    def update_task_state(self, task_id: int, **values) -> Tasks:
        if not values:
            return self.get_task(task_id)
        query = update(Tasks).where(Tasks.id == task_id).values(**values)
        with self.db_session() as session:
            session.execute(query)
            session.commit()
        return self.get_task(task_id)
    
    def delete_task(self, task_id: int, user_id: int) -> None:
        query = delete(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id)
        with self.db_session() as session:
            session.execute(query)
            session.commit()

    def get_task_by_category_name(self, category_name: str) -> list[Tasks]:
        query = select(Tasks).join(Categories, Tasks.category_id == Categories.id).where(Categories.name == category_name)
        with self.db_session() as session:
            task: list[Tasks] = session.execute(query).scalars().all()
            return task
