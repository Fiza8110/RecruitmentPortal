from fastapi import APIRouter,Request,Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import smtplib
from email.mime.text import MIMEText
from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse
import random
from datetime import datetime, timedelta
from pydantic import BaseModel

route = APIRouter()

templates = Jinja2Templates(directory='templates')

route.mount("/static", StaticFiles(directory = "static"), name = "static")

contactus = "contactus.html"

# Route to render home html page
@route.get("/") # / Default path
def home(request: Request): 
    return templates.TemplateResponse("Signup.html", {"request": request})

# ##############----------------------contact us route------------------#####################
# # Route to render contact html page
# @route.get("/contactus")
# def contact(request:Request):
#     return templates.TemplateResponse(contactus, {"request" : request})

# @route.post("/contactus")
# def contact(request:Request, name:str=Form(), email:str=Form(), msg:str=Form()):
#     print(name,email,msg)
#     if name and email and msg:
#         return templates.TemplateResponse(contactus, {"request" : request, "message" : "Successfully Submitted the request"})
#     return templates.TemplateResponse(contactus, {"request" : request})

user_data = {}
# Email settings
MAIL_USERNAME = "c31684901@gmail.com"
MAIL_PASSWORD = "Test@120"  # Use an App Password if 2FA is enabled
MAIL_FROM = "c31684901@gmail.com"
MAIL_PORT = 587
MAIL_SERVER = "smtp.gmail.com"
MAIL_STARTTLS = True
MAIL_SSL_TLS = False
USE_CREDENTIALS = True
VALIDATE_CERTS = True

class ScheduleRequest(BaseModel):
    action: str
    to: str
    date: str = None  # Optional, only for scheduling
    time: str = None  # Optional, only for scheduling
    reason: str = None  # Optional, only for rejection


def send_email(receiver_email, email_content):
    sender_email = "c31684901@gmail.com"
    password = "ualbgpbeswgejwez"  
    subject = "Scheduled Interview"

    # Construct the email message
    message = f"""
    {email_content}

    Best Regards,
    XYZ Company
    """

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # Send email using Gmail SMTP
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(sender_email, password)
            smtp.send_message(msg)
        print(f"Email successfully sent to {receiver_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

# @route.post("/scheduleInterview")  # Fix route decorator
# async def forgot_password_post(request: Request, mail: str = Form(...)):
#     global user_data
#     mail = "m.prakash9977@gmail.com"
#     send_email(mail,"19th Feb 2025, 3:00 PM")

#     # Return success response
#     response_data = {"message": "mail sent successfully"}
#     return JSONResponse(status_code=200, content=response_data)

@route.post("/scheduleInterview")
async def schedule_interview(request: ScheduleRequest):
    # Extract data from request
    action = request.action
    # mail = request.to
    mail = "m.prakash9977@gmail.com"  # Test email address, replace with actual email address when ready
    date = request.date
    time = request.time
    reason = request.reason

    # Print action (button ID)
    print(f"Action: {action}")

    if action == "scheduleInterviewBtn":
        # Send email for interview scheduling
        email_content = f"Your interview is scheduled on {date} at {time}. Please join using the Google Meet link: https://meet.google.com/sample-link"
        send_email(mail, email_content)
    
    elif action == "rejectApplicationBtn":
        # Send rejection email
        email_content = f"Dear candidate, your application has been rejected due to the following reason: {reason}."
        send_email(mail, email_content)

    # Return success response
    response_data = {"message": "Mail sent successfully"}
    return JSONResponse(status_code=200, content=response_data)
    