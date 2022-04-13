from fastapi import FastAPI, status
from .database import engine
from . import models
from .config import Settings
from fastapi.middleware.cors import CORSMiddleware   # used for circumventing the CORS protocol



# In this file we will need to reference the routers because we dont have any path operations defined here and the app is situated in this file only.
from .routers import post, user, auth, vote 


# we will be needing this to create all of our  SQL Alchemy models when our file is RUN. This would create the tables in the models.py file.
# models.Base.metadata.create_all(bind = engine)
# The above code was used to create the tables from the models.py but with the use of alembic we dont have to do it manually anymore.
# So we can keep it for reference for alternative ways of doing things.



# """ Now we have transferred our main.py file to the app folder so we would need to reload with the uvicorn command
#      uvicorn app.main: app --reload
#      previously we were loading it with 
#      uvicorn main:app --reload """

app = FastAPI()       ## creating our Base APP object.


# origins = ["https://www.google.com", "https://www.youtube.com"]   # The domains which can talk to our API.
origins = ["*"]
# If you want to set a public API so that you can get requests from every domain the just set origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins =  origins,    # Allow the domains in the origins list
    allow_credentials  = True,
    allow_methods=["*"],        # We can also allow specific http mehtods. If were building a public API we may not to allow them to have post or put or delete http methods.
    allow_headers=["*"]         # We can allow specific headers as well
)






# creating a temporary array to store the post. We would use database to store the the posts afterwards.
# """ We will need to hardcode the posts because due to lack of database every time we close the editor the values would get reset"""

# my_posts = [{"title":"title of post1",
#              "content":"content of post1",
#              "id":1},
#              {"title":"Favourite foods ",
#              "content":"I like pizza very much",
#              "id":2}]




# # testing path route
# @app.get("/sqlalchemy")
# def test_posts(db:Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data": posts}




# """Now we would include the router files of post and users which contain the path operations for posts and users and call them here
#     so that they could be executed and added to our APP object which we were working with."""
app.include_router(post.router)  # including the router object and all the path operations of post.py file.

# The above command would reference the path operations in Sequence as it did when it was in main file.

app.include_router(user.router)  # including the router object and all the path operations of user.py file.

app.include_router(auth.router) # including the router object and all the path operations in auth.py file.

app.include_router(vote.router) # include the router object and all the path operations in the vote.py file.

@app.get('/')      # This is the PATH OPERATION. The " / " signifies the root url. The ".get " is the http method.
async def root():  # The async keyword just helps to give out requests asynchronously
    return {'message':'Successfully deployed from CI/CD Pipeline' }













