""" Anything related to the JWT tokens and authentication will be accessed from Here """

# Importing the nescessary libraries

from ast import Pass
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from .config import settings
from sqlalchemy.orm import Session

""" There will be 3 pieces of information that we need to provide for our token:
        1. SECRET_KEY : Handles verifying the integrity of our token and resides on our server only.
        2. ALGORITHM : The cryptography algorithm used --> HS256.
        3. EXPIRATION TIME: After what time the token will expire. """

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCES_TOKEN_EXPIRE_MINUTES =settings.access_token_expire_minutes
 
# the token url will be our login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl= 'login' )


def create_access_token(data : dict):

    to_encode = data.copy()    # Copying the data helps not to change the original data in any way

    expire = datetime.utcnow() + timedelta(minutes = ACCES_TOKEN_EXPIRE_MINUTES )

    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY, algorithm = ALGORITHM)  # makes the JWT token with the required information mentioned above

    return encoded_jwt


def verify_access_token(token:str, credentials_exception):
        """ This Functions verifies the access token data. """
        try:
                payload = jwt.decode(token, SECRET_KEY, ALGORITHM) # decodes the payload from the token by secret key and hashing algo

                # to extract the data we can do payload.get(field to get)
                id:str = payload.get("user_id")

                if id is None:
                        raise credentials_exception
                
                token_data = schemas.TokenData(id  = id)  # validates that the token matches our token schema
        except JWTError:
                raise credentials_exception

        return token_data   # we return the token data which is nothing more than the id.


# We can pass the below function as a dependency in any of our path operations.
# Its going to take the token from the request automatically verify that the token is correct and extract the id from the token
# we can also automatically fetch the user from the databse and then add it as a parameter into our path operation functions.

""" Anytime we have a specific endpoint that should be protected i.e the user needs to be logged in to use it. What we are gonna do it that 
we can add an extra dependency in the path operation function  (user_id: int = Depends(oauth2.get_current_user)). So anytime anyone
wants to access a resource that reuires them to be logged in we expect them to provide and access token and then provide them with dependency
 which is going to call the function get_current_user and then we pass in the token that comes from the request and then we are going to run the 
 verify_access_token  which verifies that the token is okay. If there is no errors then the user is successfully authenticated """

def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
        """ In this function we can fetch the current user from the database automatically"""

        credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail= 'Could not validate credentials',
        headers = {"WWW-Authenticate": "Bearer"})


        token  = verify_access_token(token, credentials_exception)

        user = db.query(models.User).filter(models.User.id == token.id).first()

        return user