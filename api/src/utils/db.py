from sqlmodel import Session, create_engine, select, SQLModel
from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from pydantic import ValidationError

from .models import *
from .auth import oauth2_instance


def get_db():
    with Session(engine) as session:
        yield session

# TODO: Turn this URL into pydantic basesettings / environment variable and convert to postgres
engine = create_engine(str("sqlite:///database/database.db"))

SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(oauth2_instance)]



def init_db():
    SQLModel.metadata.create_all(engine)
    

def get_current_user(session: SessionDep, token: TokenDep) -> EmployerOrganization:

    try:
        payload = jwt.decode(token, "3qFcWEfxgMWm_en11JSq83bv4TpB5gN7CEyCAb36PWI=", algorithms=["HS256"]) # TODO: Change this secret key to env/pydantic settings
        token_data = TokenPayload(**payload)
    except:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    

    user = session.get(EmployerOrganization, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="Organization does not exist")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive Organization")
    
    return user


CurrentUser = Annotated[EmployerOrganization, Depends(get_current_user)]
