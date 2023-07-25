from fastapi import status, HTTPException, Depends, APIRouter
from . import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

  # checking if the provided post_id exists in db
  post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id {vote.post_id} does not exists")

  # checking for pre-existing vote for the specific post_id and user_id is same as the current_user_id
  vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)

  found_vote = vote_query.first()
    
  # vote.dir == 1 means current user wants to like a post with provided post id
  if (vote.dir == 1):
    # user has previously like the post already
    if found_vote:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                          detail=f"user {current_user.id} has already liked the post {vote.post_id}")
    
    # here current user didnt like the post beforehand
    new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)

    db.add(new_vote)
    db.commit()

    return {"message": "successfully added vote"}
    
  else:
    # dir == 0 means current user wants to delete a pre-existing vote
    if not found_vote:
      # vote doesnt exists, we cant delete a vote that doesnt exists
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"vote does not exists")
    
    # vote exists
    vote_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "successfully deleted vote"}