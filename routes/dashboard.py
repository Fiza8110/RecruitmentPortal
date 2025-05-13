from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from config.config import JObs_COL,APPLICATION_COL
from fastapi import FastAPI, Form, File, UploadFile, Request
from fastapi.responses import RedirectResponse, JSONResponse
from bson import ObjectId
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
import os
import json
from pydantic import BaseModel, EmailStr, Field
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi import Body
route = APIRouter() # route = APIRouter(): Creates a modular group of routes.
class JobUpdate(BaseModel):#Defines validation rules for form data submitted while applying for a job.
    Job_Title: str
    Job_Description: str
    Experience: str
    Skills: str
    Location: str

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token") # Setup for token-based authentication.

templates = Jinja2Templates(directory='templates') # Jinja2Templates: Tells FastAPI to render HTML from the templates directory.

route.mount("/static", StaticFiles(directory = "static"), name = "static") # mount("/static", ...): Serves static files (CSS/JS/images) from /static.

#route to render dashboard html page
@route.get("/dashboard") # This defines an HTTP GET endpoint at the URL path /dashboard
def dashboard(request: Request):#Route handler function 
    jobs_list = list(JObs_COL.find({}))#Fetches all jobs from the MongoDB collection
    return templates.TemplateResponse("Dashboard.html", {"request": request, "jobs_list": jobs_list})#Renders the Dashboard.html page with the list of jobs

# route to render HR dashboard html page
@route.get("/hrDashboard")
def hrDashboard(request: Request):
    return templates.TemplateResponse("HRDashboard.html", {"request": request})

# route to render forgot password html page
@route.get("/forgotPassword")
def forgotPassword(request: Request):
  
    return templates.TemplateResponse("ForgotPassword.html", {"request": request})

# route to render job apply html page
@route.get("/applayJob")
def hrDashboard(request: Request):
  
    return templates.TemplateResponse("JobApply.html", {"request": request})

# applayJob post action
#Ensures that there's a folder ready to store uploaded resumes or files.
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
# base module
class JobApplication(BaseModel):
    job_title: str
    first_name: str
    last_name: str
    email: EmailStr
    mobile: str = Field(..., min_length=10, max_length=15)
    current_employee: str
    company_name: str | None = None
    company_location: str | None = None
    experience:  str | None = None
    current_ctc: str | None = None
    expected_ctc: str | None = None
    notice_period: str | None = None

@route.post("/applyJob")
async def apply_job(
    job_title: str = Form(...),#Indicates this value comes from a form field.
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: EmailStr = Form(...),
    mobile: str = Form(...),
    current_employee: str = Form(...),
    company_name: str = Form(None),
    company_location: str = Form(None),
    experience: str = Form(None),
    current_ctc: str = Form(None),
    expected_ctc: str = Form(None),
    notice_period: str = Form(None),
    resume: UploadFile = File(...),#Used to upload files
    # path:'src/upload'
):
    try:
        # 🔹 Save the resume file
        #  Saves the uploaded resume file in binary mode to the uploads folder.
        resume_path = os.path.join(UPLOAD_DIR, resume.filename)
        print("✅ Received resume file:", resume.filename)
        with open(resume_path, "wb") as f:
            f.write(await resume.read())

        # 🔹 Prepare application data 
       #Create a Dictionary for the Applicant's Data
        application_data = {
            "job_title": job_title,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "mobile": mobile,
            "current_employee": current_employee,
            "company_name": company_name,
            "company_location": company_location,
            "experience":experience,
            "current_ctc": current_ctc,
            "expected_ctc": expected_ctc,
            "notice_period": notice_period,
            "resume": resume_path,  # Save file path, not binary
        }
        #Checks if the email is already in the database.
        testemail = APPLICATION_COL.find_one({"email":email})
        if testemail:
            raise HTTPException(status_code=400, detail="Email already exists.")
        
        # 🔹 Insert into MongoDB
        inserted_data = APPLICATION_COL.insert_one(application_data)
        print("Inserted data", inserted_data)
        application_data["_id"] = str(inserted_data.inserted_id)
        #Returns a JSON response with a success message and all submitted data.
        return JSONResponse(
            content={"message": "Application submitted successfully", "data": application_data}
        )
    
    #Catches any unexpected errors
    except Exception as e:
        print("❌ Internal Server Error:", str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Helper function to convert ObjectId to string
def serialize_objectid(obj):
    if isinstance(obj, ObjectId):# convert it to a string using str(obj).
        return str(obj)
    elif isinstance(obj, dict):#recursively call serialize_objectid on each value of the dictionary
        return {key: serialize_objectid(value) for key, value in obj.items()}
    elif isinstance(obj, list):# recursively process each item in the list.
        return [serialize_objectid(item) for item in obj]
    else:
        return obj

# route to view applications
# @route.get("/viewApplications")
# def viewApplications(request: Request):
#     applications_list = list(APPLICATION_COL.find({}))
#     applications_list = serialize_objectid(applications_list)  # Convert ObjectId to string
#     return templates.TemplateResponse("HRcards.html", {"request": request, "applications_list": applications_list, "show_search": True})
@route.get("/viewApplications")
def view_applications(request: Request):#This function handles the request.
    apps = list(APPLICATION_COL.find({}))#Fetches all applications from the db
    # convert ObjectIds
    for a in apps:
        a["_id"] = str(a["_id"])#uses _id fields of type ObjectId ,converts each _id to a string 
    return templates.TemplateResponse("HRcards.html", {
        "request": request,
        "applications_list": apps,
        "show_search": True
    })

# Function to convert ObjectId to string
def serialize_objectid(obj):
    """ Helper function to convert ObjectId to string for JSON serialization """
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, list):
        return [serialize_objectid(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: serialize_objectid(value) for key, value in obj.items()}
    return obj

# route to view details of a specific application
@route.get("/viewDetails/{application_id}", response_class=HTMLResponse)#response_class=HTMLResponse tells FastAPI to return an HTML page instead of JSON.
async def view_details(request: Request, application_id: str):#Converts the application_id string into a proper ObjectId
    # Fetch the application details from the database using the application_id
    application_data = APPLICATION_COL.find_one({"_id": ObjectId(application_id)})
    
    if application_data:#Converts the application_id string into a proper ObjectId
        application_data = serialize_objectid(application_data)  # Convert ObjectId to string
        return templates.TemplateResponse("ViewApplication.html", {"request": request, "application_data": application_data})
    else:
        return {"message": "Application not found!"}

# to get post new job application
@route.get("/postnewjob")
def hrDashboard(request: Request):

    return templates.TemplateResponse("Postnewjob.html", {"request": request})
@route.get("/joblist") #defines a GET endpoint at the URL path /joblist
# Renders the main dashboard showing all jobs by fetching them from JObs_COL
def joblist(request: Request):#Shows a list of all jobs currently posted.
    jobs_list = list(JObs_COL.find({}))
    return templates.TemplateResponse("Joblist.html", {"request": request, "jobs_list": jobs_list})
@route.get("/jobDetails/{job_id}")
def job_details(request: Request, job_id: str):#{job_id} is a path parameter
    job = JObs_COL.find_one({"_id": ObjectId(job_id)})#ObjectId(job_id) to convert the string into a MongoDB ObjectId.
    if job:
        job = serialize_objectid(job)  # Convert ObjectId to string
        return templates.TemplateResponse("JobDetails.html", {"request": request, "job": job})
    else:
        raise HTTPException(status_code=404, detail="Job not found")
# Route to render edit job page
@route.get("/editJob/{job_id}", response_class=HTMLResponse)
async def edit_job(request: Request, job_id: str):
    job = JObs_COL.find_one({"_id": ObjectId(job_id)})
    if job:
        job = serialize_objectid(job)
        return templates.TemplateResponse("EditJob.html", {"request": request, "job": job})
    else:
        raise HTTPException(status_code=404, detail="Job not found")
# Route to handle editing and saving the job details
@route.put("/updateJob/{job_id}", response_class=JSONResponse)
async def update_job(job_id: str, job_data: JobUpdate = Body(...)):
    # Convert the Pydantic model to a plain dict
    updated_fields = job_data.dict()

    result = JObs_COL.update_one(
        {"_id": ObjectId(job_id)},
        {"$set": updated_fields}
    )

    if result.modified_count:
        # Add the ID to the response so you can verify on the frontend
        response_data = updated_fields.copy()
        response_data["_id"] = job_id
        return JSONResponse({"message": "Job updated successfully", "data": response_data}, status_code=200)

    # If no document was modified, either nothing changed or the ID wasn't found
    raise HTTPException(status_code=400, detail="No job found or no changes made")
# Route to delete a job
@route.delete("/deleteJob/{job_id}", response_class=JSONResponse)
async def delete_job(job_id: str):
    result = JObs_COL.delete_one({"_id": ObjectId(job_id)})
    
    if result.deleted_count:
        return JSONResponse(content={"message": "Job deleted successfully"}, status_code=200)
    else:
        raise HTTPException(status_code=404, detail="Job not found")

# to post new job application post action
@route.post("/postnewjob")
async def hrDashboard(request: Request, data: dict):#Defines an asynchronous function to handle the request.
    print(data)#This prints the received job data to the console for debugging purposes.
    # Python dictionary expected to contain job details
    # Create new job data
    newjob = {#A dictionary newjob is created using values extracted from the data dictionary.
        "Job_Title": data["Job_Title"],
        "Job_Description": data["Job_Description"],
        "Experience": data["Experience"],
        "Skills": data["Skills"],
        "Location": data["Location"]
    }

    # Insert the new job into the database
    result = JObs_COL.insert_one(newjob)

    # Convert ObjectId to string
    newjob['_id'] = str(result.inserted_id)

    # Return JSON response with the new job data
    return JSONResponse(content={"message": "Job posted successfully", "data": newjob}, status_code=200)

from fastapi.responses import FileResponse

# @route.get("/add-candidate")
# def get_add_candidate(request: Request):
#     job_titles = [job["Job_Title"] for job in JObs_COL.find({}, {"_id": 0, "Job_Title": 1})]
#     return templates.TemplateResponse("AddCandidate.html", {"request": request, "job_titles": job_titles})
@route.get("/add-candidate")
def get_add_candidate(request: Request):
    # pull current jobs
    job_titles = [j["Job_Title"] 
                  for j in JObs_COL.find({}, {"_id": 0, "Job_Title": 1})]#This retrieves job titles from the MongoDB JObs_COL collection.
    return templates.TemplateResponse("AddCandidate.html", {
        "request": request,# required for rendering templates.
        "job_titles": job_titles#the list of job titles fetched from the database
    })

@route.post("/add-candidate")
async def post_add_candidate(
    job_title: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: EmailStr = Form(...),
    mobile: str = Form(...),
    current_employee: str = Form(...),
    company_name: str = Form(None),
    company_location: str = Form(None),
    experience: str = Form(None),
    current_ctc: str = Form(None),
    expected_ctc: str = Form(None),
    notice_period: str = Form(None),
    resume: UploadFile = File(...)
):
    # Save resume file
    resume_path = os.path.join(UPLOAD_DIR, resume.filename)
    with open(resume_path, "wb") as f:
        f.write(await resume.read())

    # Prevent duplicate email
    if APPLICATION_COL.find_one({"email": email}):
        raise HTTPException(400, "Email already exists.")

    # Insert into Applications collection
    APPLICATION_COL.insert_one({
        "job_title": job_title,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "mobile": mobile,
        "current_employee": current_employee,
        "company_name": company_name,
        "company_location": company_location,
        "experience": experience,
        "current_ctc": current_ctc,
        "expected_ctc": expected_ctc,
        "notice_period": notice_period,
        "resume_path": resume_path
    })

    # Redirect to HR cards view
    return RedirectResponse(url="/viewApplications", status_code=303)


# route to download a specific application's resume
@route.get("/downloadResume/{application_id}")
async def download_resume(application_id: str):
    application_data = APPLICATION_COL.find_one({"_id": ObjectId(application_id)})
    
    if application_data and "resume" in application_data:
        resume_path = application_data["resume"]
        return FileResponse(resume_path, filename=resume_path.split("/")[-1], media_type="application/pdf")
    
    raise HTTPException(status_code=404, detail="Resume not found")
@route.delete("/deleteApplication/{application_id}")
async def delete_application(application_id: str):
    """
    Delete a job application and its associated resume file
    """
    try:
        # Find the application first
        application = APPLICATION_COL.find_one({"_id": ObjectId(application_id)})
        
        if not application:
            raise HTTPException(status_code=404, detail="Application not found")
        
        # Delete the resume file if it exists
        if "resume" in application and os.path.exists(application["resume"]):
            try:
                os.remove(application["resume"])
            except OSError as e:
                print(f"Error deleting resume file: {e}")
        
        # Delete from database
        result = APPLICATION_COL.delete_one({"_id": ObjectId(application_id)})
        
        if result.deleted_count == 1:
            return {"message": "Application deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete application")
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting application: {str(e)}"
        )
    