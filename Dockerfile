# """ This file would contain all of the steps nescessary to create our own custom docker image. """

# 1. Specify our base image which would be a Python 3.9.7 image
FROM python:3.9.7
# 2. This tells docker this is where all of the commands are going to run from
WORKDIR /usr/src/app

# Next what we are going to do is that we are going to copy our requirements.txt file from our local machine onto our docker container
    # COPY <filename><directory within our image that we want to copy it to>
    # # (./ is the current directory it points to WORKDIR /usr/src/app)
COPY requirements.txt ./


# We need to run a command which would be responsible for installing our dependencies because we have our requirements.txt file copied into our docker container.
RUN pip install --no-cache-dir -r requirements.txt


#  Now we would copy all of our source code from our local current directory into our current directory of the docker image.
COPY . .

# When docker runs what it does is that it creates images from a dockerfile what it does that it treats each line above as a Layer.
#   So it kind of build the image by running the first layer then the second layer and so on and it caches the result of each step.
#   So when you cache the result and nothin changes then we can use the cached result. So when it installs the requirements, which
#   takes a decent amount of time but if we run this again and nothing has changed it can just use the cached result. This is
#   beacuse when we run our source code here it is gonna see whats changed,does it change the base image : no; does it change the 
#   working directory: no; did it change the dependency that we installed: no; It only changed the final step and this causes
#   docker to reuse the result of the first 4 steps and only needs to run the last one. This gives us an advantage because 
#   if we made the requirements step last then we would have to run the most time consuming step of installing requirements every time
#   Thats why we copy the requirements.txt file so that we can cache the result and anytime we make any changes to the source code,
#   we don't have to run a pip install.


# Finally we would have to give it the command we want to run when we start the container. We would have to break our command into 
#   small parts where it has a space between the commands and pass the individual elements as a string within this list.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# We could also have done the below command instead of the above command but the below command would be used in production.
#   And we dont want the app reloading after every change in production. 
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# So instead we do
#           We could override it in the docker-compose.yml file also by adding another flag called as command in yaml type.
#                     command : uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Now our dockerfile is complete and we can build our image.
# We do docker build --help for the different flags
# We will do -t<tag><context(this is the directory where the dockerfile is) for a name to the app. 
# So it will be (docker build -t fastapi .) .The " . " represents the current directory.