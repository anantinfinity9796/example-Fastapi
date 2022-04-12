""" Testing the user functionality with the fastAPI test client """

from app import schemas # importing the schemas so that the validation can happen easily.
import pytest
from jose import jwt
from app.config import settings










# # Testing the root url
# def test_root(client):
#     res = client.get('/')
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'Now the bind mount works completely'
#     assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json = {"email":"hello123@gmail.com", "password":"password123"})

    new_user = schemas.UserCreate_Response(**res.json()) # we unpack the response object into a dictionary and pass it in a pydantic schema for validation by pydantic class of UserCreate_Response()
    # The above would just validate that the response has the required fields
    assert new_user.email== "hello123@gmail.com"
    assert res.status_code == 201


def test_login(client, test_user):
    res = client.post("/login", data = {"username": test_user['email'], "password": test_user['password']})

    # Taking the token dictionary and validating the schema
    login_res = schemas.Token_Response(**res.json())

    # Now we also want to validate the token by decoding it to verify that the access_token is valid and contains the same user_id as the user that we created by the test_user response
    payload = jwt.decode(login_res.access_token, settings.SECRET_KEY, algorithms = [settings.ALGORITHM])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200


# Next we want to test for a failed login. But we want to test wrong email as well and a couple of other things.
# So we will use parameterize for it.


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password246', 403),  # wrong email, right password
    ('anant@gmail.com', 'wrongpassword', 403),    # right email, wrong password 
    ('wrongemail@gmail.com', 'wrongpassword', 403), # wrong email, wrong password
    (None, 'password123', 422),         # No email will give a schema validation error with 422 status code
    ('anant@gmail.com', None, 422)      # No password would also give out a schema validation error of 422 status_code.
])
def test_incorrect_login(email, password, status_code, client):
    res = client.post("/login", data = {"username":email, "password":password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == "Invalid Credentials"