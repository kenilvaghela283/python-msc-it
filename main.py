
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session

import jwt
from datetime import datetime, timedelta, timezone


# =====================================================
# FASTAPI APP
# =====================================================

app = FastAPI(title="JWT Authentication + SQLite ORM")


# =====================================================
# DATABASE CONFIGURATION
# =====================================================

DATABASE_URL = "sqlite:///./users.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# =====================================================
# USER TABLE
# =====================================================

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(
        String(100),
        unique=True,
        nullable=False
    )

    password = Column(
        String(200),
        nullable=False
    )

    full_name = Column(
        String(200),
        nullable=False
    )


# Create database table
Base.metadata.create_all(bind=engine)


# =====================================================
# DATABASE SESSION
# =====================================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# =====================================================
# JWT SETTINGS
# =====================================================

SECRET_KEY = "mysecretkey123"

ALGORITHM = "HS256"

TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


# =====================================================
# HTML TEMPLATE
# =====================================================

templates = Jinja2Templates(
    directory="templates"
)


# =====================================================
# PYDANTIC MODELS
# =====================================================

class UserSignup(BaseModel):

    username: str
    password: str
    full_name: str


class UserLogin(BaseModel):

    username: str
    password: str


# =====================================================
# HOME PAGE
# =====================================================

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# =====================================================
# SIGNUP
# =====================================================

@app.post("/signup")
def signup(
    user: UserSignup,
    db: Session = Depends(get_db)
):

    # Check existing username
    existing_user = (
        db.query(User)
        .filter(User.username == user.username)
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )


    # Create new user
    new_user = User(

        username=user.username,

        password=user.password,

        full_name=user.full_name
    )


    # Add to database
    db.add(new_user)

    db.commit()

    db.refresh(new_user)


    return {

        "message": "User created successfully",

        "user": {

            "id": new_user.id,

            "username": new_user.username,

            "full_name": new_user.full_name
        }
    }


# =====================================================
# LOGIN
# =====================================================

@app.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    # Find user from database
    db_user = (
        db.query(User)
        .filter(User.username == user.username)
        .first()
    )


    if db_user is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )


    # Check password
    if user.password != db_user.password:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )


    # Token expiration
    expire_time = (
        datetime.now(timezone.utc)
        + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    )


    # JWT payload
    payload = {

        "sub": db_user.username,

        "name": db_user.full_name,

        "exp": expire_time
    }


    # Create JWT token
    token = jwt.encode(

        payload,

        SECRET_KEY,

        algorithm=ALGORITHM
    )


    return {

        "message": "Login successful",

        "access_token": token,

        "token_type": "bearer"
    }


# =====================================================
# GET CURRENT USER
# =====================================================

def get_current_user(

    token: str = Depends(oauth2_scheme),

    db: Session = Depends(get_db)

):

    try:

        # Decode JWT
        payload = jwt.decode(

            token,

            SECRET_KEY,

            algorithms=[ALGORITHM]
        )


        username = payload.get("sub")


        if username is None:

            raise HTTPException(

                status_code=401,

                detail="Invalid token"
            )


        # Find user in database
        user = (

            db.query(User)

            .filter(User.username == username)

            .first()
        )


        if user is None:

            raise HTTPException(

                status_code=401,

                detail="User not found"
            )


        return user


    except jwt.ExpiredSignatureError:

        raise HTTPException(

            status_code=401,

            detail="Token has expired"
        )


    except jwt.InvalidTokenError:

        raise HTTPException(

            status_code=401,

            detail="Invalid token"
        )


# =====================================================
# PROFILE
# =====================================================

@app.get("/profile")
def profile(

    current_user: User = Depends(
        get_current_user
    )

):

    return {

        "message": "Authentication successful!",

        "id": current_user.id,

        "username": current_user.username,

        "full_name": current_user.full_name
    }


# =====================================================
# GET ALL USERS
# =====================================================

@app.get("/users")
def get_users(

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)

):

    users = db.query(User).all()


    user_list = []


    for user in users:

        user_list.append({

            "id": user.id,

            "username": user.username,

            "full_name": user.full_name
        })


    return {

        "total_users": len(user_list),

        "users": user_list
    }


# =====================================================
# LOGOUT
# =====================================================

@app.post("/logout")
def logout(

    current_user: User = Depends(
        get_current_user
    )

):

    return {

        "message": "Logout successful",

        "username": current_user.username
    }


# =====================================================
# RUN APPLICATION
# =====================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(

        "main:app",

        host="127.0.0.1",

        port=8000,

        reload=True
    )
