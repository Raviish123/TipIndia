from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from utils import auth
from utils.db import SessionDep
from utils.models import Token

router = APIRouter()


@router.post("/login/access-token")
def login_access_token(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:

    employer_organization = auth.authenticate(session=session, email=form_data.username, password=form_data.password)

    if not employer_organization:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    elif not employer_organization.is_active:
        raise HTTPException(status_code=400, detail="Inactive organization")
    
    return Token(access_token=auth.create_access_token(employer_organization.organization_id, expires_delta=timedelta(minutes=1))) # TODO 1


# TODO 1: Create environment variable for access token expiry