from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from .. import app
from ..schemas import TaskScheme, TaskPut, TaskDelete
from ..db import tasks_db, Task


@app.post("/create_task", response_model=TaskScheme)
async def create_task(
    data: TaskScheme, session: Annotated[Session, Depends(tasks_db.get_session)]
):
    task = Task(**data.model_dump())
    session.add(task)
    return task


@app.get("/task/{id}", response_model=TaskScheme)
async def get_task(id: int, session: Annotated[Session, Depends(tasks_db.get_session)]):
    task = session.scalar(select(Task).where(Task.id == id))
    if not task:
        raise HTTPException(404, detail="Task not found")
    return task


@app.get("/tasks")
async def get_all_tasks(session: Annotated[Session, Depends(tasks_db.get_session)]):
    tasks = session.scalars(select(Task)).all()
    tasks = [task for task in tasks]
    return tasks


@app.put("/task/{id}")
async def edit_task(
    id: int, data: TaskPut, session: Annotated[Session, Depends(tasks_db.get_session)]
):
    task = session.scalar(select(Task).where(Task.id == id))
    if not task:
        raise HTTPException(404, detail="Task not found")
    if task.author != data.author:
        raise HTTPException(403, detail="Permission denied")
    task_data = data.model_dump(exclude_unset=True)
    upd = update(Task).where(Task.id == id).values(**task_data)
    session.execute(upd)
    return task_data


@app.delete("/task/{id}")
async def delete_task(
    id: int,
    data: TaskDelete,
    session: Annotated[Session, Depends(tasks_db.get_session)],
):
    task = session.scalar(select(Task).where(Task.id == id))
    if not task:
        raise HTTPException(404, detail="Task not found")
    if task.author != data.user:
        raise HTTPException(403, detail="Permission denied")
    session.delete(task)
    return task
