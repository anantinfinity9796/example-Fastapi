""" Testing the user functionality with the fastAPI test client """

from app import schemas  # importing the schemas so that the validation can happen easily.
from .database import client, session    # Import the client fixture from the file database.py file in tests folder.



# Testing the root url
def test_root(client):
    res = client.get('/')
    print(res.json().get('message'))
    assert res.json().get('message') == 'Now the bind mount works completely'
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json = {"email":"hello123@gmail.com", "password":"password123"})

    new_user = schemas.UserCreate_Response(**res.json()) # we unpack the response object into a dictionary and pass it in a pydantic schema for validation by pydantic class of UserCreate_Response()
    # The above would just validate that the response has the required fields
    print(res.json())
    assert new_user.email== "hello123@gmail.com"
    assert res.status_code == 201