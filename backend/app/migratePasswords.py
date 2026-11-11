from app.auth import hash_password
from app.database import run_query

users = {
    "admin@dat250.local": "Admin123",
    "teacher@dat250.local": "Teacher123",
    "ta@dat250.local": "TA123",
    "alice@student.uis.no": "Alice123",
    "bob@student.uis.no": "Bob123",
    "charlie@student.uis.no": "Charlie123",
}

def main():
    for email, password in users.items():
        password_hash = hash_password(password)

        run_query(
            "UPDATE users SET password_hash = %s WHERE email = %s",
            (password_hash, email),
            commit=True,
        )

        print(f"Processed password update for {email}")


if __name__ == "__main__":
    main()
