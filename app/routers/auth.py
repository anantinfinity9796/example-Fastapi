""" This would store the code for the authentication processes and user validation and login functions"""

from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils
from .. import oauth2

# we are not going to pass the user login credentials in the body of the JSON request instead we would use FastApi to do that.

from fastapi.security.oauth2 import OAuth2PasswordRequestForm



router = APIRouter(tags = ["Authentication"])

@router.post('/login', response_model= schemas.Token_Response)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    # now we will query our database to retrieve our user credentials
    # The thing about the OAuth2PasswordRequestForm is that it retrieves the data of the user in the form of a dict with 'username' and 'password' as keys.
    # Now we would have to use the form data option instead of Raw JSON in the Postman Request.
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Invalid Credentials")


    # Check whether the hash of the password provided by the user is same as the one retrieved from the database.
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'Invalid Credentials')


    # Create a JWT token.
    access_token = oauth2.create_access_token(data = {"user_id":user.id})
    # return token
    return {"access_token":access_token, "token_type" : "bearer" }