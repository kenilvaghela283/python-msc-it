
import os
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
)
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from starlette.middleware.sessions import SessionMiddleware


# --------------------------------------------------
# Database configuration
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'tasks.db'}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(String(300), default="")
    priority = Column(String(20), default="Medium", nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)
    created_by = Column(String(100), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tasks.db and the tasks table automatically.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Personal Task Tracker",
    lifespan=lifespan,
)

# Set SESSION_SECRET in your environment for deployment.
# The fallback is convenient for local development only.
app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ.get(
        "SESSION_SECRET",
        "local-development-secret-change-me",
    ),
    same_site="lax",
    https_only=os.environ.get("COOKIE_SECURE", "false").lower()
    == "true",
)

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


# --------------------------------------------------
# Database dependency
# --------------------------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------------------------------------------
# Authentication helper
# --------------------------------------------------

def get_current_user(request: Request) -> str:
    username = request.session.get("username")

    if not username:
        raise HTTPException(
            status_code=303,
            headers={"Location": "/login"},
        )

    return username


# --------------------------------------------------
# Login and logout
# --------------------------------------------------

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={},
    )


@app.post("/login")
def login(
    request: Request,
    username: Annotated[str, Form()],
):
    username = username.strip()

    if not username or len(username) > 100:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "Enter a name of 1–100 characters."},
            status_code=400,
        )

    # Replace any previous session data.
    request.session.clear()
    request.session["username"] = username

    return RedirectResponse("/", status_code=303)


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=303)


# --------------------------------------------------
# Home page: show only the current user's tasks
# --------------------------------------------------

@app.get("/")
def home(
    request: Request,
    db: Session = Depends(get_db),
):
    username = request.session.get("username")

    if not username:
        return RedirectResponse("/login", status_code=303)

    tasks = (
        db.query(Task)
        .filter(Task.created_by == username)
        .order_by(Task.created_at.desc(), Task.id.desc())
        .all()
    )

    pending_tasks = [task for task in tasks if not task.is_completed]
    completed_tasks = [task for task in tasks if task.is_completed]

    theme = request.cookies.get("theme", "light")
    if theme not in ("light", "dark"):
        theme = "light"

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "username": username,
            "pending_tasks": pending_tasks,
            "completed_tasks": completed_tasks,
            "theme": theme,
        },
    )


# --------------------------------------------------
# Add a task
# --------------------------------------------------

@app.post("/add")
def add_task(
    request: Request,
    title: Annotated[str, Form()],
    description: Annotated[str, Form()] = "",
    priority: Annotated[str, Form()] = "Medium",
    db: Session = Depends(get_db),
):
    username = get_current_user(request)

    title = title.strip()
    description = description.strip()

    if not title or len(title) > 150:
        raise HTTPException(
            status_code=400,
            detail="Title must contain 1–150 characters.",
        )

    if len(description) > 300:
        raise HTTPException(
            status_code=400,
            detail="Description must not exceed 300 characters.",
        )

    if priority not in ("High", "Medium", "Low"):
        raise HTTPException(
            status_code=400,
            detail="Invalid priority.",
        )

    task = Task(
        title=title,
        description=description,
        priority=priority,
        is_completed=False,
        created_by=username,
        created_at=datetime.now(),
    )

    db.add(task)
    db.commit()

    return RedirectResponse("/", status_code=303)


# --------------------------------------------------
# Toggle pending/completed
# --------------------------------------------------

@app.get("/toggle/{id}")
def toggle_task(
    id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    username = get_current_user(request)

    task = (
        db.query(Task)
        .filter(Task.id == id, Task.created_by == username)
        .first()
    )

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found.")

    task.is_completed = not task.is_completed
    db.commit()

    return RedirectResponse("/", status_code=303)


# --------------------------------------------------
# Edit task form
# --------------------------------------------------

@app.get("/edit/{id}")
def edit_task(
    id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    username = get_current_user(request)

    task = (
        db.query(Task)
        .filter(Task.id == id, Task.created_by == username)
        .first()
    )

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found.")

    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={"task": task, "theme": request.cookies.get("theme", "light")},
    )


# --------------------------------------------------
# Update task
# --------------------------------------------------

@app.post("/update/{id}")
def update_task(
    id: int,
    request: Request,
    title: Annotated[str, Form()],
    description: Annotated[str, Form()] = "",
    priority: Annotated[str, Form()] = "Medium",
    db: Session = Depends(get_db),
):
    username = get_current_user(request)

    task = (
        db.query(Task)
        .filter(Task.id == id, Task.created_by == username)
        .first()
    )

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found.")

    title = title.strip()
    description = description.strip()

    if not title or len(title) > 150:
        raise HTTPException(status_code=400, detail="Invalid title.")

    if len(description) > 300:
        raise HTTPException(status_code=400, detail="Description too long.")

    if priority not in ("High", "Medium", "Low"):
        raise HTTPException(status_code=400, detail="Invalid priority.")

    task.title = title
    task.description = description
    task.priority = priority

    db.commit()

    return RedirectResponse("/", status_code=303)


# --------------------------------------------------
# Delete task
# --------------------------------------------------

@app.post("/delete/{id}")
def delete_task(
    id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    username = get_current_user(request)

    task = (
        db.query(Task)
        .filter(Task.id == id, Task.created_by == username)
        .first()
    )

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found.")

    db.delete(task)
    db.commit()

    return RedirectResponse("/", status_code=303)


# --------------------------------------------------
# Theme cookie
# --------------------------------------------------

@app.get("/set-theme/{theme}")
def set_theme(request: Request, theme: str):
    get_current_user(request)

    if theme not in ("light", "dark"):
        raise HTTPException(status_code=400, detail="Invalid theme.")

    response = RedirectResponse("/", status_code=303)
    response.set_cookie(
        key="theme",
        value=theme,
        max_age=60 * 60 * 24 * 365,
        httponly=True,
        samesite="lax",
        secure=os.environ.get("COOKIE_SECURE", "false").lower() == "true",
    )

    return response
