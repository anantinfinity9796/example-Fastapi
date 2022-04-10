
To control the content of the post that the user submits we need to define a schema for the posts. Pydantic can be used for this....
POST --->   title:str, content:str,category, published or draft :True/False.


""" A CRUD application is the one that need to create, read, update, delete the data.

Best Practices for designing an API of a CRUD based application:

    1. When it comes to naming a URL there are conventions one needs to follow:
        1. Since we are working with posts it makes sense to name all the URL's with  " /posts " :
            a. CREATE --> @app.post("/posts")

            b. READ   --> @app.get(" /posts/{id} ")
                      --> @app.get(" /posts")

            c. UPDATE --> @app.put(" /posts/{id}")     # For put we need to pass values for all the fields
                      --> @app.patch(" /posts/{id} ")  # for patch we can just update a specific field.
            
            d. DELETE --> @app.delete(" /posts/{id} ") 
    
    # Above we did not follow the best practice and named the creating post url as "/create_posts" but it should be "/posts" only.
    """


""" For now we just creating the posts and returning the data back to the user. Now we would need to save the posts somewhere also."""
""" Typically we use a database to save the posts but now we would just use a global variable to save them which is defined at the start"""


""" Typically when a task gets compelted or an Error occurs in fetching the API we get a Status Code like:
    1. 200 : Evrything is Working fine
    2. 404 : Resource not found , etc
So far our API does not return these kind of responses. So we need to make sure that our API returns these responses to the user
For that we would need to add a "response" object in out API functions which returns the appropriate response to the user upon
executing a task. For this we need to import the response into our code from FAST_API and then we would be able to add it

"""




""" As we are working with posts in our API and our choice of database is a relational database then we need to figure out the 
    columns of our database:
    1. title: As a post will have a title which will be a string.
    2. content: A post will have some content which would be of type string.
    3. id : unique --> The id will be a unique integer 
    4. published : Boolean
    5. Created_at : timestamp"""

""" To work with a postgres database with a python application we need to have a POSTGRES driver so we need to install a library
known as " psycopg ". It is the most widely used library for postgres connections """



""" When working with databases in python or any other language code we can pass SQL queries directly as statements to our
        programming languages driver which can be executed by the driver on the database.
        
        But this has a problem that the programmer should have good knowldge of SQL to run queries
        
        
        An OBJECT RELATIONAL MAPPER (ORM) solves the aforementioned problem as it sits between the databse and US . 
        We can perform the execution of all traditional SQL queries without writing SQL code just through Python.
        
        SQL Alchemy is the most popular standalone ORM's that is the most widely used in Python community.
        It can be used with other web frameworks or any python based application.
        
        But one thing we need to keep in our mind is that SQL Alchemy cannot talk to any database on its own i.e it does not have
        support for database drivers. So we will need to install a Database driver for our respective databses such a psycopg2 for
        POSTGRES database. Ultimately the driver will talk with the database and SLQ Alchemy just helps with the queries. """



""" Some things that an ORM allows us to do
    1. Make our database tables as Python Models.
    2. Queries can be made exclusively through Python codes """


""" We should not save string representations of the passwords in our databases instead we should save the hashes of the passwords
    The passwords are impossible to reverse engineer from the hash."""



""" We can see that we have path operations for CRUD operations for working with posts, and path operations for working with users.
    But the main file is getting very cluttered and as we keep adding more and more operatiosn it becomes unmanageable.
    So we break it out into two files.
    1. For all of the routes or path operations that work and deal with Posts.
    2. For all of the path opeartion that work with Users. 
    
    This involves something called as 'ROUTERS' and it is not specific to Fast_API and all the frameworks have some sort of
        system in place for tackling this problem. 'ROUTERS' help split up our path opertions so that we can organize our
        code better. """


""" The most important part of any application is the way it handles authentication.
    There are really two main ways to handle authentication.
        1. Session Based Authentication - We store something on our backend server/ API to track whether our user is logged in.
        2. Using JWT token base Autentication - This is stateless i.e. there is nothing on our server that tracks whether a 
                user is logged in or not. The token itself is stored on the frontend and our client actualy keeps track whether our
                user is logged in or not.
        """
""" The Flow for JWT Authentication token for logging in and accesses a specific endpoint for JWT authentication:
    1. The client or the frontend would try and log in with the path operation ('/login') with there credentials.
    2. We will verify if the credentials are valid. Then we would create the JWT token(its like a string).
    3. The token would be sent as a response back to the client.
    4. Now he can start accessing resources that require authentication.
    5. So lets say that he wants to see the posts. He would send a request to the ('/posts') endpoint but he would also send the {token} in the header of the request.
    6. The API will verify if the token is valid with some mechanism. If it is then it just sends back the data. 
    7. So the API does not have to store anything on the backend. All is given by the client and API just does the verification. """

""" The basics of a JWT token. What exactly is it.
        1. A JWT looks like a bunch of cryptic chracters jammed together but it is not encrypted.
        2. It consists of 3 parts:

            1. Header - It includes metadata about the token. It contains the algorithm used for hashing and the type = 'JWT'.
                    It is fixed for all the tokens.

            2. Payload - This is upto the user. Any piece of information can be sent within the payload but as the token is not 
                    encrypted sensitive information should not be sent by the payload. So common things are: the user_id when 
                    logging in, the users role: priviledge user or not. Jamming a lot of info would increase the size.

            3. Signature : It is a combination of 3 things : 
                            1. Header - the header provided above
                            2. Payload - the payload of the token
                            3. Secret - This is the most important thing. It is like a kind of a password stored that is kept on our
                                API. It's only there and no one else would know it. We would take the above 3 things and pass it to
                                the algorithm and it would return us the Signature which is used to determine if the token is valid
                                and no one else has tampered with it.
"""

""" PURPOSE OF THE SIGNATURE 
    1. Lets say that a user has sent his/her credentials and the API is in the process of sending back the token.
    2. The token has the same 3 things that are discussed above: 
        i. Header
        ii. Role : user(not a priviledged user)
        iii. Signature : We take the header, payload and the secret and pass it to a hashing functions and we make a signature and 
                pass it back to the toekn and then to the user.
    3. Lets say a user decides to do a shady thing and the user decides to change the token by a little and changes a few bits in the token
        and changes the role form user to admin. But he could have changed anything. But he cannot do anythin because the signature
        that was generated with the token was generated for the role:user, so its no longer valid, so he will have to create a brand
        new signature to match the data he is sending. However he cant create the signature because he doesn't have the supe secret password
        which only resides on our API.
    4. Lets say the user does send a token with a artificial signature to the API. What the API does is that he takes the Header, Payload and the
        SECRET  pasword stored in the API and creates a TEST SIGNATURE and then compares them and the tokens do not match.
    5. Thats why the SECRET PASSWORD is so important because it ensure that no other token can be generated by anyone else. """

""" Lets discuss how we are going to handle logging of the user. Specifically how we are going to verify if the credentials are correct.

    1. The user is going to hit the LOGIN endpoint with his [email + password(in plain text)]. When that happens we are going to search the databse
        to try to find the user based of his username and email and the databse is going to send all the data back including the password(hashed).
        But how exactly we compare the hashed password from the database with the plain text password provided by the user because the hashed password 
        cannot be converted to the plain text. So we take the plain text password and hash it again and then compare them and then we see if they are equal.
    2. If the password is correct then the token is generated and returned.
"""
""" First we will need to install a library that helps install signing and verifying JWT tokens : Python-jose
"""


""" We would also need to verify in our application if the token has not expired. So we will set up a schema in the schema file."""

""" Anytime we have a specific endpoint that should be protected i.e the user needs to be logged in to use it. What we are gonna do it that 
we can add an extra dependency in the path operation function  (get_current_user: int = Depends(oauth2.get_current_user)). So anytime anyone
wants to access a resource that reuires them to be logged in we expect them to provide and access token and then provide them with dependency
 which is going to call the function get_current_user and then we pass in the token that comes from the request and then we are going to run the 
 verify_access_token  which verifies that the token is okay. If there is no errors then the user is successfully authenticated """



""" Now we are going to look at some of the more advanced features of Postman starting off with Environments
    --> An environment is a set of variables that allows you to switch the context of your requests.
    If we look at all our postman requests we can see that we have hardcoded it to 127.0.0.1:8000. And if we deploy our app, its 
    not gonna be deployed on the localhost. It's gonna be deployed on some public IP somewhere on the internet. So when we would test out our
    production server  or make some test request to it we would have to change everything in our requests and continuously flip back and form 
    development to production and back.

    So to circumvent the above problem and avoid hard coding these values we would define a variable that changes depending on what environment
     we use within postman. 
"""

"""Now that we have built authentication in our API, testting out API has got a little more challenging as the user has to be authenticated
before we do anything which is very cumbersome. Luckily Postman can automate this task of authenticating the user with the help of environment
variables.
1. Generate a new access token by logging in the user. Go to test in options. There is an example snippet of set environment variables
    The snippet is :--> pm.environment.set("variable_key", "variable_value");
    Which transforms to --> pm.environment.set("JWT", pm.response.json().access_token); this would be the code to set up the environment variables
    variable_key : JWT
    variable_value : This is the value of the bearer token which is in the pm.response.json().access_token. This would automatically take the authentication
    JWT token and pass it to the environement variable as soon as a new user authenticated himself by providing the credentials.
2. Then go to the request you want to send. Go to the Authorization tab, select Bearer Token from the drop down menu and set {{JWT}} as the token value
    instead of the original JWT string. This would automatically pass the string to the required field and we won't need to input it everytime.
3. So anytime we log in a user its going to update the variable.

"""


""" Relationships of the Posts table and users table.
    1. In our application there is nothing that ties a post to the users that created it.
    2. So we need to set up some kind of a special relationship between the users and the posts table which allows us to relate
        both the tables together.
    3. The way we do that is that we create an extra column in both the tables. An we are going to set up a foreign key.
    4. we tell  SQL how a column in a table is connected to other table by the help of a foreign key.
    5. We specify two things : Table that its connected to (users table) and column that it is connected to (id column).
        5.1. The data types of both the columns need to match.
    6. Then whichever user creates this post we just embed the id of that specific user in the user_id column in the posts table.
    7. Thats all we have to do to create a relationship between tables.
    8. The above is referred to as a ONE TO MANY RELATIONSHIP in a SQL databse because ONE user can have MANY posts which he created.
    9. However a post can only be created by one user."""

""" We are going to use SQL Alchemy to generate all the tables and provide all the foreign keys as well.
    So we would define them in the models.py file as we have been doing so."""

""" currently we have the authentication set up for a user to login and create posts. We do not have any logic set up to prevent a user
    when he is deleting someone elses posts. So we need to implement that also."""


""" One thing that we need to do is that we need to send in some additional information in the response of when creating a post. Because 
    instead of displaying the owner id of the user we would need to display the Name or the user_id of the user like it gets displayed in
    twitter and other social media apps. In sqlalchemy we can actually set it up so that it does that for us. 
    We can set up a relationship (it is a construct in SQL Alchemy) which tells sql alchemy to automatically fetch some information based 
    off the relationship."""

""" QUERY PARAMETERS 
    When we expand a URL in the search bar we see the domain name, the endpint we are going to hit and everything after the '?' mark is
    known as the query parameters. This is an optional (key, value) pair that allow us to filter the result of a request.
    1. So we will go to the get_posts router and we want to allow for the users to be able to filter down on the post that they want to see.
    2. We want to allow them to specify how many posts the user wants to see, 10,20 or 50.
    3. To allow a query parameter we could just go into our path operation functions and just pass in another argument (Limit:int = 10)
        10 here is the default value.
    4. To send the query parameter just type a '?' in the url then the name of the query parameter i.e. limit = 3.
"""
""" Next we should make the skip functionality which allows the user to skip some of the results in the query result. Maybe we wanted to skip
    the first two results. Then we should be able to put another query argument called as skip in the path operation function.
    This would allow us to implement the pagination on the front end because the front end should be able to skip results depending upon the
    page that we are on. """

""" The last query parameter that we are going to implement is the search functionality. 
    The search query parameter would allow us to provide some string and it would search the entire title of the post and it would see if the 
    search keywords are anywhere in the post title. It makes us easy so that we could provide some keywords like beaches, etc and it would
    filter out the results."""
""" USING SPACES IN A SEARCH QUERY 
    As we can't use spaces in the URL so for search query what we can do is that we can add '%20' which represents space and send that in
    the URL """

""" Putting our passowrd in plain text in our database environment casues:
    1. Compromises our application.
    2. Right now the application is running on our local machine. When we actually deploy it in production our POSTGRES server will reside 
     on other machine. So we would need our code to automatically update in our production environment to point to the actual production 
     POSTGRES databse instead of using a hardcoded databse url. 
     
    We also have our SECRET_KEY hardcoded so we need that to be secure.
    WE WOULD NEED SOMETHING CALLLED AS ENVIRONMENT VARIABLES"""

""" ENVIRONMENT VARIABLES 
    Anything that needs to get updated based off on the environment that its in for e.g(Production/Development) such as URL's, passwords
    and SECRET_KEYS etc which we don't want to expose and they can be different for different environments can be set as environment
    variables.
    This variable is just a variable that we configure on our computer. Any application thats running on that computer will be able to
    access it, including our Fast_API and by extension our Python app will be able to access the E.V on the machine. So instead of 
    hardcoding the varibale we will retrieve it through Python.
    How to set Environment Variables on windows.
    1. Search for environment variables. Goto Environment variables on the bottom right.
    2. There are two types : a)System Variables: Can be used by anyone ; b) User Variables: Specific to the User
    3. To acces a Path environment variable just type echo %Path% and it will display the Path EV.
    
    4. To set a new EV goto new.
    5. Type the variable name and value. In our e.g: variable_name:MY_DB_URL, variable_value: localhost:5432
    6. Now try to access the variable in cmd by echo %MY_DB_URL% and you will see that it returns localhost:5432.
    7. We wont be setting the individual environment variables manually because many complex applications have more than 20 EV's.
    8. To get around setting all the environment manually we use what's called as an Environment File.
    9. It would also be good to perform some sort of validation to ensure that all of the right EV's have been set for your application
        to run properly.
    10. When we read an EV its ouputted as a string. So we need to keep that in mind when performing validation. We can use Pydantic library
        to perform validation like we do with schemas.
    11. When you move to production we would just update the config.py file and set all of these values and it is going to automatically,
        import it and set those values whereever we reference them.  """

""" In our social media app there is going to be some sort of voting or likes system where:
    1. Users should be able to like a post.
    2. Users should be able to like a post only once.
    3. Retrieving posts should also fetch the number of likes.

    VOTE MODEL
    1. Just like we have a table for users and a table for posts we should also have a table for posts and there likes with the users also.
    2. Column referencing the post id.
    3. Column referencing the id of the user who liked the post.
    4. A user should only be able to like the post once, so we need to ensure that every (post_id-user_id) combonation is unique """
    
"""THIS REQUIRES US TO HAVE A CONCEPT OF COMPOSITE KEYS
    Composite keys : It is a primary key that can span multiple columns. Since primary keys must be unique this will ensure that no user 
    can like a post twice.
    When you have a composite primary key, it does not care if it has duplicates in one row and it does not care of ot has duplicates in 
    one column. It only cares of if the combination is not duplicated in any row."""

""" We would have another path when it comes to the voting functionality.
    1. The Path would be '/vote'.
    2. The user id will be extracted from the JWT token.
    3. The body would contain the id of the post the user is voting on as well as the direction of the vote.
        {
            post_id: 45
            vote_dir: 0
        }
    4. A vote direction of 1 means we want to add the vote and a direction of 0 means we want to delete a vote.  """



""" Automatically returning the number of likes on a post would require a more in depth knowledge of SQL because of the way we have built 
    these relationships, so a lot of the time we would need information from two tables simultaneously. We do this by joining two tables
    at a time by using a JOIN.
    EG: SELECT posts.*, email FROM POSTS LEFT JOIN users ON posts.owner_id = users.id
    
    The direction tells us which table for e.g LEFT is always the first table referenced and the RIGHT is always the second table.


    We would need to do joins in SQL Alchemy because we are not writing queries.
    By default the join in SQL Alchemy is the left inner join.
    And we would have to create a new response schema because the ouput of the query breaks our current schema validation .
    So we will have to include votes in our current schema validation code.  

    """


""" SQL alchemy does not allow us to update the databse table schemas becuase it searches the databse for a tablename and if it finds one
    it does not modify it and simply skips that table. If it doesn't find a tablename then only it creates the table with the specific
    schema.  So what we did till now is that we were deleting the tables and remaking them from scratch when we wanted to update them.

    But that would be a foolish thing to do when we are in a production environment.

    SO a databse migration tool like 'ALEMBIC' would allow us to :
    1. Update the columns in our postgres databse based on the models that we define in our models.py file.
    2. Its able to allow us to do incremental changes to our database and actually track it like GIT and rollback changes at any point in time.
    3. Alembic can also automatically pull database models from SQLalchemy and generate the proper tables.


    DATABASE MIGRATION TOOL ALEMBIC
    1. First we need to initalize alembic and what we do is that we type 'alembic init <foldername>' in the command prompt which creates up
       a folder and also creates a alembic.ini file. 
    2. In the alembic folder it has what is called a env.py file which is like the main configuration file.
    3. There will be a couple of things that we need to add in this file to make sure that the things work correctly.
    4. Because alembic works with the models of sqlalchemy we need to make sure that it has access to the BASE OBJECT i.e Base = declarative_base()
       and we would want to set the target_metadata = Base.metadat and the Base is imported from app.database.py file.

    5. The next thing we have to do in the file 'alembic.ini' and what we nedd to do is to pass the sqlalchemy url to access our postgres databse.
    6. But for that we would need to hardcode the sqlalchemy.url and we dont want to have our password hardcoded. So what we will do is that
        we will override the 'sqlalchemy.url' option in the alembic.ini file from the env.py file by 'config.set_main_option("sqlalchemy.url")'
        and providing the required fields from the Settings object from our Config file (from app.config import Settings), which is a pydantic class
        which will validate and input settings from our environment variables to the sqlalchemy url.

    """

""" 1. Now we will create all our tables in the way that we knew about alembic  when we first started with our project to see how we would have done 
        it if we  had known about alembic in the first place.
    2. So what we will do is we wil do alembic --help just to see the commands that we would have.
    3. First we will use the 'revision' command . First when we want to make a change to our databse we do a revision command. The revision is
        what really tracks the changes that we make on a step by step basis.
        1. The only one imortant for now is '-m' flag in the revision --help, which helps us kind of have a human readable name with each association.
        2. As soon as you write (alembic revision -m "create post table") which would add a message to the post table you will see a versions folder
            pop up which contains all of our changes.
        3. If we take a look at the revisions file we can see that  it imports op from alembic library and sqlalchemy as 'sa', and it has two functions
            as upgrade and downgrade functions which are empty at the moment. These functions are pretty important and what they do is that they run
            the commands when we are making the changes that we wanna do. So in this case we wanna create the post table, so we are going to put all 
            the logic in the upgrade function and if we ever wanna rollback the table then what we are going to do is put all the logic in the
            downgrade function to handle removing the table but its all manual.
    4. So we have set up the logic in the upgrade and the downgrade function using alembic abd sqlalchemy. Now what we need to do is go to the 
        command propmpt and type alembic upgrade --help where we see that we have to provide a revision number to tell it what revision we want
        to go to. The revision number is in the revision.py file created in versions and we will type (alembic upgrade <revison Number>) and we 
        would do the operation.
    5. The above operation creates two tables in the databse. One is the post table and the other is the alembic versions table which keeps track
        the revison id of the changes.
    6. Lets say that we are building our application and we want to add a brand new column to our database. 
        We can type alembic revision -m "add content colum to post table" and its gonna do a brand new revision for us and we have to add the logic
        for upgrade and downgrade. There is also a variable named down_revision so if we want to go down a step we can see that it would go down to 
        the revision of the previous one.

        1. alembic current --> give us the id of the current revision number
        2. alembic heads --> Gives us the latest revision number in the head variable. So we can do (alembic upgrade <revision Num>)
             or we can do (alembic upgrade head)
        3. alembic downlgrade <down_revison number> --> downgrades the revision of the revision number provided.
            We can also say alembic downgrade -1 and it will go back to one revision earlier and -2 goes back 2 revisions earlier.
        4. alembic history --> It gets the history of our revisions.

    7. So we got out posts table now the next finctionality was a users table.
    8. Now we did the users table and now we need to set up the foreign keys of the tables. For that we would create another revision.
        1. First of all we have to add column to our posts table called as user_id and that is goin to be the one with the foreign key.
        2. Then we would need to add the foreign key by the alembic upgrade heads.
    9. Lets implement all of the columns we had in our post table
    10. If we want to roll back all the way to when we created our posts table we can do (alembic dowgrade <revision number>).
    11. The last thing we have to do now is to genrate the votes table. But we won't create it manually this time. We would use the 
        auto-generate tool provided by alembic.
        1. So what alembic can also do is that it looks at our models and check if the thing exists in our database tables or not and if it 
            does not it can create the table with the auto-generate tool. It can also figure out what columns are extra between the SQL ALchemy's
            models and the postgres database and delete them and also add few other columns and make the changes for us. The reason we ca do that
            we imported the Base object from app.models file and then we passed it into  'target_metadata'.
        2. So what we can do is that we pass in alembic's revision function and with the flags of --autogenerate.
            The command is ---> (alembic revision --autogenerate -m "auto genrated votes tables").
            This would auto-generate the votes table with the revision file in the versions folder.
            To make the changes in database --> alembic upgrade head, would make the tables in the database.

    12. This provides us with the convenience of making changes in a very easy way such that we can modify the tables in models file and 
        we can just invoke the revision command of alembic and make the changes.

"""

""" CORS POLICY

    So far we have been sending requests from POSTMAN but it is important to know that POSTMAN sends API requests from our computer. But in the 
    real world we send requests from a number of different devices. It can be sent from mobile devices and most importantly it is being sent 
    from web browsers. So when a web browser sends a request using the JAVASCRIPTS fetch() API there is gonna be a slightly different behaviour
    which we have to account for which we cant take into consideration when taking in requests from postman because POSTMAN is not a web browser.
    
    Now we will se what happens when we send a request from the web browser.
    1. Go to google.com and click on inspect element by right clicking on the page. Now go to the console and it can be used to send requests.
    2. Now type 'fetch('http://localhost:8000').then(res => res.json()).then(console.log)' in the space provided.
    3. What this does is that it is sending a request to the root url of our API and then its gonna print out the contents of whatever we get
    back form the server.
    4. When executing the above command we get (Access to fetch at 'http://localhost:8000/' from origin 'https://www.google.com'
        has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
        If an opaque response serves your needs, set the request's mode to 'no-cors' to fetch the resource with CORS disabled.)
    5. But why is it that we cannot send in requests from the web browser but we can send reequests from POSTMAN. It has to do with this
        CORS POLICY.
    
    6. CORS is the short form for CROSS ORIGIN RESOURCE SHARING(CORS) allows you to make requests from a web browser on one domain to a server
        on a different domain.
        By default our API will only allow web browsers running on the same domain as our server to make requests to it. It will be blocked by CORS.
        So if our API is hosted on google.com and our website is hosted on ebay.com then we cannot send requests from ebay.com to google.com.

        But if we try to send requests from localhost:8000 to our API which is hosted on localhost:8000 then it wont be blocked and we will get a
        response back.


        To fix this if we want people from other domains to talk to our API  we would go to FAST_API documentation and go to the CORS and import.
        ---> from fastapi.middleware.cors import CORSMiddleware
        ---> Then add   origins = []   # The domains which can talk to our API.
                        # If you want to set a public API so that you can get requests from every domain the just set origins = ["*"]
                        app.add_middleware(
                        CORSMiddleware,
                        allow_origins =  origins,    # Allow the domains in the origins list
                        allow_credentials  = True,
                        allow_methods=["*"],        # We can also allow specific http mehtods. If were building a public API we may not to allow them to have post or put or delete http methods.
                        allow_headers=["*"] )        # We can allow specific headers as well


        So this is technically a 'middleware' is a term that is used in most of the web frameworks to refer to a function that runs before every
        every request. So if someone sends a request to all our apps, before it gets sent to the routers it goes through the middleware and our
        middleware can perform some sort of operation. But what we want to is to specify the origins of what domains we wanna allow. So what
        domains should be able to talk to our API and we would just put them in a list called as origins.
"""

""" NOW WE WILL SET UP GIT TO KEEP TRACK OF OUR CHANGES AND TO STORE OUR CODE IN A REPOSITORY.
     It would make the whole deployment  process a whole lot easier. But when check our files into git, by default it would check all the files.
     There will be some files which we dont want to check into the repository. So what we will do is that we will create a 'gitignore' file
     
     But we would run into an issue because if someone clones our repository he would not be able to see what libraries to install.
     And which other packages and dependencies to install for our application to actually work.

     What we would do is that we would create a requirements.txt file and we would pass in the output of pip freeze which would pass
     in all the installed libraries with their specific versions into the requirements.txt file
                pip freeze > requirements.txt  
    So now anyone can look into our requirements.txt file and install the dependencies for our application by :
                pip install -r requirements.txt

    Next we would set up and install git
    After installation do:
        1. Type (git init) in the terminal in VS Code and make sure you are in the root directory of your project.
            This will initialize git in your project and add a git folder in your directory.
        2. Now skip git add readme.md
        3. Now we will run (git add --all). This will add all of our files of the directory into the repository.
        4. Now run (git commit -m "Initial commot"), to commit and finalize the changes to the repository.
        5. Now run (git branch -M master) to set what our branch is. This would set our branch to be called as master
        6. Then we would have to set up a remote branch. This is whats gonna allow us to store all of our code to github.
            (git remote add origin https://github.com/anantinfinity9796/example-Fastapi.)
        7. Finally push the code to the github repository by (git push -u origin master)
        8. Finally the code is sent to the repository and we can verify that by going to github.

     """


""" Next we will move on to deploying our application.
    There will be two deployment methods that we will learn in this course.
        1. We will deploy our application to a platform called as Heroku. It would give anyone access to our API.
        2. Create an account on the heroku platform. Its free.
        3. Now we would nedd the Heroku CLI to be installed on our computer. Download the installer and run it.
        4. After you have installed heroku then usually we have to close the pre existing terminals and open again to access heroku.
        5. Now check the version of heroku installed in (heroku --version).
        6. Then login to the heroku by typing (heroku login)
        7. The heroku documents give us a demo app to follow along but we have our own app.

        8. We have to run the command (heroku create) to create and app wthin our heroku account. heroku create --help gives us all
            the arguments to the options we have when creating the app.
        9. We can day (heroku create <app name>)  to create our app and what we also need to know is that app names are global i.e
            if we create and app with a name, another user around the globe cannot create an app of the same name.
            The links are : https://fastapi-anant.herokuapp.com/ | https://git.heroku.com/fastapi-anant.git
        10. If we type in git remote it is gonna show all of the remotes that have been set up for our git. There two now : origin and
            heroku. So instead of using (git push origin master) to push it out to github we can just do (git push heroku master) and
            its gonna push out to our heroku platform and then it will then create an instance for our application and install all of
            the dependencies and deploy the application.
        11. In the output what it will do is that it would provide the URL of the application : https://fastapi-anant.herokuapp.com/
            For now this would give out an error which states that something in our application is broken and this is to be expected
            because we have to do somethings before the app starts working. 
        12. If take a look at what we have done is that we have pushed our app to heroku, but heroku does not know how to actually 
            start our application. It does not know what commands to use, it only knows that it is a python app. When we ran it in 
            our development environment we ran (uvicorn app.main:app --reload) to start the application but we havent given the 
            command to heroku yet.
        13. So what we have to do is that we have to create a file that is gonna tell heroku what is the exact command that we wanna
            run. So inside your root directory create a file called as 'Procfile'.

        14. The Procfile is just a file with the command that tells Heroku what is the command that we need to do start the application.
            We can give it a process type and since it is a web application it will be responding to web requests we would use

            web: uvicorn app.main:app --host=0.0.0.0 --port=${port:-5000}

            we are not gonna pass in uvicorn app.main:app --reload because we dont want the app to be reloaded on changes because this is production.
            There should be no changes in the application because it is in production.

             We do have to provide the host ip (--host=0.0.0.0), This is just saying that we should be able to respond to request to any IP.
             So whatever IP heroku gives us this is going to accept it.
             Next is the port flag (--port=${port:-5000}) which would run the app on the port provided. If nor specified it runs on default port.
             However in heroku they are actually going to provide us a port. So we dont know what this port is ahead of time but we have to accept it regardless.
             Its actually going to pass it as an environement variable. So anytime we want to accept an EV we do (${PORT}. default is 5000).

        15. Then we are gonna have to push out these changes once again using 
                git add --all
                git commit -m "added Procfile"
                git push origin master 
        16. Then to push the changes to the Heroku app do  (git push heroku master)
        17. Anytime the heroku app is not working they have a very easy way of accessing logs (heroku logs --tail). This would tail
            the logs as they happen.
        18. There is some error in our app because it needs the Environment Variables and it was not checked into git. So heroku does
            not know how to put the environment variables and we would do that either to the command line or through the dashboard.
        19. Heroku provides us with a free postgres instance that we can access:
            type heroku addons:create heroku-postgresql:<PLAN NAME> we have the PLAN NAME as 'hobby-dev'. This would start a heroku 
            postgres database instance in the cloud and it will get displayed on the dashboard and we can click on the databse and
            go to the settings and go and see the database credential. Heroku does not let us create our own databse and passwords,
            rather they give us their own database and passwords. And they also provide us the full postgres url if we wnat it.
        20. Heroku calls its instances as dynos.
        21. Config VARS in settings is the place we provide the environment variables to our heroku instance. There should be only
            one config variables. When you add your postgres instance to the heroku app, heroku adds up only one EV and that is
            databse_url and its going to contain the entire postgres URL. We could go into our application and code it up to put the 
            URL in our code but instead of putting this EV in our code directly we could break down  this url into multiple EV's. 
            Now see what the EV's are in config.py and set it in the settings-->Config VARS in the heroku dashboard.
            After doing this our app shoud work and we will try this out again.
            We cant use the app argument ot restart the app because it does not have a restart flag.
            On doing heroku ps --help we see that it has the restart option. So we do (heroku ps:restart) which is going to restart 
            our dyno heroku instance.
            Then we will do (heroku logs -tail to tail the logs).
        22. The Procfile is just a file with the command that tells Heroku what is the command that we need to do start the application.
             We can give it a process type and since it is a web application it will be responding to web requests we would use
             web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-5000}

             we are not gonna pass in uvicorn app.main:app --reload because we dont want the app to be reloaded on changes because this is production.
             There should be no changes in the application because it is in production.

             We do have to provide the host ip (--host=0.0.0.0), This is just saying that we should be able to respond to request to any IP.
             So whatever IP heroku gives us this is going to accept it.
             Next is the port flag (--port=${port:-5000}) which would run the app on the port provided. If nor specified it runs on default port.
             However in heroku they are actually going to provide us a port. So we dont know what this port is ahead of time but we have to accept it regardless.
             Its actually going to pass it as an environement variable. So anytime we want to accept an EV we do (${PORT}. default is 5000).
        23.  If we ever want to get information like URL's of the app etc. we can run (heroku apps:info fastapi-anant) and get the required info about our app.
        24.  You can access the swagger documentation and send requests with it on https://fastapi-anant.herokuapp.com/docs url. 
        25. If you try to send requests now and create a user you will be treated with a SQL error and what happened is that we had a new instance of postgres sql.
             but right now if you try to connect to that instance we are gonna see a few issues. We do not have any tables in our postgres instance if we connect
             to our databse in pgadmin4 appication, thats why we are getting errors. This is where alembic comes in again because we have our revisions set up,getting
             our production database to match our development databse will be as simple as running one command (alembic upgrade head) in our production instance and 
             we will see the production gets updated to our latest schema. The heroku instance has access to our revisions. 
             But we need to undersatnd that we never run revision on our production server. We only run them to our development server and then use push out all of
             code changes as well as all of the alembic revisions to our production server and we just run an (alembic upgrade head).
        26. But the first thing that we need to figure out is how to actually run a command in our heroku instance. We can do it by doing (heroku run<"command">).
             the aboe will run the alembic command which has all the incremental revisions and we could roll back like we did in the production environment.
             To make changes to the files what we need to do is that we would have to go through the whole process op adding, committing and pushing the changes
             and then we would also need to make changes to the heroku app also by (git push heroku master).
             To make changes to the postgres database we will have to do all the above steps and then do (alembic upgrade head) on top of it.
"""
NGINX High Performance Server
    Right now what we do is that when we send the request to our app then we send the request to the app directly. This is fine but 
    you will see that in more professional type deployments there will be an intermediary server running on an ubuntu machine and that
    web server will act as a porxy and will proxy that request to our specific application or the Gunicorn.

    One of the common web servers is NGINX. The benefits of doing this is:
    1. NGINX is optimised for SSL Termination.
    2. It is a high performance server.
    3. Whenever we send and https request we send it to NGINX and it converts it to plain http and forwards it to our application
        Technically we could configure our application to handle https but our app is not optimised for that, it designed to be a
        plain API, adding responsibilities like performing SSL offload would be a degradation in performance. SO we will use NGINX
        to be an intermediary and a gateway into our system.
    4. Any request we send to our system, http or https we will send it to our NGINX server and what it will do, if the request is https NGINX would take it and it will
        forward it as an http packet to our application.
    5. Its fairly easy to get it up and running. We just have to set a .config file.
    6. We would need a domain name for that.
    THIS NEEDS MORE ATENTION BECAUSE WE NEED TO CREATE A DIGITAL OCEAN ACCOUNT AND WE NEED TO SET UP A UBUNTU MACHINE AND ASLO INSTALL CRETIFICATES,CONFIGURE FIREWALL.
    SO WE WILL DO IT AFTER WE HAVE DONE EVERYTHING.



Dockerizing our application
    We are going to learn how to quickly set-up our fast-api application in docker and how to set up our POSTGRES application in docker.
        1. Go to dockerhub and download the base custom python official image. Now we would have to customize the image so that we can just run the image and our app
            gets working.
        2. All custom images need to start with a base image and we would customize it by including all of our source code into it and installing all the dependencies.
        3. To create a custom docker imgae go to the project directory, create a file referred to as a dockerfile. This dockerfile will have all of the steps nescessary 
            to create our own custom image.
        The first thing that we have to do is to specify our base image.

        # 1. Specify our base image which would be a Python 3.9.7 image
                FROM python:3.9.7
        # 2. This tells docker this is where all of the commands are going to run from
                WORKDIR /usr/src/app

        # Next what we are going to do is that we are going to copy our requirements.txt file from our local machine onto our docker container
            # COPY <filename><directory within our image that we want to copy it to>
            # # (./ is the current directory it points to WORKDIR /usr/src/app)
                COPY requirements.txt ./


        # We need to run a command which would be responsible for installing our dependencies because we have our requirements.txt file copied into our docker container.
                RUN pip install --no-cache-dir -r requirements.txt


        #  Now we would copy all of our source code from our local current directory into our current directory of the docker image.
                COPY . .

        # When docker runs what it does is that it creates images from a dockerfile what it does that it treats each line above as a Layer.
        #   So it kind of build the image by running the first layer then the second layer and so on and it caches the result of each step.
        #   So when you cache the result and nothin changes then we can use the cached result. So when it installs the requirements, which
        #   takes a decent amount of time but if we run this again and nothing has changed it can just use the cached result. This is
        #   beacuse when we run our source code here it is gonna see whats changed,does it change the base image : no; does it change the 
        #   working directory: no; did it change the dependency that we installed: no; It only changed the final step and this causes
        #   docker to reuse the result of the first 4 steps and only needs to run the last one. This gives us an advantage because 
        #   if we made the requirements step last then we would have to run the most time consuming step of installing requirements every time
        #   Thats why we copy the requirements.txt file so that we can cache the result and anytime we make any changes to the source code,
        #   we don't have to run a pip install.


        # Finally we would have to give it the command we want to run when we start the container. We would have to break our command into 
        #   small parts where it has a space between the commands and pass the individual elements as a string within this list.
                CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


        # Now our dockerfile is complete and we can build our image.
        # We do docker build --help for the different flags
        # We will do -t<tag><context(this is the directory where the dockerfile is) for a name to the app. 
        # So it will be (docker build -t fastapi .) .The " . " represents the current directory.
    
    Now we  can check all or docker images by doing (docker image ls).
    Now we can go ahead and use this image for building out a cotainer. So we can do (docker run --<flags>), but that is very tedious
    process and we would have to type long commands. So instead we would do a (docker compose) and this essentially does all the work 
    of docker run but we can define the commands in a seperate file so we dont have to remember all of these long commands.


DOCKER COMPOSE - Used to automatically spin up our one or multiple docker comtainers with one command.
    1. To use the docker compose we have to provide a file with a set of instructions using a file called as --> docker-compose.yml
    2. This is a yaml file is technically a markup language. In a yaml file spacing matter


    3. This is a yaml file and it is technically a markup language. In a yaml file spacing matters, kind of like python.

    4. First thing is that we need to specify what version of python is that we want to use.
    5. you can go to docker.com and see what features were added in the respective versions.
        version : "3"

    6. Then we have a concept of services : A service at the heart is essentially is a container.
    7. So if you want docker to spin you up a container you would have to define a service. If you want it to spin up 4 containers, define 4 services.
    8. So we have to each service or each container a name.

        services:
            api:
            build: . 
            ports:
                - 8000:8000

    9. To run this file do (docker-compose up -d) which would run the containers in the background
    10. When we run this we would see that what we are doing is that we are rebuilding the image, beacuse we specified the build here in services.
    11. And then it would start our container. The naming syntax comes from the project directory <direcotry>_<name of the service>_<instance number>.
    12. So this container would be fastapi_api_1.

    13. we can see which container are running and which have dies out by running (docker ps -a)
    14. To see what caused a container to die out and the log status we can do (dockers logs <container name>) such as (docker logs fastapi_api_1).
    15. This woud show the errors in the pydantic library and it would show that the environment variables are not set and as a container is like
        its own seperate machine it would be needing the environement variables passed in or our application gonna crash.

    16. So how do we pass environement variables in docker what we would do is that we would just pass a environment field

            services:
            api:
            build: . 
            ports:
                - 8000:8000
            env_file:
                - ./.env
            environment:
                - DATABASE_HOSTNAME  = postgres
                - DATABSE_PORT = 5432    
                - DATABSE_PASSWORD = Anant9796
                - DATABSE_NAME = Fastapi
                - DATABSE_USERNAME = postgres
                - SECRET_KEY = dipshit
                - ALGORITHM = HS256
                - ACCESS_TOKEN_EXPIRE_MINUTES = 30
        If you dont want to write our environement variables we can actually use docker to point to a .env file on our local machine.
        All  we need to do is to specify the env_file:
                                                    - ./.env  (current directory/.env)


    17. Now  we would do a docker-compose down to tear everything down and  do docker-compose up -d to bring everythin back up.
        But now notice that it didn't build the image. Well docker compose is very simple, so it goes to docker image ls and it looks
        for the image that it could have created which is in a very specific format in this case "fastapi_api_1". So since the image
        was already created previously it doesn't recreate it. But you can use the docker flag --build to force it to build the image.

    18. Now do a docker ps to see the status of the running container.
    19. We can go to localhost:8000 and send a get request and we will see that the we get a response from the image that is running.

    20. Now we want to set up our postgres database in our container. Because if we are able to access our API which is running on a container
        , the next thing we need is to set up our postgres database, but we have one installed on our local machine, why we would want to set
        up another one.
        1. First of all if we are already dockerizing our environment it makes sense to from a development perspective to set up our postgres
         database within a docker container, because its so much easier to set it up in a container than it is to install it on our local
         machine, because we can just spin up a pre-built image. So even if we don't wanna dockerize your application database, we should do 
         it from a development perspective, so that we can spin up a quick database just for testing purposes. Since we already have a docker
         based application now we are going to just use a postgres database running in a docker container instead of our local machine.

         If we take a look at our environment variables that we passed to our container, we provide a value of the localhost. So localhost means
         that the api running in the container is going to try to access the database running locally on the container which its not. 
    21. So lets create a brand new service which is nothing more than another container for running our postgres database. 
        So we will go to the docker-compost.yml file and in services we are going to create another service called as postgres.
        So previously we did build because we are building a custom image but here we are going to use a pre-built default postgres image.
        So if you go to dockerhub and search postgres, you will see the official postgres image which will contain all of the documentation 
            for setting up postgres, but the imortant thing is that we need to pass a couple of environment variables that we have to pass.
                 - POSTGRES_PASSWORD = Anant9796
                 - POSTGRES_DB = Fastapi
                 # One thing about containers is that when we kill the container the data gets lost so we need to save the data and for that 
                    we need to create something called as a volume which allows us to save data onto our local machine so if we kill our 
                    container, we can spin up a new container we can just point to those files. There are anonymous, named volumes. etc in docker.

                    services:
                        api:
                        build: . 
                        ports:
                            - 8000:8000
                        # env_file:
                            # - ./.env
                        environment:
                            - DATABASE_HOSTNAME=postgres
                            - DATABASE_PORT=5432    
                            - DATABASE_PASSWORD=Anant9796
                            - DATABASE_NAME=Fastapi
                            - DATABASE_USERNAME=postgres
                            - SECRET_KEY=dipshit
                            - ALGORITHM=HS256
                            - ACCESS_TOKEN_EXPIRE_MINUTES=30
                        postgres:
                        image:
                        environment: 
                            - POSTGRES_PASSWORD = Anant9796
                            - POSTGRES_DB = Fastapi
                        volumes:
                            - postgres-db: /var/lib/postgresql/data  # This is the path in the container that postgres writes to it is the named volume.

                    volumes:            # We do this because named volumes are designed so so that multiple containers can access them.
                    postgres-db:         # Swe would have to fill here the IP address of our postgres databse. So what docker does it that when we run docker-compose 
                                            it create a custom  docker netwot. So a docker network has its own DNS. So instead of writing the IP we can just use DNS
                                            and write "postgres"  or whatever our service is called, we can just reference that and the name will resolve the
                                            IP address of the container.

                    So we can just start this up with docker-compose up -d.

    22. But after this builds up the container with our app and the database what we would need to do is that we would need the databse
        to start up first because our app is dependent upon the database to work. So in the services.build of the docker-compose.yml file
        we can pass in another option depends_on:
                                        - postgres  which could just tell docker to start the postgres container before the api container starts.


        Technically it wont wait for the postgres container to initialize before it starts the api container. So we need to put in checks
        in our code to make sure that if we ca't access the databse its gonna keep retrying.
        After doing docker-compose up -d we would see that it would start the databse before the api and would kill the API before killing
        the database because the set up the depends on it.
    23. When we work  with docker containers we experience a few extra challenges :
        1.  If we make changes in our code like we change the message that we display on the landing page of the API, technically what it should
            do is that it should also change the text that we see in the response. But this is not the case as we can see the text did not change.
        2. For looking at the problem we gotta see what the file system of docker looks like. To do that we do (docker exec -it fastapi_api_1 bash).
            This is gonna allow us to access the file system which is the linux file system.
            So we change the directory to the app folder by doing (cd app).
            next we see whats in the docker container file of main.py by doing (cat main.py). This would show us the state of the file main.py
            the way the docker container has it and we have to make changes in such a way that the changes get reflected in the files in the
            container. Because what we did is when we created the image we also copied all the files the way they were when the image was created.
            So after that any changes will not get reflected in the container files.
        3. So how do we get around this limitation:

            1. The thing that we can do is to make use of a special volume called as a "Bind Mount". A bind mount is a special volume because it
                allows us to sync a folder on our local machine with a folder in our container. So we would wanna sync this folder in our development
                folder with the app folder in our container so the changes get copied to the container. We define it under volumes in the 
                docker-compose.yml file . 

                volumes: # This is a bind mount which allows us to sync the folders of our dev environment and docker containers
                    - ./:/usr/src/app:ro      # folders of our current directory:folder structure in ur docker cotainer. The ro(read_only prevents the container from changing any of the files)
            
            2. The problem with the above implementation is that the changes are getting refelcted only after we tear the container down and build it back up.
                This is happening because in the Dockerfile where we are building the image, where we have given the command to run the uvicorn server, we have not given the 
                reload flag. So the app is not restarting when a change is being detected. And we cannot see the change. For us to see the change, what we need
                is to tear the container down and build it back up. Then the changes would be visible.Or while creating the image we would pass the  (--reload) flag in the Run command
                while building the image so that when the changes take place it automatically restarts the app with the changes.

                But this is only for the development environment as in Production we would not like the app to be reloaded after every change.
                So there are two types of fixes:
                    1. First we add "--reload" in the CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
                    2. We could override it in the docker-compose.yml file also by adding another flag called as command in yaml type.
                                command : uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
            3. After we compose the container again we check and see that the bind mount works and now we have a development environement the likes
                of what we had before using docker.


    SETTING UP A REPOSITORY ON DOCKERHUB TO STORE OUR images
    1. We should have a docker account.
    2. Dockerhub is kind of the docker equivalent of github and it acts a kind of a repository for our docker images.
    3. Anytime we make a new image we can upload it so that we track changes in it over time.
    4. Create a new public repository with any name that you want.
    5. Go to the command prompt and type (docker image ls). What this will do is that it will list out all the docker images in your
        machine.
    6. First do docker login to login in the account by typing docker login in the terminal. Give your credentials if it does
        automatically login you.
    7. To upload the image to dockerhub just type (docker push <image name>).
    8. But if you push the image now by docker push fastapi_api what we would get is an error that request toresource is denied.
    9. This is because docker expects the push to happend by an exact specific naming convention.
        docker push <username>/<repository_name>:<tagname(optional)>
        docker push anant9796/fastapi:tagname
    10. Now we would have to rename our image. By docker image tag <source image to be renamed> <new name>:<tagname(optional)>
            docker image tag fastapi_api anant9796/fastapi
    11. Now you can find the new image name in docker image ls.
    12. Now push by : docker push <image name>.
    13. Now if go to the dockerub page we can see that the last push happened.
    14. So if we set up a production docker environment we could just pull the image from the dockerhub repositories.

    15. So if we take a look at our code we can see that we have an identical clone of our code in the code editor but we are also
        running our docker container with the same code running. The issue here is that when we are moving to production assuming 
        that we are using docker in production which is kind of the main idea behind docker that the dev and prod environment are
        almost exactly the same because they are using the same docker images and containers. But  if we try to use this docker compose
        file in production there is gonna be a whole bunch of issues.
            1. We would need to change the environment variables and we can't hardcode them.
            2. We wouldnt want the --reload flag.
            3. We wouldn't want the bind mount because the code shouldn't be changing.
            4. The ports that we use could also potentially be different.
        So even thought the production environments should be roughly similar, there are  some differences and we need to account for that
        Solution:
            We should create two docker compose files.
                1. Production
                2. Development
            An we would do the nescessary changes in the production file as decribed above and save it. But we would have some problems
            with the docker because `(docker-compose UP -d)` looks for only specific file names in the directory for the yaml file.
            * It would throw and error:::  Supported filenames: docker-compose.yml, docker-compose.yaml, compose.yml, compose.yaml

            So when we have a custom filename we do :::   docker-compose -f <filepath with filename> up -d
                                                    :::   docker-compose -f <filepath with filename> down
        


        The last thing that we want to change is that in the production environment we do not want to build the image, instead whats 
        recommended is that when you are done developing you push the brand new image to dockerhub and in the production environment 
        we just pull this image from dockerhub. 
            So we remove the build option from the production file and we set this to be a image: <name of the repository>:<tagname>





TESTING OUR API 
    Whenever we make some changes to our code what we need to be sure that the existing functionality is not being affected by our
    changes. So normally we after making changes we have to manually test out every single scenario to  make sure that things are working. This is not a very scalable solution and would essentially require a lot of wasted hours for essentially any changes to our code because we dont know what code we broke by doing those changes. 

    This is where an automated testing library comes into play and here we can define a whole bunch of tests to test the functionality
    automatically of our code to ensure that our changes have not broken anything.

    For testing the library we are gonna be using is called as PYTEST  and so we would install  and set it up.
    To run our testing all we have to do is to run the command pytest in the terminal and pytest would automatically go and run our
    tests and would also give the output on those tests.

    Our code is probably a little advanced for testing because we are coming from a background of no testing
    So we want to start out with the simplest of functions.
    So we will create a new file called as calculations.py beacuse it would be a collection of functions that we have to test.
    In this file we will define our first test. A test is really just a function or a method within a class. 
    Pytest will run through all of our tests and when it runs through it and no errors get thrown that means the test has passed, else failed . We would use the assert function and if we assert a false value then it throws and error.

    To test the add function we would have to import it into our mytests.py 
        from app.calculations import add

    To automatically make pytest to test your functions we can see the documentation for the python test discovery and the test discovery goes through the file system recursively and looks for tests with names as specific keywords. It cannot find files starting with test_*.py so it will not cosider it a test file. So we would need to rename our file to test_calculations.py.
        We would also need a __init__.py file in the folder for our folder to be considered a package.
        Now we would run pytest from the terminal and it would just automatically discover the tests.

    We can also find the test file by specifying the file path after the pytest keyword and then we wont have to rename the file.
        pytest tests/mytest.py

    If you want more verbose text in the test  description then you would have to do pytest -v
    By default pytest will not any of the print statements defined in the function to the test result. We would have to pass a flag for that ..... pytest -v -s

    PARAMETERIZE - Pytest provides us a simpler method for testing functions with multiple sets of inputs and outputs rather than copying the function and changing the inputs and outputs.
        We can do this using something called as Parameterize. We can add a decorator to our test function
         @pytest.mark.parameterize()   and then provide a list of different inputs for testing and then provide a n expected result.

    Testing functions is a little bit easier than when we are trying to test classes, we have to write more code.
        1. So we would create a bank account class in the calculations.py file and import it in our test_calculations.py
        2. We can see that when testing the class we always have to initialize an object of the type class (here BankAccount)This     is a repetitive process across all of our tests and when we get to a more complex class we might have 50 tests for a single class and it would be a highly repetitive process.
        3. FIXTURES - Pytest provides us with some tools to minimize some repetitive code and these are called as fixtures. A fixture is nothing more than a function that runs before each one of the specific tests that you want.

        4. So we can create a function that does nothing more but initialize a bank account and return it to our function thats about to run. The best practice is to keep the fixture at the top of the file.
                    @ pytest.fixture
                    def ban_account():
                        return BankAccount(50)   # return the bank account with an initial balance

        5. For all of the tests we would reference the fixture by passing it as an argument to the test function.
        6. As pytest see the fixture as an argument then it would call the fixture function before it runs the test case and the return value get passed into the variable parameter name.

                def test_withdraw(bank_account):
                    bank_account.withdraw(10)
                    assert bank_account.balance == 40

        7. So what if need to test transactions for a bank accounts doing multiple transaction with multiple input-output values. This would need us to combine  Fixtures and Parameterize decorators.
        8. But for scenarios where you expect to raise an error would we would need to have another test case. Where an error in the execution leads to a passed test case and not failed test case. But how do we tell python that its gonna recieve an exception
            We do it by -----> with pytest.raises(Exception):
                                    bank_account.withdraw(200).   So whats its gonna do is that the test will pass if the exception 
                                                                                                            is raised.

        8. In real scenarios we won't be having generic exceptions. We would be writing our own exception classes which will extend the Exception class.  
                    class InsufficientFunds(Exception):
                        pass
            If we wanted to be as apecific as possible we can import the insufficient funds class into our test file and tell pytest that we expect InsufficientFunds type Exception in our exceptions.
            The good thing about this practice is that if for some reason our code raised some  other type of exception, our code test will fail.

FASTAPI TEST CLIENT
    When it comes to FastAPi it automatically provides us with a test client.
        from fastapi.testclient import TestClient  
        Then we can just pass in out api instance which is stored in our app and then we can perform any request to our application by doing 
                client = TestClient(app)

                response = client.get("/")
        As this is based on the requests libary anythin we could do with the requests library we could do with the test client.

        So we are going to make a new file called as test_users.py to test the users functionality

    There are a couple of other flags that we can pass to the pytest command so that we can tweak the behaviour of our testing.
        1. We can disable warnings by pytest --disable-warnings.

        2. When we have multiple tests failing then the default behaviour is that when a test fails we continue running the other tests. But this may not be the behaviour that we want, if we wanted our tests to stop when a test fails and then fix it and then run the other tests. if we want to do that we could just pass in the (" -x ") flag which would stop the testing after the test fails.
                            pytest -v -x

    Lets create the tests for testing user create functionality
        def test_create_user():
            res = client.post("/users/", json = {"email":"hello123@gmail.com", "password":"password123"})

            print(res.json())
            assert res.json().get("email") == "hello123@gmail.com"
            assert res.status_code == 201
    Instead of doing the assert statements manually and testing all the parts of the response object what we can do is that we can import the schema of the UserCreate_Response to by importing the schema file in the test_user.py file.


        def test_create_user():
            res = client.post("/users/", json = {"email":"hello123@gmail.com", "password":"password123"})

            new_user = schemas.UserCreate_Response(**res.json()) # we unpack the response object into a dictionary and pass it in a pydantic schema for validation by pydantic class of UserCreate_Response()
            # The above would just validate that the response has the required fields
            print(res.json())
            assert new_user.email== "hello123@gmail.com"
            assert res.status_code == 201
    
    Right now we are using our develoment database for our tests and thats not good. So I want to create a seperate database of my own
    for testing so that I dont get in the way of develoment, staging or production databases. 
        Right now when we import our client we would be using whatever the database is defined in the rest of our app which is going to be our fastpai database

    One of the good things that we have done in our database file is that we have created a dependency called as get_db() which returns the Sessionlocal which allows us to make queries using SQL ALchemy and that comes from the sessionmaker where we passed in all of our details. And if we go into anyone of our routes we can see that we have passed in the dependecy into our routes.
        The easy thing about dependencies is that it is very easy to override a dependency in any environment especially in a testing environment we can say that instead of get_db() we can define another dependency get_test_db() which is going to be a function which returns the test instance of our database.

    Below we are going to see how to create a test instance of our database. So we will copy all of the code in our database.py into the test_users.py file. To create another instance override_test_db() we will make use of the code in database.py and change the variable names.

    But the problem still persists that how do we override any dependency. Fastapi has some documentation for this also. It is called as Testing Dependencies with overrides.
    To setup the override we do app.dependency_overrides[dependency we want to oveeride] = override the dependency with another one

    When we run the above command what it is gonna do is that it is gonna override the function parameters of the dependencies i.e get_db() with the function override_get_db() which is just going to give a different session object which is just pointing towards a different database. Thats why we had set up that dependency when we first started that database.

    Since this is a database the SQL url will still be using development Environment variables but we can hardcode the environment variables for our testing database because that does not pose a threat to the security of our app.

    Since we have a brand new database the last thing that we want to do is that we would want to create the tables in the database.So we have to build out our tables before we do any other thing.

    But for the test database we would do it with the sqlalchemy to build all the tables based  of the models. We could use almebic
    as well. So we will see how to set up alembic in our testing database to show migrations in our testing as well but for now we are gonna keep things simple and use the SQL ALchemy path. 


    So now we have a database set up but now what is happening is that if we try to run the tests two times what is happening here is that once a user is created in the database due to the unique constraints the same test with the same credentials cannot be used again. This throws an error and cuases the things to break. 

    But I want to run my tests as many times as possible and I want to start out  with a clean set of tables every time. 
    We can make use of fixtures which is function that runs before our tests runs
            @pytest.fixture
            def client():
                """ This is actually going to return our client and the name of the function is actually the TestClient object
                        that we created will be returned by this function and this function will be referenced by the test functions
                        that need to run multiple times without violating the unique constraints of the tables."""

                return TestClient(app)

    But just making this function has not solved the problem, but we now have a function that runs before each one of the tests that gives us our testing client and whats even better is we can change the function a little bit from "return TestClient(app)"
    to "yield TestClient(app)". Because now we can put in logic to what should be run before our test runs. We then "yield TestClient(app)" which is the same as returning our TestClient but the function does not exit and then we can put in some logic do do something after our test finishes.
                    @pytest.fixture
                    def client():
                        # Run some logic before our test runs to create the tables
                        Base.metadata.create_all(bind =engine)

                        # Yield the TestClient(app) which is the same as return but the function does not stop with yield
                        yield TestClient(app)

                        # run some logic after the test runs and drop off all the tables
                        Base.metadata.drop_all(bind = engine)
    Now after running the test and then going back to database we can see that the test passed but there are no tables in the db because we dropped the tables after we are done. And if we run the tests again we can see that the test runs successfully wothout any without us having to think of any duplicate users.
    One thing that we can do is to drop off all the existing tables first and then create the new ones and then return the app, because if any test fails then we can pass in the -x flag to stop the test after it fails and we get to keep all of our data and tables so we can see what is the current state of the database when the test fails. Because if we just delete the table then we everythin will be lost and we wont be able to see what went wrong.
                    @pytest.fixture
                    def client():
                        # run some logic and  drop off all the tables before the begining of a new test cycle
                        Base.metadata.drop_all(bind = engine)

                        # Run some logic and create the tables for the test to run successfully
                        Base.metadata.create_all(bind =engine)

                        # Yield the TestClient(app) which is the same as return but the function does not stop with yield
                        yield TestClient(app)
    If we dont want to use SQLAlchemy then we can do it with alembic just import command from alembic 
                    from alembic import command

                    @pytest.fixture
                    def client():
                        # run some logic and  drop off all the tables before the begining of a new test cycle
                        command.downgrade("base")

                        # Run some logic and create the tables for the test to run successfully
                        command.upgrade("head")

                        # Yield the TestClient(app) which is the same as return but the function does not stop with yield
                        yield TestClient(app)
    FIXTURES IN FIXTURES
        One of the great things about fixtures is that we can code one fixture to be dependent upon other fixtures. So we can essentially pass one fixture into the argument of another fixture. The reason we are doing this is that we want one fixture that returns our database objects and the other fixture that returns my clients.

        For the database override functionality what we are gonna do is that we are gonna move it also into the session function
        and this session fixture will yield the database object and what I can do now is that I can pass in the session fixture into my client fixture and so by doing it like this whats gonna happen is that anytime I go into my tests and I pass in the client fixture as a dependency its gonna call the client funtion and the client function will call the session fixture before it runs and in the client fixture we can pass in all the logic that we normally would. So we would copy the override_get_db function into the client fixture and in the override_get_db intead of yielding the db we would yield the session and then we copy the line    
                        app.dependency_overrides[get_db] = override_get_db

                                                    and yield a brand new test client.

        The benefit of this is that not only we get access to the client we get access to the database as well, so I can make queries and I have access to the client as well.



    Now we can see that our test_users files is a little bit cluttered with all the database information so we can move the database specific code to another file database.py in the tests folder.


THERE IS ONE SLIGHT ISSUE THAT EXISTS IN THE ROUTERS IS THAT IF WE SEND A REQUEST TO "/USERS", IT IS DIFFERENT WHEN THE REQUESTS ARE BEING SENT TO "/USERS/".  When we send the requests from POSTMAN we were sending it to "/users" and then if we look at the 
terminal logs we can see that when we send requests to "/users" it redirects it to "/users/".
                INFO:     127.0.0.1:52666 - "POST /users HTTP/1.1" 307 Temporary Redirect
                INFO:     127.0.0.1:52666 - "POST /users/ HTTP/1.1" 201 Created.

But the fastapi is intelligent enough to send the redirects to "/users/". However this creates an issue with our testing because it does not automatically redirect and when we check for the status code it would send a status code error. beacuse it gets that the final status_code is 307 and not 201. So we wanna make sure that we add that trailing slash otherwise we would run into some issues when testing the code.
