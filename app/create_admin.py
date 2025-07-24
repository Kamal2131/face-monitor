# app/create_admin.py

from getpass import getpass
from app.database import SessionLocal
from app.models import User
from passlib.hash import bcrypt

def main():
    db = SessionLocal()

    print("=== Create Admin User ===")
    username = input("Enter admin username: ")
    password = getpass("Enter password: ")  # Hides input
    confirm = getpass("Confirm password: ")

    if password != confirm:
        print("❌ Passwords do not match.")
        return

    # Check if user already exists
    existing_user = db.query(User).filter(User.name == username).first()
    if existing_user:
        print("❌ User already exists.")
        return

    # Create new admin
    hashed_password = bcrypt.hash(password)
    admin = User(name=username, password_hash=hashed_password, role="admin")
    db.add(admin)
    db.commit()
    db.refresh(admin)

    print(f"✅ Admin user '{username}' created successfully.")

if __name__ == "__main__":
    main()
