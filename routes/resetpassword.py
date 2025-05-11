from fastapi import APIRouter, Request, HTTPException, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, RedirectResponse
from itsdangerous import URLSafeTimedSerializer
from passlib.context import CryptContext
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from config import REGISTER_COL
import pymongo

route = APIRouter()

templates = Jinja2Templates(directory="templates")

# Password reset configuration
SECRET_KEY = "your-secure-secret-key-change-in-production"  # Should be long and random
SECURITY_PASSWORD_SALT = "your-password-salt-change-in-production"
RESET_TOKEN_EXPIRE_HOURS = 24

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt=SECURITY_PASSWORD_SALT)

def verify_reset_token(token, expiration=RESET_TOKEN_EXPIRE_HOURS*3600):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=SECURITY_PASSWORD_SALT,
            max_age=expiration
        )
        return email
    except Exception:
        return None

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def send_email(receiver_email, subject, email_content):
    sender_email = "c31684901@gmail.com"
    password = "ualbgpbeswgejwez"  

    message = f"""
    {email_content}

    Best Regards,
    XYZ Company
    """

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(sender_email, password)
            smtp.send_message(msg)
        print(f"Email successfully sent to {receiver_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

@route.get("/forgot-password")
def forgot_password_page(request: Request):
    return templates.TemplateResponse("forgot_password.html", {"request": request})

@route.post("/forgot-password")
async def forgot_password(request: Request, email: str = Form(...)):
    # Check if email exists in database
    user = REGISTER_COL.find_one({"email": email})
    if not user:
        return templates.TemplateResponse(
            "forgot_password.html",
            {"request": request, "message": "Email not found in our system"},
            status_code=404
        )
    
    token = generate_reset_token(email)
    reset_url = f"http://localhost:8000/reset-password?token={token}"
    
    email_content = f"""
    To reset your password, click on the following link:
    {reset_url}
    
    This link will expire in {RESET_TOKEN_EXPIRE_HOURS} hours.
    
    If you didn't request a password reset, please ignore this email.
    """
    
    send_email(email, "Password Reset Request", email_content)
    
    return templates.TemplateResponse(
        "forgot_password.html",
        {"request": request, "message": "Password reset link sent to your email"}
    )

@route.get("/reset-password")
async def show_reset_password_form(request: Request, token: str):
    email = verify_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    return templates.TemplateResponse(
        "reset_password.html",
        {"request": request, "token": token}
    )

@route.post("/reset-password")
async def reset_password(
    request: Request,
    token: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...)
):
    if new_password != confirm_password:
        return templates.TemplateResponse(
            "reset_password.html",
            {"request": request, "token": token, "error": "Passwords don't match"},
            status_code=400
        )
    
    email = verify_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    # Update password in database
    hashed_password = get_password_hash(new_password)
    result = REGISTER_COL.update_one(
        {"email": email},
        {"$set": {"password": hashed_password}}
    )
    
    if result.modified_count == 1:
        return RedirectResponse(url="/login", status_code=303)
    else:
        raise HTTPException(status_code=500, detail="Failed to update password")