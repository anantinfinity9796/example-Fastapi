""" All the Path Operations dealing with users will be put up in this file"""

# Importing the nescessary Libraries
from fastapi import Depends, FastAPI, Response, status, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils

# One thing that we do not have is that we dont have access to the APP object. This is where the ROUTER comes in.
from fastapi import APIRouter


# Then we initialize the router object and since we do not have access to the APP object in this file we would replace @app with our router object
""" We can see that all the routes end with the /users. As our API is very simple we can copy the path operations for each CRUD 
    operation but for complex API's copying for each post becomes too cumbersome. So we could pass a parameter into the
    API router function called as prefix. And as every route here begins with '/users' we can add /posts as the parameter and 
    add just a '/' inplace of '/users' """

router = APIRouter(prefix = "/users",
                    tags = ["Users"]) # This groups all the individual path parameters into one group Users in the Swagger documentation









# Creating the API endpoint for Generating a user based on the credentials provided by the user.
""" This would be a new path operation for creation of the user"""
""" When we creae a new user we have to do a couple of things
        1. We need to create the hash of the password given by the user. Password can be retrieved by user.password """


@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.UserCreate_Response)

def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)  # retrieves the password provided by the user and hashes it.
    user.password = hashed_password   # Update the user pydantic model's password with the hashed password. 

    new_user = models.User(**user.dict())  # initialize the user schema and and pass in the values provided by the user by unpacking the dict.
    db.add(new_user)   # add the schema to the users table
    db.commit()        # commit the changes
    db.refresh(new_user) # again query the same post and send it as a response to show the succesfull creation of the user.

    return new_user



# Now we need to setup and route or path operation or API endpoint for retrieving the user information based on the id provided by the user.
""" It could be a part of the authentication process so that you can retrieve information about your own account.
    """

@router.get("/{id}", response_model= schemas.UserReturn_Response)
def get_user(id:int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"The user with id {id} does not exist")

    
    return user