from fastapi import FastAPI
from pydantic import BaseModel

from backend.auth import hash_password, verify_password
from backend.database import (
    initialize_database,
    get_connection,
)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Assistant API",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    initialize_database()


@app.get("/")
def root():
    return {
        "status": "online",
        "service": "AI Assistant API",
    }


@app.get("/api/health")
def health():
    return {
        "status": "healthy",
    }


class SignupRequest(BaseModel):
    name: str
    email: str
    password: str


@app.post("/api/auth/signup")
def signup(data: SignupRequest):
    password_hash = hash_password(data.password)

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO users (name, email, password_hash)
            VALUES (?, ?, ?)
            """,
            (
                data.name,
                data.email.lower().strip(),
                password_hash,
            ),
        )

        connection.commit()

    except Exception:
        connection.close()

        return {
            "success": False,
            "message": "An account with this email may already exist.",
        }

    connection.close()

    return {
        "success": True,
        "message": "Account created successfully.",
    }


class LoginRequest(BaseModel):
    email: str
    password: str


@app.post("/api/auth/login")
def login(data: LoginRequest):
    connection = get_connection()

    user = connection.execute(
        """
        SELECT id, name, email, password_hash
        FROM users
        WHERE email = ?
        """,
        (data.email.lower().strip(),),
    ).fetchone()

    connection.close()

    if not user:
        return {
            "success": False,
            "message": "Invalid email or password.",
        }

    if not verify_password(
        data.password,
        user["password_hash"],
    ):
        return {
            "success": False,
            "message": "Invalid email or password.",
        }

    return {
        "success": True,
        "message": "Login successful.",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
        },
    }
