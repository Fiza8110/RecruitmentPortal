from routes.dashboard import route as dashboard # route -This refers to a FastAPI router object 
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from routes.register import route as register #router object from routes/register.py
from routes.login import route as login #router object from routes/login.py
from routes.home import route as home #router object from routes/home.py
from routes.resetpassword import reset_router# instance for fastapi 
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
import os
app = FastAPI() # app is the main app object you'll use to define routes, settings, middlewares, etc.

# To use the html folder
templates = Jinja2Templates(directory='templates') # is used to render HTML templates using the Jinja2 templating engine
 # directory='templates': This tells FastAPI that your HTML files are stored in a folder named templates.
# Mount the static folder for css, js, images
app.mount("/static", StaticFiles(directory = "static"), name = "static")
port = int(os.environ.get("PORT", 8000))  # Use 8000 locally, use PORT on Render
uvicorn.run("main:app", host="0.0.0.0", port=port)
# Include the routes 
# Add this middleware (choose your own secret key)
app.add_middleware(SessionMiddleware, secret_key="your-random-secret")
#These lines add route modules to the main FastAPI app
app.include_router(home)
app.include_router(login)
app.include_router(register)
app.include_router(reset_router)
app.include_router(dashboard)
