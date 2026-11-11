import secrets
from fastapi import Request

from argon2 import PasswordHasher

from app.database import run_query

ph = PasswordHasher()

def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return  ph.verify(password_hash, password) 

def create_session(user_id: int) -> str:
    token = secrets.token_hex(16)
    run_query(
        "INSERT INTO sessions (user_id, session_token) VALUES (%s, %s)",
        (user_id, token),
        commit=True,
    )
    return token


def get_user_from_session(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token:
        return None
    session = run_query(
        """
        SELECT u.* FROM sessions s
        JOIN users u ON u.id = s.user_id
        WHERE s.session_token = %s
        """,
        (session_token,),
        fetchone=True,
    )
    return session


def clear_session(token: str):
    run_query("DELETE FROM sessions WHERE session_token = %s", (token,), commit=True)
