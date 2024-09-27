from sqlalchemy.orm import Session
from models import User
import bcrypt

def create_user(db: Session, name: str, email: str, password: str, role):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = User(name=name, email=email, passwd=hashed_password, role=role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def verify_user_password(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if user and bcrypt.checkpw(password.encode('utf-8'), user.passwd.encode('utf-8')):
        return True
    return False

def update_user_role(db: Session, user_id: int, new_role):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.role = new_role
        db.commit()
        db.refresh(user)
        return user
    return None

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False
