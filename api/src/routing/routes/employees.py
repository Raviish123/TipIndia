from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from utils.db import CurrentUser, SessionDep
from utils.models import *
import utils.auth as auth


router = APIRouter()


@router.get("/organization", response_model=EmployerOrganization)
def get_organization(current_user: CurrentUser) -> Any:
    return current_user


@router.post("/organization", response_model=EmployerOrganization)
def create_organization(*, session: SessionDep, current_user: CurrentUser, organization_in: EmployerOrganizationCreate):

    user = auth.get_org_by_email(session=session, email=organization_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Organization already exists")
    
    if current_user.email != "panicker.raviish2@gmail.com":
        raise HTTPException(status_code=400, detail="You are not Raviish")

    user = auth.create_organization(session=session, organization_create=organization_in)
    return user


@router.get("/{employee_id}", response_model=Employee)
def get_employee(session: SessionDep, employee_id: str):
    employee = session.get(Employee, employee_id)

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    if not employee.is_active:
        raise HTTPException(status_code=404, detail="Employee is inactive")
    
    return employee

@router.get("/organization/{organization_id}", response_model=OrganizationEmployees)
def get_employees_by_organization(session: SessionDep, organization_id: str):
    statement = select(Employee).where(Employee.org_id == organization_id)
    employees = session.exec(statement).all()

    if not employees:
        raise HTTPException(status_code=404, detail="Organization is not registered with TipIndia")

    return OrganizationEmployees(
        org_id=organization_id,
        organization_name=employees[0].organization.organization_name,
        organization_description=employees[0].organization.organization_description,
        data=employees
    )

@router.post("/")
def create_employee(*, session: SessionDep, employee_in: EmployeeCreate):
    if not session.get(EmployerOrganization, employee_in.organization_id):
        raise HTTPException(status_code=404, detail="Organization not found")
    return auth.create_employee(session=session, employee_in=employee_in)


@router.delete("/")
def delete_employee(*, session: SessionDep, current_user: CurrentUser, employee_id: str):
    employee = session.get(Employee, employee_id)

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    if not current_user.organization_id == employee.organization.organization_id:
        raise HTTPException(status_code=400, detail="Operation requires authentication")
    
    session.delete(employee)
    session.commit()
    return {"result": "success"}