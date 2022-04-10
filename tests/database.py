""" This file would contain all if the code related with the database fastapi_test """

from http import client
from fastapi.testclient import TestClient
from app.main import app
import pytest

from alembic import command  # For doing the creation and deletion of database tables in the test database with alembic


# Setting up the test database instance

from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db
from app.database import Base


# Hardcoding the environment variables for the test database URL 
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Anant9796@localhost:5432/fastapi_test"
# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

# SQLALCHEMY_DATABASE_URL  = 'postgresql://postgres:An@nt9796@localhost/Fastapi'

# Now we will have to create an Engine that will be responsible for SQL Alchemy to connect to a Postgres Database.

engine = create_engine(SQLALCHEMY_DATABASE_URL) #Check documentation for other databases.

# But when we actually wanna talk to a SQL Database we would need to have a session
TestingSessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine )  # these are default values

# Define our Baseclass and all the Models that we would define to create our tables would be extending this Base Class.
# Base = declarative_base()

# The last thing that we need to do is to create a dependency.
# The session object is responsible for connecting to the database and the function below does the job for us.
# Every time we get a request we would be able to get a session and we will be able to send SQL request to it and close the seeion when we are done.
# So in our path operations wherever we need to interact with the databse we would just need to pass one more keyword for the database session.
# We coud keep calling this function anytime we get a request to our API endpoints.


# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db

# Creating the tables using the sqlalchemy
# models.Base.metadata.create_all(bind =engine)
# Base.metadata.create_all(bind =engine)

# Setting our app in the TestClient to a variable called as client
# client = TestClient(app)






# Now we can run whatever tests that we want.

# For running our tests multiple times with the same credentials and not violating the unique constraints of the table and not causing errors.
# For the above task we would create fixtures 

# @pytest.fixture
# def client():
#     """ This is actually going to return our client and the name of the function is actually the TestClient object
#              that we created will be returned by this function and this function will be referenced by the test functions
#              that need to run multiple times without violating the unique constraints of the tables."""

#     return TestClient(app)

# @pytest.fixture
# def client():
#     # Run some logic before our test runs to create the tables
#     Base.metadata.create_all(bind =engine)

#     # Yield the TestClient(app) which is the same as return but the function does not stop with yield
#     yield TestClient(app)

#     # run some logic after the test runs and drop off all the tables so that we start from scratch the next time around.
#     Base.metadata.drop_all(bind = engine)


# @pytest.fixture
# def client():
#     # run some logic and  drop off all the tables before the begining of a new test cycle
#     Base.metadata.drop_all(bind = engine)

#     # Run some logic and create the tables for the test to run successfully
#     Base.metadata.create_all(bind =engine)

#     # Yield the TestClient(app) which is the same as return but the function does not stop with yield
#     yield TestClient(app)

# Doing the above functionality with alembic
# @pytest.fixture
# def client():
#     # run some logic and  drop off all the tables before the begining of a new test cycle
#     command.downgrade("base")

#     # Run some logic and create the tables for the test to run successfully
#     command.upgrade("head")

#     # Yield the TestClient(app) which is the same as return but the function does not stop with yield
#     yield TestClient(app)
 

# One of the great things about fixtures is that we can code one fixture to be dependent upon other fixtures.
# So we can essentially pass one fixture into the argument of another fixture. The reason we are doing this is
#  that we want one fixture that returns our database objects and the other fixture that returns my clients.
# So we are going to break the logic of manipulating the database and the yielding of the client into two seperate fixtures

@pytest.fixture
def session():
    # run some logic and  drop off all the tables before the begining of a new test cycle
    Base.metadata.drop_all(bind = engine)

    # Run some logic and create the tables for the test to run successfully
    Base.metadata.create_all(bind =engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

    

@pytest.fixture
def client(session):
    # Yield the TestClient(app) which is the same as return but the function does not stop with yield
    def override_get_db():
        
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)