""" This file contains the BaseClass derived Models of Tables do that we can define our tables with Python code through an ORM such as SQL Alchemy. """




from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

# Define our Model. Since we are working with posts only we would define our structure for posts.
class Post(Base): # This class extends the Base Class from the file database.py in this directory.
    # creating a table with a tablename
    __tablename__ = "posts"

    # defining the columns

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published  = Column(Boolean, server_default = 'True', nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))
    owner_id  = Column(Integer, ForeignKey("users.id", ondelete= "CASCADE"), nullable = False )
    
    # we would import relationships from sqlalchemy.orm and what it does is that it retrieves some information from a table.
    # It is not a foreign key.

    owner = relationship("User")  # We are referencing an actual sqlalchemy class and not the table users
    # What its going to do for us is that its going to create another property for our post so that when we retrieve a post its going return
    # a owner property and its going to figure out the relationship to user. So its going to fetch the user based off the owner_id and return
    # that for us. We would need to update our schema also to see the changes. 


""" The problem with SQL ALchemy is that it generates tables in a very simple way i.e it goes through 
the database and checks if the tablename exists. If it doesn't then it creates the table but if it does then SQLAlchemy
does not do anything and the table does not get updated. So every time we need a table to be updated we will need to
delete the previous table and create a new one."""

""" If we want to make changes to the table schema after we have created it or make Database migration we would need
another too called as ALEMBIC"""


""" For our added functionality we would create a user based system where a user can CRUD his own posts and this will be specific for every user
So we would need some Login functionality and for that we would need to process user authentication details.
So for that we would create a USER table. """

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default= text('now()'))
    phone_number = Column(String)


class Vote(Base):
    __tablename__ = 'votes'

    user_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), primary_key = True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete = "CASCADE"), primary_key = True)


