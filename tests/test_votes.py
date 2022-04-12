""" This file will be used to test the voting functionality """
from multiprocessing import AuthenticationError
import pytest
from app import models


@pytest.fixture()
def test_vote(session, test_user, test_post):
    new_vote = models.Vote(post_id = test_post[3].id, user_id = test_user['id'])
    session.add(new_vote)
    session.commit()













# testing a successful vote
def test_sucessfull_vote_on_post(authorized_client, test_post):
    res = authorized_client.post("/vote/", json = {"post_id":test_post[3].id, "direction":1})

    assert res.status_code == 201

# testing voting twice on the same post
# For this we would need to have a post that's aready been voted on but our current test_post fixture doesn't allow it. So we need a new one
# We will define it here because we don't think that it would be used elsewhere.
def test_vote_twice_post(authorized_client, test_post, test_vote):
    res = authorized_client.post("/vote/", json = {"post_id": test_post[3].id, "direction": 1})

    assert res.status_code == 409



# testing successfully deleting a vote
def test_delete_vote(authorized_client, test_post, test_vote):
    res = authorized_client.post("/vote/", json = {"post_id":test_post[3].id, "direction":0})

    assert res.status_code == 201


# deleting a vote that does not exist
# we are gonna remove the test_vote fixture beacuse we want to make sure that there is not a vote.
def test_delete_vote_non_exist(authorized_client, test_post):
    res = authorized_client.post("/vote/", json = {"post_id":test_post[3].id, "direction":0})

    assert res.status_code == 404



# finally lets try the to vote on a post that does not exist

def test_vote_post_non_exist(authorized_client, test_post):
    res = authorized_client.post("/vote/", json = {"post_id":50000, "direction":1})

    assert res.status_code == 404


# lastly we wanna check that a user who isn't authenticated cannot vote
def test_vote_unauthorized_user(client, test_post):
    res = client.post("/vote/", json = {"post_id":test_post[3].id, "direction":1})

    assert res.status_code == 401



""" this concludes our tests """ 
