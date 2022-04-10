""" Testing the user functionality with the fastAPI test client """

from http import client
from fastapi.testclient import TestClient
from app.main import app
from app import schemas  # importing the schemas so that the validation can happen easily.


# Setting up the test database instance

from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db


# Hardcoding the environment variables for the test database URL 
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Anant9796@localhost:5432/fastapi_test"
# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

# SQLALCHEMY_DATABASE_URL  = 'postgresql://postgres:An@nt9796@localhost/Fastapi'

# Now we will have to create an Engine that will be responsible for SQL Alchemy to connect to a Postgres Database.

engine = create_engine(SQLALCHEMY_DATABASE_URL) #Check documentation for other databases.

# But when we actually wanna talk to a SQL Database we would need to have a session
TestingSessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine )  # these are default values

# Define our Baseclass and all the Models that we would define to create our tables would be extending this Base Class.
Base = declarative_base()

# The last thing that we need to do is to create a dependency.
# The session object is responsible for connecting to the database and the function below does the job for us.
# Every time we get a request we would be able to get a session and we will be able to send SQL request to it and close the seeion when we are done.
# So in our path operations wherever we need to interact with the databse we would just need to pass one more keyword for the database session.
# We coud keep calling this function anytime we get a request to our API endpoints.
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


# Setting our app in the TestClient to a variable called as client
client = TestClient(app)


# Now we can run whatever tests that we want.

# Testing the root url
def test_root():
    res = client.get('/')
    print(res.json().get('message'))
    assert res.json().get('message') == 'Now the bind mount works completely'
    assert res.status_code == 200

def test_create_user():
    res = client.post("/users/", json = {"email":"hello123@gmail.com", "password":"password123"})

    new_user = schemas.UserCreate_Response(**res.json()) # we unpack the response object into a dictionary and pass it in a pydantic schema for validation by pydantic class of UserCreate_Response()
    # The above would just validate that the response has the required fields
    print(res.json())
    assert new_user.email== "hello123@gmail.com"
    assert res.status_code == 201