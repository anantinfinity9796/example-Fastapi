# The Procfile is just a file with the command that tells Heroku what is the command that we need to do start the application.
# We can give it a process type and since it is a web application it will be responding to web requests we would use

web : uvicorn app.main:app --host=0.0.0.0 --port=${port:-5000}

# we are not gonna pass in uvicorn app.main:app --reload because we dont want the app to be reloaded on changes because this is production.
# There should be no changes in the application because it is in production.

# We do have to provide the host ip (--host=0.0.0.0), This is just saying that we should be able to respond to request to any IP.
# So whatever IP heroku gives us this is going to accept it.
# Next is the port flag (--port=${port:-5000}) which would run the app on the port provided. If nor specified it runs on default port.
# However in heroku they are actually going to provide us a port. So we dont know what this port is ahead of time but we have to accept it regardless.
# Its actually going to pass it as an environement variable. So anytime we want to accept an EV we do (${PORT}. default is 5000).