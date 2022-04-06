""" This file keeps the Schemas related to the pydantic models for the request and response """

# Creating a template(schema) of out post
from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

from app.models import Post

""" The below calasses are the Pydantic Models for Requests particularly the way the requests given by a user should be structured so that their validation and use 
becomes easy"""
class PostBase(BaseModel):
    title: str
    content:str

    # lets say that we wanted to define a property that was optional i.e the user could decide to publish or not publish a post.
    published : bool = True
    
    # # lets say that we want to provide a field that is completely optional i.e. if the user does not provide it, it's set to None.
    # rating: Optional[int] = None

class PostCreate(PostBase):
    pass

# The below code should be after class UserCreate but due to some dependency issue in Post_Response we have pasted it here.
""" But when a user is being created he is getting his password back as plain text. 
So we need to define a Response Model to make sure that any unwanted details do not go in the response body. """
class UserCreate_Response(BaseModel):
    id : int
    email : EmailStr
    created_at: datetime

    # This would also be a SQL Alchemy model. So we would need to convert it to Pydantic
    class Config:
        orm_mode = True
    pass



""" The below classes are Pydantic Models of Response so that their Schema validation becomes easy and we return only the data that the user has permission to access 
    and not the whole document."""

class Post_Response(PostBase):
    id : int
    created_at :datetime
    owner_id : int
    owner : UserCreate_Response
    # The bottom 3 fields are inherited from the PostBase class
    # title: str
    # content : str
    # published: bool

    """ SQL Alchemy will return a model of SQL Alchemy type which cannot be interpreted by our pydantic model because it want's the schema to be a dictionary.
        So we need to tell it that it should just overlook that its not a dict and validate it anyway.
        The below code snippet does that"""
    class Config:
        orm_mode = True


""" We would need to create a new schema for validating the data that the uer provides to genrate the user """
class UserCreate(BaseModel):
    email : EmailStr  # This could have been a string but pydantic would also verify that it satisfies the constraints of an email.
    password : str



""" When a user requests information about his acoount we need to provide him with the details. So we would create a Response Model
    which return the details of the user and does not return the password."""

class UserReturn_Response(UserCreate_Response):
    pass


""" The user provides his/her login credentials which need to be schema validated """

class UserLogin(BaseModel):
    email : EmailStr
    password: str


""" The schema for verifying the JWT token """

class Token_Response(BaseModel):
    access_token:str
    token_type: str

""" Schema for the token data"""

class TokenData(BaseModel):
    id: Optional[str] = None


""" This class would be used to validate the request by the user when he tries voting on a post"""
class Vote(BaseModel):
    post_id : int
    direction : conint(le = 1)



""" Schema for validation of POSTS with VOTES data """
class Post_Vote_Response(BaseModel):
    Post: Post_Response
    votes : int

    class Config:
        orm_mode = True