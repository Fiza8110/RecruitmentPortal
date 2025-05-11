from routes.dashboard import route as dashboard # route -This refers to a FastAPI router object 
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from routes.register import route as register #router object from routes/register.py
from routes.login import route as login #router object from routes/login.py
from routes.home import route as home #router object from routes/home.py

# instance for fastapi 
app = FastAPI() # app is the main app object you'll use to define routes, settings, middlewares, etc.

# To use the html folder
templates = Jinja2Templates(directory='templates') # is used to render HTML templates using the Jinja2 templating engine
 # directory='templates': This tells FastAPI that your HTML files are stored in a folder named templates.
# Mount the static folder for css, js, images
app.mount("/static", StaticFiles(directory = "static"), name = "static")

# Include the routes 
#These lines add route modules to the main FastAPI app
app.include_router(home)
app.include_router(login)
app.include_router(register)
app.include_router(dashboard)