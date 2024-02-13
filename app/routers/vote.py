from fastapi import status, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from app import models, utils, oauth2
from app.database import get_db
from app.schema import UserCreate, Vote

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, db: Session = Depends(get_db), user_token: str = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")

    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id)

    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User {user_token.id} has already voted on post {vote.post_id}")
        new_vote = models.Votes(user_id=user_token.id, post_id=vote.post_id)

        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)

        return {"message": "successfully deleted vote"}
