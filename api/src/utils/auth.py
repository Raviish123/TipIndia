from typing import Any
from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer


from sqlmodel import Session, select

from .models import Employee, EmployerOrganization, EmployeeCreate, EmployerOrganizationCreate




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_instance = OAuth2PasswordBearer(tokenUrl="/api/login/access-token")


def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, "3qFcWEfxgMWm_en11JSq83bv4TpB5gN7CEyCAb36PWI=", algorithm="HS256") # TODO HERE
    return encoded_jwt


def verify_password(*, plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# TODO: Put secret key into environment variable or pydantic basesettings!!!!



def get_org_by_email(*, session: Session, email: str) -> Employee | None:
    statement = select(EmployerOrganization).where(EmployerOrganization.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> EmployerOrganization | None:
    db_user = get_org_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(plain_password=password, hashed_password=db_user.hashed_password):
        return None
    return db_user


def create_employee(*, session: Session, employee_in: EmployeeCreate) -> Employee:
    db_item = Employee.model_validate(employee_in, update={"org_id": employee_in.organization_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

def create_organization(*, session: Session, organization_create: EmployerOrganizationCreate) -> EmployerOrganization:
    db_item = EmployerOrganization.model_validate(organization_create, update={"hashed_password": get_password_hash(organization_create.password), "total_tips": 0})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item
