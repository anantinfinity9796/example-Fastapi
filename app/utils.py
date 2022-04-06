""" This file will contain a bunch of utility functions. Such as password hashing logic and So on, so forth """

# Password hashing and security libraries import 
from passlib.context import CryptContext

# What we are doing here is that we are telling passlib what is the default hashing algorithm. In this case this is "bcrypt".
pwd_context = CryptContext(schemes= ["bcrypt"], deprecated = "auto")


def hash(password: str):
    """ Returns the hash of the string password given by the user. """    
    return pwd_context.hash(password)


""" We would create a function which is going to take the raw password provided by the user and hash it and then compare it with
    the hash provided by the database after querying. """

def verify(plain_password: str, hashed_password):
    
    """ verifies if the hash of the plain text password and the password returned by querying the database is equal. """

    return pwd_context.verify(plain_password, hashed_password)