""" Test File for posts. This will pose some extra challenges beacuse all of our post path operation require authentication"""
""" We  would like to create a fixture that does this automatically for us. But instead of making requests to our API I want to just
    import the method (oauth2) for creating an access token. So we could just import this into our tests and create a fake token for
    ourselves wihtout having to go through the full api and get a token by making calls. """
""" We will go to conftest.py to create the fixtures. """

from email import contentmanager
from turtle import title
from typing import List
from app import schemas
import pytest









def test_get_all_posts(authorized_client, test_post):
    res = authorized_client.get("/posts/")
    # its up to decide to us what checks we want to perform on the response object.
    assert len(res.json()) == len(test_post)

    # Lets see how we can do the validation of out posts data via the schemas.
    def validate(post):
        return schemas.Post_Vote_Response(**post)
    posts_map = map(validate, res.json())

    # After we have validated the responses and we have access to the posts_map list we can put assert statements to test anything.


    posts_list = list(posts_map)

    assert len(res.json()) == len(test_post)
    assert res.status_code == 200

    # assert posts_list[0].Post.id == test_post[0].id


# Now we setup the test to retrieve all the post and now what we want to do is that test that an unauthenticated user is not bale to retrieve posts.

def test_unathorized_user_get_all_posts(client, test_post):
    res = client.get("/posts/")

    assert res.status_code == 401


# Now we will want to test getting an idividual post by id for an unauthenticated user.

def test_unathorized_user_get_one_posts(client, test_post):
    res = client.get(f"/posts/{test_post[0].id}")

    assert res.status_code == 401

# we also want to test to retrieve posts for an id that does not exist.

def test_get_one_post_not_exist(authorized_client, test_post):
    res = authorized_client.get(f"/posts/8888")

    assert res.status_code == 404


def test_get_one_post(authorized_client, test_post):
    res = authorized_client.get(f"/posts/{test_post[0].id}")

    # We can also do the validation as by the shcemas
    post = schemas.Post_Vote_Response(**res.json())
    assert post.Post.id == test_post[0].id
    assert post.Post.content == test_post[0].content

@pytest.mark.parametrize("title, content, published", [
    ("new title", "new contnet", True),
    ("favourite pizza","good pizza", True),
    ("yeah new title", "no content", False),
    ("tell you nothing", 'No telling', True)
])
def test_create_post(authorized_client, test_user, test_post, title, content, published):
    res = authorized_client.post("/posts/", json = {"title":title, "content": content, "published":published})

    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_post_default_published_true(authorized_client, test_user,  test_post):
    res = authorized_client.post("/posts/", json = {"title":'arbitrary', "content": 'arbitarary content'})

    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == 'arbitrary'
    assert created_post.content == 'arbitarary content'
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']


# Testing a user creating not logged in 
def test_unathorized_user_create_post(client, test_post, test_user):
    res = client.post(f"/posts/", json={"title":"arbitrary title", "content":"arbitrary"})

    assert res.status_code == 401

# Testing for and unauthorised user to delete a post.
def test_unauthorized_user_delete_post(client, test_user, test_post):
    res = client.delete(f"/posts/{test_post[0].id}")

    assert res.status_code == 401

# Testing a successful deletion of the post
def test_delete_post_success(authorized_client, test_user, test_post):
    res = authorized_client.delete(f"/posts/{test_post[0].id}")

    # we could also assert that the total number of posts is one less
    assert res.status_code == 204

# testing a deletion of a nonexistent post

def test_delete_post_non_exist(authorized_client, test_user, test_post):
    res = authorized_client.delete(f"/posts/50000")

    assert res.status_code == 404

# testing deleting a post of other user
# For this we would need multiple users and it is best to use fixtures and create them in conftest.py
def test_delete_other_user_post(authorized_client, test_user, test_post):
    # The authorized client would always be logged in as user1.
    res = authorized_client.delete(f"/posts/{test_post[3].id}")

    assert res.status_code == 403


# Now we are looking at updating a post
def test_update_post(authorized_client, test_user, test_post):
    data = {
        'title':'updated_title',
        'content':'updated_content',
        'id': test_post[0].id
    }

    res = authorized_client.put(f"/posts/{test_post[0].id}", json = data)

    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

# Now we wil try to update another  users post

def test_update_another_user_post(authorized_client, test_user, test_post, test_user2):
    data = {
        'title':'updated_title',
        'content':'updated_content',
        'id': test_post[3].id
    }

    res = authorized_client.put(f"/posts/{test_post[3].id}", json = data)

    
    assert res.status_code == 403
    
# unauthenticated user trying to update a post
def test_unauthorized_user_update_post(client, test_user, test_post):
    res = client.put(f"/posts/{test_post[0].id}")

    assert res.status_code == 401


# test to update apost that does not exist
def test_update_post_non_exist(authorized_client, test_user, test_post):
    data = {
        'title':'updated_title',
        'content':'updated_content',
        'id': test_post[3].id
    }
    res = authorized_client.put(f"/posts/50000", json = data)

    assert res.status_code == 404