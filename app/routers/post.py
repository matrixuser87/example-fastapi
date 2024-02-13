from fastapi import HTTPException, status, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from .. import models, oauth2
from ..database import get_db
from ..schema import Post

router = APIRouter(
    prefix="/posts",
    tags=["Posts"])


# Get all posts for current user
@router.get("/")
def get_posts(db: Session = Depends(get_db), token_data: str = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post)\
        .filter(models.Post.owner_id == token_data.id)\
        .all()
    return posts


@router.get("/{id}")
def get_post_by_id(id: str, db: Session = Depends(get_db), current_user_id: str = Depends(oauth2.get_current_user)):
    assert_int_id(id)

    post = db.query(models.Post).filter(models.Post.id == id).first()
    return {"data": post}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post: Post, db: Session = Depends(get_db), token_data: str = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=token_data.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_by_id(id, db: Session = Depends(get_db), token_data: str = Depends(oauth2.get_current_user)):
    try:
        post_id = int(id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Id should be a valid integer")

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")

    if post.owner_id != token_data.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform this action")

    post_query.delete(synchronize_session=False)
    db.commit()


def assert_int_id(id: str):
    try:
        int(id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Id should be a valid integer")
