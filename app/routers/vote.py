""" This file would contain the path operations also known as routers of the voting functionality."""


from fastapi import FastAPI, Depends, APIRouter, Response, status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2
router  = APIRouter(prefix = "/vote",
                tags = ["Vote"])

@router.post("/", status_code = status.HTTP_201_CREATED)
def vote(vote:schemas.Vote, db : Session = Depends(database.get_db), current_user: str = Depends(oauth2.get_current_user)):
    """ Since we need to get response from the user there are a couple of things we need to pass in:
        1. Schema for validating the vote respponse.
        2. The databse session
        3. current user in the session
        3. The user authetication and logging in parameters"""

    # we would first query the database to see if the user has tried to vote on a post that does not exist. If so then we will just raise an error
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {vote.post_id} does not exist")




    #query the database to retrieve the post with the post_id and the user_id if of the user who has voted on the post that the user is trying to vote.
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first() # retrieve the first result
    

    if vote.direction == 1: # If the user is trying to upvote the post
        if found_vote:  # If you have found that the user has already voted on the post
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = f"user {current_user.id} has already voted on post {vote.post_id}")
        else: # when the user has not already voted on the post just set post_id field of the votes table to id of the post that the user is trying to like and the user_id field to the current user_id
            new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id) # create the post_id,user_id combo that the user is trying to like to the votes table.
            db.add(new_vote) # add the new vote to the table
            db.commit() # commit the changes.
            return {"message":"successfully added vote"}
    
    else: # If the user is trying to downvote the post or unlike the post then he sends a direction = 0.
        if not found_vote: # If the post that the user has tried to vote on does not exist
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Vote does not exist")
        else:
            vote_query.delete(synchronize_session= False)   # delete the post_id, user_id combo because the use os trying to unlike the post
            db.commit()
            return {"message": "successfully deleted vote"}

