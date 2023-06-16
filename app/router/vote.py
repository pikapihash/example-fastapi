from fastapi import FastAPI, Response , status , HTTPException, Depends , APIRouter
from .. import schemas , database , models , oauth2
from sqlalchemy.orm import Session
router = APIRouter(
    prefix = "/votes",
    tags=['Vote']
    
)
@router.post("/")
def vote_sys(vote:schemas.Vote , db:Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"this post {vote.post_id} does not exits")
    vote_query = db.query(models.Vote).filter(models.Vote.user_id == current_user.id, models.Vote.post_id == vote.post_id )
    found_query = vote_query.first()
    if (vote.dir==1):
        if found_query:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail="This id {current_user.id} already vote this post")
        new_query = models.Vote(post_id = vote.post_id , user_id =current_user.id )
        db.add(new_query)
        db.commit()
        return{"message":"vote has successfully add"}
    else:
        if not found_query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"sorry post does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return{"message":"vote had successsful delete "}
 

            