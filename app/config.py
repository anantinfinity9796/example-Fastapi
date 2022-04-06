""" This file hosts the code for automatically setting up and Validation of Environment Variables and all the configs related to the application"""


# Using pydantic to perform the validation of Environment Variables
from pydantic import BaseSettings


# Using pydantic to perform the validation of Environment Variables
class Settings(BaseSettings):
    """ Best Practice to set EV's is to do ALL CAPS."""
    database_hostname: str 
    database_port: str 
    database_password : str
    database_name: str
    database_username: str
    secret_key : str
    algorithm :str
    access_token_expire_minutes : int

    # Now we will have to tell Pydantic to just import the variables form the '.env' file
    class Config:
        env_file = ".env"

# we could technically set all the variables manually on our windows machine but thats a lot of work. So we will create a new file '.env' which contains all of our EV's.
# In production we won't do it with a '.env' file all of this rather we would set it on our machine but its perfectly fine to set it here.


settings = Settings()   # creating and instance of the settings class and pydantic will do all the checks