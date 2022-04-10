""" This would handle our database connections and other stuff related to the Databases """

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings  # Importing the pydantic class of environement variables from the config file.

# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time


# Setting up the connection to the database using the databse driver of PGAdmin.
# If we enter some credentials wrong in connecting to the database it does not connect but the later code keeps on executing.
# To mitigate that problem we put the connection code in a WHILE loop when executes until database is connected.

# while True:
#     try:
#         """ The connect method of the psycopg library is used for connecting to the POSTGRES database and it has some parameters
#                 1. host : IP adress of the host
#                 2. database
#                 3. username
#                 4. password"""
#         conn = psycopg2.connect(host = 'localhost',database = 'Fastapi', user = 'postgres', password = 'Anant9796',
#                     cursor_factory = RealDictCursor )
#         cursor = conn.cursor()
#         print('Datbase connection was succesful!')
#         break     # breaks out if connection is succesfull.

#     except Exception as error:
#         print('Connecting to databse failed')
#         print('Error: ', error)
#         time.sleep(2)





# Now we need to specify our connection string i.e where our database is located.
# A lot of time when working with database connections there is a Unique URL that we need to create for connecting to the database.
# There is a unique format string for a URL that needs to be passed.

# SQLALCHEMY_DATABASE_URL_TEMPLATE  = 'postgresql://<username>:<password>@<ip-address/hostname>/database_name>'
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

# SQLALCHEMY_DATABASE_URL  = 'postgresql://postgres:An@nt9796@localhost/Fastapi'

# Now we will have to create an Engine that will be responsible for SQL Alchemy to connect to a Postgres Database.

engine = create_engine(SQLALCHEMY_DATABASE_URL) #Check documentation for other databases.

# But when we actually wanna talk to a SQL Database we would need to have a session
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine )  # these are default values

# Define our Baseclass and all the Models that we would define to create our tables would be extending this Base Class.
Base = declarative_base()

# The last thing that we need to do is to create a dependency.
# The session object is responsible for connecting to the database and the function below does the job for us.
# Every time we get a request we would be able to get a session and we will be able to send SQL request to it and close the seeion when we are done.
# So in our path operations wherever we need to interact with the databse we would just need to pass one more keyword for the database session.
# We coud keep calling this function anytime we get a request to our API endpoints.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
