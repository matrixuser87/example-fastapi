from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session

from app import models, utils
from app.database import get_db
from app.schema import UserCreate

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd

    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {new_user}


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@router.get("/{id}")
def get_users(id: str, db: Session = Depends(get_db)):
    return db.query(models.User) \
        .filter(models.User.id == id) \
        .all()
