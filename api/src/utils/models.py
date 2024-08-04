from sqlmodel import Field, Relationship, SQLModel
from pydantic import EmailStr
import uuid


# TODO: If deactivate an organization, also deactivate all employees
class EmployerOrganizationBase(SQLModel):
    email: EmailStr = Field(unique=True)
    organization_name: str = Field(max_length=50)
    organization_description: str = Field(max_length=50)
    is_active: bool = True


class EmployerOrganization(EmployerOrganizationBase, table=True):
    __tablename__ = 'organizations'

    organization_id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    hashed_password: str
    total_tips: int = 0
    employees: list["Employee"] = Relationship(back_populates="organization", sa_relationship_kwargs={"lazy": "selectin"})

class EmployerOrganizationCreate(EmployerOrganizationBase):
    password: str = Field(max_length=100)

class EmployeeBase(SQLModel):
    name: str = Field(max_length=50)
    is_active: bool = True
    upi_id: str = Field(max_length=50)


class Employee(EmployeeBase, table=True):
    __tablename__ = "employees"
    
    employee_id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    org_id: str = Field(foreign_key="organizations.organization_id", nullable=False)
    organization: EmployerOrganization = Relationship(back_populates="employees", sa_relationship_kwargs={"lazy": "selectin"})

class EmployeeCreate(EmployeeBase):
    organization_id: str

class OrganizationEmployees(SQLModel):
    org_id: str
    organization_name: str
    organization_description: str
    data: list[Employee]

class TipBase(SQLModel):
    employee_id: str
    amount: int

class TipCreate(TipBase):
    pass

class Tip(TipBase, table=True):
    __tablename__ = "tips"

    org_id: str
    tip_id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    datetime: str

# class TipList(SQLModel):
#     org_id: str
#     data: list[Tip]

class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(SQLModel):
    sub: str | None = None

