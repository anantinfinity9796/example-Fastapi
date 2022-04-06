""" All the path operations dealing with posts will be under this file"""

# Importing the nescessary Libraries
from fastapi import Depends, FastAPI, Response, status, HTTPException
from sqlalchemy.orm import Session

from app import oauth2
from ..database import get_db
from .. import models, schemas , utils, oauth2
from typing import Optional, List
from sqlalchemy import func    # this give us access to functions like count.

# One thing that we do not have is that we dont have access to the APP object. This is where the ROUTER comes in.
from fastapi import APIRouter


# Then we initialize the router object and since we do not have access to the APP object in this file we would replace @app with our router object
""" We can see that all the routes end with the /posts. As our API is very simple we can copy the path operations for each CRUD 
    operation but for complex API's copying for each post becomes too cumbersome. So we could pass a parameter into the
    API router function called as prefix. And as every route here begins with '/posts' we can add /posts as the parameter and 
    add just a '/' inplace of '/posts' """

router = APIRouter( prefix = "/posts",
                    tags = ['Posts']) # This groups all the individual path parameters into one group Posts in the Swagger documentation







@router.get("/",response_model= List[schemas.Post_Vote_Response])  # The " /posts " is the new path operation which return a list of posts of the user.
def get_posts(db:Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user), skip:int = 0, search:Optional[str] = "", limit: int =100):
    # # To retrieve the lists of posts we need to query the databse with our cursor object.
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # print(posts)

    # just put a filter on the query that retrieves the post to return only the posts where the owner_id of the user which created the post matches current_user id.
    # the filter is .filter(models.Post.owner_id == current_user.id).all()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # The limit function is the query parameter which will limit the query results displayed. 
    # The offset method just skips the results by the skip variable in the results 
    # The filter just filter the query with the search keyword that the user provides. 

    # We would need to return the number of likes on a post in the response so for that we would need to query the databse 
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id,
                isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    results = results.all()

    
    return results

""" They way fast API works is that when a request is made the API goes through your code and what is does is that it finds
 the matching decorator with the method in the code and then it finds the matching path operation in the brackets of the http
 method and it executes the first match. So if there is a same method with the same path operation later on in the code it
 won't be executed and returned to the user. """


 # Creating a post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.Post_Response)
def create_post(post : schemas.PostCreate, db: Session = Depends(get_db), current_user : str = Depends(oauth2.get_current_user)):
    # To create a post with a model we need to reference the specific models file and provide the fields nescessary to create a post.
    # To avoid doing post.title, post.content etc, for multiple fields. We can just add a shortcut and just convert the post to dict and unpack the dict and it automatically populates all the fields.

    # print(current_user.id)
    new_post = models.Post(owner_id = current_user.id, **post.dict())  # automatically unpacks all the fields.

    # To commit changes with SQL Alchemy we need to commit it to the databse.
    db.add(new_post) # adds the newly created post to the databse
    db.commit()      # commiting the changes to the databse via the session object.

    # And we dont have the facility of the SQL statements so we cannot use RETURNING *. Instead we use db.refresh()

    db.refresh(new_post) # This retrieves the newly created post and stores it again in the now_post variable.



    """ So what we are doing here is that we are creating a post and passing the data as json and this function is parsing 
    the data by importing the Body method from the fastapi.params, converting data into a dict and assigning it into a
    variable called as payload and then it is being printed out into the console and the mesaage is being returned to the user."""
    
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published) )
    # # we can also execute it with a python f string like cursor.execute(f"" INSERT INTO posts (title, content, published) VALUES ({post.title},{post.content},{post.published})"")
    # # But doing it with an fstring makes us vulnerable to a SQL injection attack as a hacker can potentially pass a SQL query as title and manipulate the database.
    # # Postgres can sanitize the parameters passed and could check for potential queries in the parameters and warn us.
    # new_post = cursor.fetchone()


    # So anytime we create a post we need to send a response of 201 to the user with a post created message.
    # But the message that this endpoint displays when a post is created is " 200 OK ".
    # So to change the default we would just edit the decorator path object with status_code = 201



    # To add the post data sent to this url we would need to parse it and add to the my_posts list.

    # To add the changes made by the API to the database we have to commit the changes to the database.
    # conn.commit() # commiting the changes

    # If we ever need to convert out pydantic model to dictionary we can just use the .dict() method of the model.
    return new_post

# Finding one post by id
# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p

# Endpoint for getting one post
@router.get("/{id}", response_model = schemas.Post_Vote_Response)
def get_one_post(id:int, response : Response, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):

    # post = db.query(models.Post).filter(models.Post.id == id).first()

    # We also need to get the vote count when a user retrieves one post. So we will validate using the POST_VOTE_Response and query according to it.
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id,
                isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()




    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()

    # If we dont find a post we would send the status code 404
    if post == None:
        # response.status_code = 404
        # instead of hardcoding the value we could just import the status module which provides us with all the status values and select from that.
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} not found"}
        # The above is also a very verbose and requires us to hardcode the responses. We can raise an Http exception built into Fast_API to do this better.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")

    # The below code is used to show only the posts that the owner has created
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform the requested action")


    return post


# This function finds the index of the post based on the id provided.
# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i


# API Endpoint for Deleting a Post
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session=Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id) #query the db with id

    post = post_query.first()


    # # deleting a post is like referencing a post by it's unique ID and removing it from the list of posts.
    # # the satus code for deleting something is 204. So we need to update it
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,(str(id)) )
    # deleted_post = cursor.fetchone()

    # conn.commit()

    if post == None: # If post is not present raise 404 error.
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f" The post with id: {id} does not exist")
    


    # This check is being done so that the user can only delete the posts that he has created.
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform the requested action")
    
    post_query.delete(synchronize_session= False)
    db.commit()

    


    # But when we delete something we dont want to send any data back. So we send a status code instead of a message.
    # return {"message": "The post was sucessfully deleted"}

    return Response(status_code = status.HTTP_204_NO_CONTENT)


# API endpoint for Updating a Post
""" for updating a post we have two methods which require two formats of input
        1. put - This requires us to send the whole data stream irrespective of the field to be updated.
        2. patch - This requires us to send data for only the fields that need to be updated. """

@router.put("/{id}", response_model = schemas.Post_Response)
def update_post(id:int, updated_post:schemas.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()


    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content,
    #                                                                                      post.published,str(id)))
    # updated_post = cursor.fetchone()

    # conn.commit()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f" The post with id: {id} does not exist")
    

    # This check is being done so that the user can only update the posts that he has created.
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform the requested action")
    
    post_query.update(updated_post.dict(), synchronize_session=False) # we pass the new values as a dictionary in the update mehtod.
    db.commit()

    return post_query.first()