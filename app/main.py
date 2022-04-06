from fastapi import FastAPI
from . import models
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
    return {'message':'This is my first API!!' }













# To control the content of the post that the user submits we need to define a schema for the posts. Pydantic can be used for this....
# POST --->   title:str, content:str,category, published or draft :True/False.


# """ A CRUD application is the one that need to create, read, update, delete the data.

# Best Practices for designing an API of a CRUD based application:

#     1. When it comes to naming a URL there are conventions one needs to follow:
#         1. Since we are working with posts it makes sense to name all the URL's with  " /posts " :
#             a. CREATE --> @app.post("/posts")

#             b. READ   --> @app.get(" /posts/{id} ")
#                       --> @app.get(" /posts")

#             c. UPDATE --> @app.put(" /posts/{id}")     # For put we need to pass values for all the fields
#                       --> @app.patch(" /posts/{id} ")  # for patch we can just update a specific field.
            
#             d. DELETE --> @app.delete(" /posts/{id} ") 
    
#     # Above we did not follow the best practice and named the creating post url as "/create_posts" but it should be "/posts" only.
#     """


# """ For now we just creating the posts and returning the data back to the user. Now we would need to save the posts somewhere also."""
# """ Typically we use a database to save the posts but now we would just use a global variable to save them which is defined at the start"""


# """ Typically when a task gets compelted or an Error occurs in fetching the API we get a Status Code like:
#     1. 200 : Evrything is Working fine
#     2. 404 : Resource not found , etc
# So far our API does not return these kind of responses. So we need to make sure that our API returns these responses to the user
# For that we would need to add a "response" object in out API functions which returns the appropriate response to the user upon
# executing a task. For this we need to import the response into our code from FAST_API and then we would be able to add it

# """




# """ As we are working with posts in our API and our choice of database is a relational database then we need to figure out the 
#     columns of our database:
#     1. title: As a post will have a title which will be a string.
#     2. content: A post will have some content which would be of type string.
#     3. id : unique --> The id will be a unique integer 
#     4. published : Boolean
#     5. Created_at : timestamp"""

# """ To work with a postgres database with a python application we need to have a POSTGRES driver so we need to install a library
# known as " psycopg ". It is the most widely used library for postgres connections """



# """ When working with databases in python or any other language code we can pass SQL queries directly as statements to our
#         programming languages driver which can be executed by the driver on the database.
        
#         But this has a problem that the programmer should have good knowldge of SQL to run queries
        
        
#         An OBJECT RELATIONAL MAPPER (ORM) solves the aforementioned problem as it sits between the databse and US . 
#         We can perform the execution of all traditional SQL queries without writing SQL code just through Python.
        
#         SQL Alchemy is the most popular standalone ORM's that is the most widely used in Python community.
#         It can be used with other web frameworks or any python based application.
        
#         But one thing we need to keep in our mind is that SQL Alchemy cannot talk to any database on its own i.e it does not have
#         support for database drivers. So we will need to install a Database driver for our respective databses such a psycopg2 for
#         POSTGRES database. Ultimately the driver will talk with the database and SLQ Alchemy just helps with the queries. """



# """ Some things that an ORM allows us to do
#     1. Make our database tables as Python Models.
#     2. Queries can be made exclusively through Python codes """


# """ We should not save string representations of the passwords in our databases instead we should save the hashes of the passwords
#     The passwords are impossible to reverse engineer from the hash."""



# """ We can see that we have path operations for CRUD operations for working with posts, and path operations for working with users.
#     But the main file is getting very cluttered and as we keep adding more and more operatiosn it becomes unmanageable.
#     So we break it out into two files.
#     1. For all of the routes or path operations that work and deal with Posts.
#     2. For all of the path opeartion that work with Users. 
    
#     This involves something called as 'ROUTERS' and it is not specific to Fast_API and all the frameworks have some sort of
#         system in place for tackling this problem. 'ROUTERS' help split up our path opertions so that we can organize our
#         code better. """


# """ The most important part of any application is the way it handles authentication.
#     There are really two main ways to handle authentication.
#         1. Session Based Authentication - We store something on our backend server/ API to track whether our user is logged in.
#         2. Using JWT token base Autentication - This is stateless i.e. there is nothing on our server that tracks whether a 
#                 user is logged in or not. The token itself is stored on the frontend and our client actualy keeps track whether our
#                 user is logged in or not.
#         """
# """ The Flow for JWT Authentication token for logging in and accesses a specific endpoint for JWT authentication:
#     1. The client or the frontend would try and log in with the path operation ('/login') with there credentials.
#     2. We will verify if the credentials are valid. Then we would create the JWT token(its like a string).
#     3. The token would be sent as a response back to the client.
#     4. Now he can start accessing resources that require authentication.
#     5. So lets say that he wants to see the posts. He would send a request to the ('/posts') endpoint but he would also send the {token} in the header of the request.
#     6. The API will verify if the token is valid with some mechanism. If it is then it just sends back the data. 
#     7. So the API does not have to store anything on the backend. All is given by the client and API just does the verification. """

# """ The basics of a JWT token. What exactly is it.
#         1. A JWT looks like a bunch of cryptic chracters jammed together but it is not encrypted.
#         2. It consists of 3 parts:

#             1. Header - It includes metadata about the token. It contains the algorithm used for hashing and the type = 'JWT'.
#                     It is fixed for all the tokens.

#             2. Payload - This is upto the user. Any piece of information can be sent within the payload but as the token is not 
#                     encrypted sensitive information should not be sent by the payload. So common things are: the user_id when 
#                     logging in, the users role: priviledge user or not. Jamming a lot of info would increase the size.

#             3. Signature : It is a combination of 3 things : 
#                             1. Header - the header provided above
#                             2. Payload - the payload of the token
#                             3. Secret - This is the most important thing. It is like a kind of a password stored that is kept on our
#                                 API. It's only there and no one else would know it. We would take the above 3 things and pass it to
#                                 the algorithm and it would return us the Signature which is used to determine if the token is valid
#                                 and no one else has tampered with it.
# """

# """ PURPOSE OF THE SIGNATURE 
#     1. Lets say that a user has sent his/her credentials and the API is in the process of sending back the token.
#     2. The token has the same 3 things that are discussed above: 
#         i. Header
#         ii. Role : user(not a priviledged user)
#         iii. Signature : We take the header, payload and the secret and pass it to a hashing functions and we make a signature and 
#                 pass it back to the toekn and then to the user.
#     3. Lets say a user decides to do a shady thing and the user decides to change the token by a little and changes a few bits in the token
#         and changes the role form user to admin. But he could have changed anything. But he cannot do anythin because the signature
#         that was generated with the token was generated for the role:user, so its no longer valid, so he will have to create a brand
#         new signature to match the data he is sending. However he cant create the signature because he doesn't have the supe secret password
#         which only resides on our API.
#     4. Lets say the user does send a token with a artificial signature to the API. What the API does is that he takes the Header, Payload and the
#         SECRET  pasword stored in the API and creates a TEST SIGNATURE and then compares them and the tokens do not match.
#     5. Thats why the SECRET PASSWORD is so important because it ensure that no other token can be generated by anyone else. """

# """ Lets discuss how we are going to handle logging of the user. Specifically how we are going to verify if the credentials are correct.

#     1. The user is going to hit the LOGIN endpoint with his [email + password(in plain text)]. When that happens we are going to search the databse
#         to try to find the user based of his username and email and the databse is going to send all the data back including the password(hashed).
#         But how exactly we compare the hashed password from the database with the plain text password provided by the user because the hashed password 
#         cannot be converted to the plain text. So we take the plain text password and hash it again and then compare them and then we see if they are equal.
#     2. If the password is correct then the token is generated and returned.
# """
# """ First we will need to install a library that helps install signing and verifying JWT tokens : Python-jose
# """


# """ We would also need to verify in our application if the token has not expired. So we will set up a schema in the schema file."""

# """ Anytime we have a specific endpoint that should be protected i.e the user needs to be logged in to use it. What we are gonna do it that 
# we can add an extra dependency in the path operation function  (get_current_user: int = Depends(oauth2.get_current_user)). So anytime anyone
# wants to access a resource that reuires them to be logged in we expect them to provide and access token and then provide them with dependency
#  which is going to call the function get_current_user and then we pass in the token that comes from the request and then we are going to run the 
#  verify_access_token  which verifies that the token is okay. If there is no errors then the user is successfully authenticated """



# """ Now we are going to look at some of the more advanced features of Postman starting off with Environments
#     --> An environment is a set of variables that allows you to switch the context of your requests.
#     If we look at all our postman requests we can see that we have hardcoded it to 127.0.0.1:8000. And if we deploy our app, its 
#     not gonna be deployed on the localhost. It's gonna be deployed on some public IP somewhere on the internet. So when we would test out our
#     production server  or make some test request to it we would have to change everything in our requests and continuously flip back and form 
#     development to production and back.

#     So to circumvent the above problem and avoid hard coding these values we would define a variable that changes depending on what environment
#      we use within postman. 
# """

# """Now that we have built authentication in our API, testting out API has got a little more challenging as the user has to be authenticated
# before we do anything which is very cumbersome. Luckily Postman can automate this task of authenticating the user with the help of environment
# variables.
# 1. Generate a new access token by logging in the user. Go to test in options. There is an example snippet of set environment variables
#     The snippet is :--> pm.environment.set("variable_key", "variable_value");
#     Which transforms to --> pm.environment.set("JWT", pm.response.json().access_token); this would be the code to set up the environment variables
#     variable_key : JWT
#     variable_value : This is the value of the bearer token which is in the pm.response.json().access_token. This would automatically take the authentication
#     JWT token and pass it to the environement variable as soon as a new user authenticated himself by providing the credentials.
# 2. Then go to the request you want to send. Go to the Authorization tab, select Bearer Token from the drop down menu and set {{JWT}} as the token value
#     instead of the original JWT string. This would automatically pass the string to the required field and we won't need to input it everytime.
# 3. So anytime we log in a user its going to update the variable.

# """


# """ Relationships of the Posts table and users table.
#     1. In our application there is nothing that ties a post to the users that created it.
#     2. So we need to set up some kind of a special relationship between the users and the posts table which allows us to relate
#         both the tables together.
#     3. The way we do that is that we create an extra column in both the tables. An we are going to set up a foreign key.
#     4. we tell  SQL how a column in a table is connected to other table by the help of a foreign key.
#     5. We specify two things : Table that its connected to (users table) and column that it is connected to (id column).
#         5.1. The data types of both the columns need to match.
#     6. Then whichever user creates this post we just embed the id of that specific user in the user_id column in the posts table.
#     7. Thats all we have to do to create a relationship between tables.
#     8. The above is referred to as a ONE TO MANY RELATIONSHIP in a SQL databse because ONE user can have MANY posts which he created.
#     9. However a post can only be created by one user."""

# """ We are going to use SQL Alchemy to generate all the tables and provide all the foreign keys as well.
#     So we would define them in the models.py file as we have been doing so."""

# """ currently we have the authentication set up for a user to login and create posts. We do not have any logic set up to prevent a user
#     when he is deleting someone elses posts. So we need to implement that also."""


# """ One thing that we need to do is that we need to send in some additional information in the response of when creating a post. Because 
#     instead of displaying the owner id of the user we would need to display the Name or the user_id of the user like it gets displayed in
#     twitter and other social media apps. In sqlalchemy we can actually set it up so that it does that for us. 
#     We can set up a relationship (it is a construct in SQL Alchemy) which tells sql alchemy to automatically fetch some information based 
#     off the relationship."""

# """ QUERY PARAMETERS 
#     When we expand a URL in the search bar we see the domain name, the endpint we are going to hit and everything after the '?' mark is
#     known as the query parameters. This is an optional (key, value) pair that allow us to filter the result of a request.
#     1. So we will go to the get_posts router and we want to allow for the users to be able to filter down on the post that they want to see.
#     2. We want to allow them to specify how many posts the user wants to see, 10,20 or 50.
#     3. To allow a query parameter we could just go into our path operation functions and just pass in another argument (Limit:int = 10)
#         10 here is the default value.
#     4. To send the query parameter just type a '?' in the url then the name of the query parameter i.e. limit = 3.
# """
# """ Next we should make the skip functionality which allows the user to skip some of the results in the query result. Maybe we wanted to skip
#     the first two results. Then we should be able to put another query argument called as skip in the path operation function.
#     This would allow us to implement the pagination on the front end because the front end should be able to skip results depending upon the
#     page that we are on. """

# """ The last query parameter that we are going to implement is the search functionality. 
#     The search query parameter would allow us to provide some string and it would search the entire title of the post and it would see if the 
#     search keywords are anywhere in the post title. It makes us easy so that we could provide some keywords like beaches, etc and it would
#     filter out the results."""
# """ USING SPACES IN A SEARCH QUERY 
#     As we can't use spaces in the URL so for search query what we can do is that we can add '%20' which represents space and send that in
#     the URL """

# """ Putting our passowrd in plain text in our database environment casues:
#     1. Compromises our application.
#     2. Right now the application is running on our local machine. When we actually deploy it in production our POSTGRES server will reside 
#      on other machine. So we would need our code to automatically update in our production environment to point to the actual production 
#      POSTGRES databse instead of using a hardcoded databse url. 
     
#     We also have our SECRET_KEY hardcoded so we need that to be secure.
#     WE WOULD NEED SOMETHING CALLLED AS ENVIRONMENT VARIABLES"""

# """ ENVIRONMENT VARIABLES 
#     Anything that needs to get updated based off on the environment that its in for e.g(Production/Development) such as URL's, passwords
#     and SECRET_KEYS etc which we don't want to expose and they can be different for different environments can be set as environment
#     variables.
#     This variable is just a variable that we configure on our computer. Any application thats running on that computer will be able to
#     access it, including our Fast_API and by extension our Python app will be able to access the E.V on the machine. So instead of 
#     hardcoding the varibale we will retrieve it through Python.
#     How to set Environment Variables on windows.
#     1. Search for environment variables. Goto Environment variables on the bottom right.
#     2. There are two types : a)System Variables: Can be used by anyone ; b) User Variables: Specific to the User
#     3. To acces a Path environment variable just type echo %Path% and it will display the Path EV.
    
#     4. To set a new EV goto new.
#     5. Type the variable name and value. In our e.g: variable_name:MY_DB_URL, variable_value: localhost:5432
#     6. Now try to access the variable in cmd by echo %MY_DB_URL% and you will see that it returns localhost:5432.
#     7. We wont be setting the individual environment variables manually because many complex applications have more than 20 EV's.
#     8. To get around setting all the environment manually we use what's called as an Environment File.
#     9. It would also be good to perform some sort of validation to ensure that all of the right EV's have been set for your application
#         to run properly.
#     10. When we read an EV its ouputted as a string. So we need to keep that in mind when performing validation. We can use Pydantic library
#         to perform validation like we do with schemas.
#     11. When you move to production we would just update the config.py file and set all of these values and it is going to automatically,
#         import it and set those values whereever we reference them.  """

# """ In our social media app there is going to be some sort of voting or likes system where:
#     1. Users should be able to like a post.
#     2. Users should be able to like a post only once.
#     3. Retrieving posts should also fetch the number of likes.

#     VOTE MODEL
#     1. Just like we have a table for users and a table for posts we should also have a table for posts and there likes with the users also.
#     2. Column referencing the post id.
#     3. Column referencing the id of the user who liked the post.
#     4. A user should only be able to like the post once, so we need to ensure that every (post_id-user_id) combonation is unique """
    
# """THIS REQUIRES US TO HAVE A CONCEPT OF COMPOSITE KEYS
#     Composite keys : It is a primary key that can span multiple columns. Since primary keys must be unique this will ensure that no user 
#     can like a post twice.
#     When you have a composite primary key, it does not care if it has duplicates in one row and it does not care of ot has duplicates in 
#     one column. It only cares of if the combination is not duplicated in any row."""

# """ We would have another path when it comes to the voting functionality.
#     1. The Path would be '/vote'.
#     2. The user id will be extracted from the JWT token.
#     3. The body would contain the id of the post the user is voting on as well as the direction of the vote.
#         {
#             post_id: 45
#             vote_dir: 0
#         }
#     4. A vote direction of 1 means we want to add the vote and a direction of 0 means we want to delete a vote.  """



# """ Automatically returning the number of likes on a post would require a more in depth knowledge of SQL because of the way we have built 
#     these relationships, so a lot of the time we would need information from two tables simultaneously. We do this by joining two tables
#     at a time by using a JOIN.
#     EG: SELECT posts.*, email FROM POSTS LEFT JOIN users ON posts.owner_id = users.id
    
#     The direction tells us which table for e.g LEFT is always the first table referenced and the RIGHT is always the second table.


#     We would need to do joins in SQL Alchemy because we are not writing queries.
#     By default the join in SQL Alchemy is the left inner join.
#     And we would have to create a new response schema because the ouput of the query breaks our current schema validation .
#     So we will have to include votes in our current schema validation code.  

#     """


# """ SQL alchemy does not allow us to update the databse table schemas becuase it searches the databse for a tablename and if it finds one
#     it does not modify it and simply skips that table. If it doesn't find a tablename then only it creates the table with the specific
#     schema.  So what we did till now is that we were deleting the tables and remaking them from scratch when we wanted to update them.

#     But that would be a foolish thing to do when we are in a production environment.

#     SO a databse migration tool like 'ALEMBIC' would allow us to :
#     1. Update the columns in our postgres databse based on the models that we define in our models.py file.
#     2. Its able to allow us to do incremental changes to our database and actually track it like GIT and rollback changes at any point in time.
#     3. Alembic can also automatically pull database models from SQLalchemy and generate the proper tables.


#     DATABASE MIGRATION TOOL ALEMBIC
#     1. First we need to initalize alembic and what we do is that we type 'alembic init <foldername>' in the command prompt which creates up
#        a folder and also creates a alembic.ini file. 
#     2. In the alembic folder it has what is called a env.py file which is like the main configuration file.
#     3. There will be a couple of things that we need to add in this file to make sure that the things work correctly.
#     4. Because alembic works with the models of sqlalchemy we need to make sure that it has access to the BASE OBJECT i.e Base = declarative_base()
#        and we would want to set the target_metadata = Base.metadat and the Base is imported from app.database.py file.

#     5. The next thing we have to do in the file 'alembic.ini' and what we nedd to do is to pass the sqlalchemy url to access our postgres databse.
#     6. But for that we would need to hardcode the sqlalchemy.url and we dont want to have our password hardcoded. So what we will do is that
#         we will override the 'sqlalchemy.url' option in the alembic.ini file from the env.py file by 'config.set_main_option("sqlalchemy.url")'
#         and providing the required fields from the Settings object from our Config file (from app.config import Settings), which is a pydantic class
#         which will validate and input settings from our environment variables to the sqlalchemy url.

#     """

# """ 1. Now we will create all our tables in the way that we knew about alembic  when we first started with our project to see how we would have done 
#         it if we  had known about alembic in the first place.
#     2. So what we will do is we wil do alembic --help just to see the commands that we would have.
#     3. First we will use the 'revision' command . First when we want to make a change to our databse we do a revision command. The revision is
#         what really tracks the changes that we make on a step by step basis.
#         1. The only one imortant for now is '-m' flag in the revision --help, which helps us kind of have a human readable name with each association.
#         2. As soon as you write (alembic revision -m "create post table") which would add a message to the post table you will see a versions folder
#             pop up which contains all of our changes.
#         3. If we take a look at the revisions file we can see that  it imports op from alembic library and sqlalchemy as 'sa', and it has two functions
#             as upgrade and downgrade functions which are empty at the moment. These functions are pretty important and what they do is that they run
#             the commands when we are making the changes that we wanna do. So in this case we wanna create the post table, so we are going to put all 
#             the logic in the upgrade function and if we ever wanna rollback the table then what we are going to do is put all the logic in the
#             downgrade function to handle removing the table but its all manual.
#     4. So we have set up the logic in the upgrade and the downgrade function using alembic abd sqlalchemy. Now what we need to do is go to the 
#         command propmpt and type alembic upgrade --help where we see that we have to provide a revision number to tell it what revision we want
#         to go to. The revision number is in the revision.py file created in versions and we will type (alembic upgrade <revison Number>) and we 
#         would do the operation.
#     5. The above operation creates two tables in the databse. One is the post table and the other is the alembic versions table which keeps track
#         the revison id of the changes.
#     6. Lets say that we are building our application and we want to add a brand new column to our database. 
#         We can type alembic revision -m "add content colum to post table" and its gonna do a brand new revision for us and we have to add the logic
#         for upgrade and downgrade. There is also a variable named down_revision so if we want to go down a step we can see that it would go down to 
#         the revision of the previous one.

#         1. alembic current --> give us the id of the current revision number
#         2. alembic heads --> Gives us the latest revision number in the head variable. So we can do (alembic upgrade <revision Num>)
#              or we can do (alembic upgrade head)
#         3. alembic downlgrade <down_revison number> --> downgrades the revision of the revision number provided.
#             We can also say alembic downgrade -1 and it will go back to one revision earlier and -2 goes back 2 revisions earlier.
#         4. alembic history --> It gets the history of our revisions.

#     7. So we got out posts table now the next finctionality was a users table.
#     8. Now we did the users table and now we need to set up the foreign keys of the tables. For that we would create another revision.
#         1. First of all we have to add column to our posts table called as user_id and that is goin to be the one with the foreign key.
#         2. Then we would need to add the foreign key by the alembic upgrade heads.
#     9. Lets implement all of the columns we had in our post table
#     10. If we want to roll back all the way to when we created our posts table we can do (alembic dowgrade <revision number>).
#     11. The last thing we have to do now is to genrate the votes table. But we won't create it manually this time. We would use the 
#         auto-generate tool provided by alembic.
#         1. So what alembic can also do is that it looks at our models and check if the thing exists in our database tables or not and if it 
#             does not it can create the table with the auto-generate tool. It can also figure out what columns are extra between the SQL ALchemy's
#             models and the postgres database and delete them and also add few other columns and make the changes for us. The reason we ca do that
#             we imported the Base object from app.models file and then we passed it into  'target_metadata'.
#         2. So what we can do is that we pass in alembic's revision function and with the flags of --autogenerate.
#             The command is ---> (alembic revision --autogenerate -m "auto genrated votes tables").
#             This would auto-generate the votes table with the revision file in the versions folder.
#             To make the changes in database --> alembic upgrade head, would make the tables in the database.

#     12. This provides us with the convenience of making changes in a very easy way such that we can modify the tables in models file and 
#         we can just invoke the revision command of alembic and make the changes.

# """

# """ CORS POLICY

#     So far we have been sending requests from POSTMAN but it is important to know that POSTMAN sends API requests from our computer. But in the 
#     real world we send requests from a number of different devices. It can be sent from mobile devices and most importantly it is being sent 
#     from web browsers. So when a web browser sends a request using the JAVASCRIPTS fetch() API there is gonna be a slightly different behaviour
#     which we have to account for which we cant take into consideration when taking in requests from postman because POSTMAN is not a web browser.
    
#     Now we will se what happens when we send a request from the web browser.
#     1. Go to google.com and click on inspect element by right clicking on the page. Now go to the console and it can be used to send requests.
#     2. Now type 'fetch('http://localhost:8000').then(res => res.json()).then(console.log)' in the space provided.
#     3. What this does is that it is sending a request to the root url of our API and then its gonna print out the contents of whatever we get
#     back form the server.
#     4. When executing the above command we get (Access to fetch at 'http://localhost:8000/' from origin 'https://www.google.com'
#         has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
#         If an opaque response serves your needs, set the request's mode to 'no-cors' to fetch the resource with CORS disabled.)
#     5. But why is it that we cannot send in requests from the web browser but we can send reequests from POSTMAN. It has to do with this
#         CORS POLICY.
    
#     6. CORS is the short form for CROSS ORIGIN RESOURCE SHARING(CORS) allows you to make requests from a web browser on one domain to a server
#         on a different domain.
#         By default our API will only allow web browsers running on the same domain as our server to make requests to it. It will be blocked by CORS.
#         So if our API is hosted on google.com and our website is hosted on ebay.com then we cannot send requests from ebay.com to google.com.

#         But if we try to send requests from localhost:8000 to our API which is hosted on localhost:8000 then it wont be blocked and we will get a
#         response back.


#         To fix this if we want people from other domains to talk to our API  we would go to FAST_API documentation and go to the CORS and import.
#         ---> from fastapi.middleware.cors import CORSMiddleware
#         ---> Then add   origins = []   # The domains which can talk to our API.
#                         # If you want to set a public API so that you can get requests from every domain the just set origins = ["*"]
#                         app.add_middleware(
#                         CORSMiddleware,
#                         allow_origins =  origins,    # Allow the domains in the origins list
#                         allow_credentials  = True,
#                         allow_methods=["*"],        # We can also allow specific http mehtods. If were building a public API we may not to allow them to have post or put or delete http methods.
#                         allow_headers=["*"] )        # We can allow specific headers as well


#         So this is technically a 'middleware' is a term that is used in most of the web frameworks to refer to a function that runs before every
#         every request. So if someone sends a request to all our apps, before it gets sent to the routers it goes through the middleware and our
#         middleware can perform some sort of operation. But what we want to is to specify the origins of what domains we wanna allow. So what
#         domains should be able to talk to our API and we would just put them in a list called as origins.
# """

# """ NOW WE WILL SET UP GIT TO KEEP TRACK OF OUR CHANGES AND TO STORE OUR CODE IN A REPOSITORY.
#      It would make the whole deployment  process a whole lot easier. But when check our files into git, by default it would check all the files.
#      There will be some files which we dont want to check into the repository. So what we will do is that we will create a 'gitignore' file
     
#      But we would run into an issue because if someone clones our repository he would not be able to see what libraries to install.
#      And which other packages and dependencies to install for our application to actually work.

#      What we would do is that we would create a requirements.txt file and we would pass in the output of pip freeze which would pass
#      in all the installed libraries with their specific versions into the requirements.txt file
#                 pip freeze > requirements.txt  
#     So now anyone can look into our requirements.txt file and install the dependencies for our application by :
#                 pip install -r requirements.txt

#     Next we would set up and install git
#     After installation do:
#         1. Type (git init) in the terminal in VS Code and make sure you are in the root directory of your project.
#             This will initialize git in your project and add a git folder in your directory.
#         2. Now skip git add readme.md
#         3. Now we will run (git add --all). This will add all of our files of the directory into the repository.
#         4. Now run (git commit -m "Initial commot"), to commit and finalize the changes to the repository.
#         5. Now run (git branch -M master) to set what our branch is. This would set our branch to be called as master
#         6. Then we would have to set up a remote branch. This is whats gonna allow us to store all of our code to github.
#             (git remote add origin https://github.com/anantinfinity9796/example-Fastapi.)
#         7. Finally push the code to the github repository by (git push -u origin master)
#         8. Finally the code is sent to the repository and we can verify that by going to github.

#      """


# """ Next we will move on to deploying our application.
#     There will be two deployment methods that we will learn in this course.
#         1. We will deploy our application to a platform called as Heroku. It would give anyone access to our API.
#         2. Create an account on the heroku platform. Its free.
#         3. Now we would nedd the Heroku CLI to be installed on our computer. Download the installer and run it.
#         4. After you have installed heroku then usually we have to close the pre existing terminals and open again to access heroku.
#         5. Now check the version of heroku installed in (heroku --version).
#         6. Then login to the heroku by typing (heroku login)
#         7. The heroku documents give us a demo app to follow along but we have our own app.

#         8. We have to run the command (heroku create) to create and app wthin our heroku account. heroku create --help gives us all
#             the arguments to the options we have when creating the app.
#         9. We can day (heroku create <app name>)  to create our app and what we also need to know is that app names are global i.e
#             if we create and app with a name, another user around the globe cannot create an app of the same name.
#             The links are : https://fastapi-anant.herokuapp.com/ | https://git.heroku.com/fastapi-anant.git
#         10. If we type in git remote it is gonna show all of the remotes that have been set up for our git. There two now : origin and
#             heroku. So instead of using (git push origin master) to push it out to github we can just do (git push heroku master) and
#             its gonna push out to our heroku platform and then it will then create an instance for our application and install all of
#             the dependencies and deploy the application.
#         11. In the output what it will do is that it would provide the URL of the application : https://fastapi-anant.herokuapp.com/
#             For now this would give out an error which states that something in our application is broken and this is to be expected
#             because we have to do somethings before the app starts working. 
#         12. If take a look at what we have done is that we have pushed our app to heroku, but heroku does not know how to actually 
#             start our application. It does not know what commands to use, it only knows that it is a python app. When we ran it in 
#             our development environment we ran (uvicorn app.main:app --reload) to start the application but we havent given the 
#             command to heroku yet.
#         13. So what we have to do is that we have to create a file that is gonna tell heroku what is the exact command that we wanna
#             run. So inside your root directory create a file called as 'Procfile'.

#         14. The Procfile is just a file with the command that tells Heroku what is the command that we need to do start the application.
#             We can give it a process type and since it is a web application it will be responding to web requests we would use

#             web: uvicorn app.main:app --host=0.0.0.0 --port=${port:-5000}

#             we are not gonna pass in uvicorn app.main:app --reload because we dont want the app to be reloaded on changes because this is production.
#             There should be no changes in the application because it is in production.

#              We do have to provide the host ip (--host=0.0.0.0), This is just saying that we should be able to respond to request to any IP.
#              So whatever IP heroku gives us this is going to accept it.
#              Next is the port flag (--port=${port:-5000}) which would run the app on the port provided. If nor specified it runs on default port.
#              However in heroku they are actually going to provide us a port. So we dont know what this port is ahead of time but we have to accept it regardless.
#              Its actually going to pass it as an environement variable. So anytime we want to accept an EV we do (${PORT}. default is 5000).

#         15. Then we are gonna have to push out these changes once again using 
#                 git add --all
#                 git commit -m "added Procfile"
#                 git push origin master 
#         16. Then to push the changes to the Heroku app do  (git push heroku master)
#         17. Anytime the heroku app is not working they have a very easy way of accessing logs (heroku logs --tail). This would tail
#             the logs as they happen.
#         18. There is some error in our app because it needs the Environment Variables and it was not checked into git. So heroku does
#             not know how to put the environment variables and we would do that either to the command line or through the dashboard.
#         19. Heroku provides us with a free postgres instance that we can access:
#             type heroku addons:create heroku-postgresql:<PLAN NAME> we have the PLAN NAME as 'hobby-dev'. This would start a heroku 
#             postgres database instance in the cloud and it will get displayed on the dashboard and we can click on the databse and
#             go to the settings and go and see the database credential. Heroku does not let us create our own databse and passwords,
#             rather they give us their own database and passwords. And they also provide us the full postgres url if we wnat it.
#         20. Heroku calls its instances as dynos.
#         21. Config VARS in settings is the place we provide the environment variables to our heroku instance. There should be only
#             one config variables. When you add your postgres instance to the heroku app, heroku adds up only one EV and that is
#             databse_url and its going to contain the entire postgres URL. We could go into our application and code it up to put the 
#             URL in our code but instead of putting this EV in our code directly we could break down  this url into multiple EV's. 
#             Now see what the EV's are in config.py and set it in the settings-->Config VARS in the heroku dashboard.
#             After doing this our app shoud work and we will try this out again.
#             We cant use the app argument ot restart the app because it does not have a restart flag.
#             On doing heroku ps --help we see that it has the restart option. So we do (heroku ps:restart) which is going to restart 
#             our dyno heroku instance.
#             Then we will do (heroku logs -tail to tail the logs).
#         22. # The Procfile is just a file with the command that tells Heroku what is the command that we need to do start the application.
# # We can give it a process type and since it is a web application it will be responding to web requests we would use
# # web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-5000}

# # we are not gonna pass in uvicorn app.main:app --reload because we dont want the app to be reloaded on changes because this is production.
# # There should be no changes in the application because it is in production.

# # We do have to provide the host ip (--host=0.0.0.0), This is just saying that we should be able to respond to request to any IP.
# # So whatever IP heroku gives us this is going to accept it.
# # Next is the port flag (--port=${port:-5000}) which would run the app on the port provided. If nor specified it runs on default port.
# # However in heroku they are actually going to provide us a port. So we dont know what this port is ahead of time but we have to accept it regardless.
# # Its actually going to pass it as an environement variable. So anytime we want to accept an EV we do (${PORT}. default is 5000).
        
# """