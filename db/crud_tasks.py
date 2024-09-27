from sqlalchemy.orm import Session
from models import Task, User, TaskStatus

def create_task(db: Session, name: str, description: str, status: TaskStatus, priority):
    new_task = Task(name=name, description=description, status=status, priority=priority)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_task_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def add_executor_to_task(db: Session, task_id: int, user_id: int):
    task = get_task_by_id(db, task_id)
    user = db.query(User).filter(User.id == user_id).first()
    if task and user:
        task.executors.append(user)
        db.commit()
        db.refresh(task)
        return task
    return None

def change_task_status(db: Session, task_id: int, new_status: TaskStatus):
    task = get_task_by_id(db, task_id)
    if task:
        task.status = new_status
        db.commit()
        db.refresh(task)
        return task
    return None

def append_to_task_description(db: Session, task_id: int, additional_text: str):
    task = get_task_by_id(db, task_id)
    if task:
        task.description += f"\n{additional_text}"
        db.commit()
        db.refresh(task)
        return task
    return None

def delete_task(db: Session, task_id: int):
    task = get_task_by_id(db, task_id)
    if task:
        db.delete(task)
        db.commit()
        return True
    return False
