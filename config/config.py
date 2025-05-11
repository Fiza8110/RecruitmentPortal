import pymongo


#Establing mongodb server
MONGO_URI = f'mongodb+srv://c31684901:Job_portal@cluster0.us9wx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

#instance for mongodb server
Client = pymongo.MongoClient(MONGO_URI)

#Creatng db 
DB = Client["HrPortal"]

#Creating users collection to store the user credentials
REGISTER_COL = DB["USERS"]

JObs_COL=DB["Jobs"]
APPLICATION_COL=DB["Applications"]
