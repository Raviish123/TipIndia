from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from utils.db import CurrentUser, SessionDep
from utils.models import *
import utils.auth as auth

import datetime

router = APIRouter()


@router.get("/tips")
def get_total_tips(*, session: SessionDep, current_user: CurrentUser):

    statement = select(Tip).where(Tip.org_id == current_user.organization_id)
    tips = session.exec(statement).all()
    total = 0
    for tip in tips:
        total += tip.amount

    return total


@router.post("/add_tip")
def add_tip(*, session: SessionDep, tip_in: TipCreate) -> Tip:
    employee = session.get(Employee, tip_in.employee_id)

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db_item = Tip.model_validate(tip_in, update={"datetime": datetime.datetime.now().isoformat(), "org_id": employee.org_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item