from fastapi import FastAPI, Response, Request
from pydantic import BaseModel

from backend.auth import hash_password, verify_password
from backend.database import (
    initialize_database,
    get_connection,
)

from fastapi.middleware.cors import CORSMiddleware 

import secrets
from datetime import datetime, timedelta, timezone


app = FastAPI(
    title="AI Assistant API",
    version="0.1.0",
)
SESSION_COOKIE_NAME = "session"
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
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
    remember: bool = False
class PlanRequest(BaseModel):
    plan: str


@app.post("/api/auth/login")
def login(data: LoginRequest, response: Response):
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

    session_token = create_session(user["id"])

    # store the session token in an HttpOnly cookie
    response.set_cookie(
        key="session",
        value=session_token,
        httponly=True,
        samesite="lax",
        secure=False, # True when using HTTPS in production
        max_age=60 * 60 *24 * 30 if data.remember else None,
    )

    return {
        "success": True,
        "message": "Login successful.",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
        },
    }


@app.get("/api/auth/me")
def get_current_user(
    request: Request,
    response: Response,
):
    session_token = request.cookies.get(SESSION_COOKIE_NAME)

    if not session_token:
        return {
            "success": False,
            "message": "Not authenticated.",
        }

    connection = get_connection()

    session = connection.execute(
        """
        SELECT user_id, expires_at
        FROM sessions
        WHERE session_token = ?
        """,
        (session_token,),
    ).fetchone()

    if not session:
        connection.close()

        response.delete_cookie(
            key=SESSION_COOKIE_NAME,
            httponly=True,
            samesite="lax",
        )

        return {
            "success": False,
            "message": "Invalid session.",
        }

    expires_at = datetime.fromisoformat(session["expires_at"])

    if expires_at <= datetime.now(timezone.utc):

        connection.execute(
            """
            DELETE FROM sessions
            WHERE session_token = ?
            """,
            (session_token,),
        )

        connection.commit()
        connection.close()

        response.delete_cookie(
            key=SESSION_COOKIE_NAME,
            httponly=True,
            samesite="lax",
        )

        return {
            "success": False,
            "message": "Session expired.",
        }

    user = connection.execute(
        """
        SELECT id, name, email, plan
        FROM users
        WHERE id = ?
        """,
        (session["user_id"],),
    ).fetchone()

    connection.close()

    if not user:
        response.delete_cookie(
            key=SESSION_COOKIE_NAME,
            httponly=True,
            samesite="lax",
        )

        return {
            "success": False,
            "message": "User not found.",
        }

    return {
        "success": True,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "plan": user["plan"],
        },
    }


@app.post("/api/auth/plan")
def select_plan(
    data: PlanRequest,
    request: Request,
):
    allowed_plans = {
        "free",
        "pro",
        "advanced",
    }

    # Validate requested plan
    if data.plan not in allowed_plans:
        return {
            "success": False,
            "message": "Invalid plan.",
        }

    # Get session cookie
    session_token = request.cookies.get(SESSION_COOKIE_NAME)

    if not session_token:
        return {
            "success": False,
            "message": "Not authenticated.",
        }

    connection = get_connection()

    # Find authenticated session
    session = connection.execute(
        """
        SELECT user_id, expires_at
        FROM sessions
        WHERE session_token = ?
        """,
        (session_token,),
    ).fetchone()

    if not session:
        connection.close()

        return {
            "success": False,
            "message": "Invalid session.",
        }

    # Check session expiration
    expires_at = datetime.fromisoformat(session["expires_at"])

    if expires_at <= datetime.now(timezone.utc):
        connection.close()

        return {
            "success": False,
            "message": "Session expired.",
        }

    # Get current user plan
    user = connection.execute(
        """
        SELECT plan
        FROM users
        WHERE id = ?
        """,
        (session["user_id"],),
    ).fetchone()

    if not user:
        connection.close()

        return {
            "success": False,
            "message": "User not found.",
        }

    # IMPORTANT:
    # A user can only choose a plan once.
    if user["plan"] is not None:
       connection.close()

       return {
            "success": False,
            "message": "You have already selected a plan.",
            "plan": user["plan"],
        }

    # Save selected plan
    connection.execute(
        """
        UPDATE users
        SET plan = ?
        WHERE id = ?
        """,
        (
            data.plan,
            session["user_id"],
        ),
    )

    connection.commit()
    connection.close()

    return {
        "success": True,
        "message": "Plan selected successfully.",
        "plan": data.plan,
    }


def create_session(user_id):
    session_token = secrets.token_urlsafe(32)

    expires_at = (
        datetime.now(timezone.utc) + timedelta(days=30)
    ).isoformat()

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO sessions (
            session_token,
            user_id,
            expires_at
        )
        VALUES (?, ?, ?)
        """,
        (
            session_token,
            user_id,
            expires_at,
        ),
    )

    connection.commit()
    connection.close()

    return session_token


@app.post("/api/auth/logout")
def logout(request: Request, response: Response):

    session_token = request.cookies.get(SESSION_COOKIE_NAME)

    if session_token:

        connection = get_connection()

        connection.execute(
            """
            DELETE FROM sessions
            WHERE session_token = ?
            """,
            (session_token,),
        )

        connection.commit()
        connection.close()

    response.delete_cookie(
        key=SESSION_COOKIE_NAME,
        httponly=True,
        samesite="lax",
    )

    return {
        "success": True,
        "message": "Logout successful.",
    }
