from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import datetime
from jose import jwt
from jose.exceptions import ExpiredSignatureError
from fastapi import Depends,HTTPException
from config.config import REGISTER_COL


#Secret key for jwt token
secret_key = "mykey"


#algorithm to encode jwt token
algorithm = 'HS256'

#Token expiration time
token_expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)

#Creating instance to hash or verify hashed password
pwd_encode = CryptContext(schemes=["bcrypt"], deprecated = "auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')


#Function to verify hash_password in database to plain password in the form
def verify_password(password, hash_password):
    return pwd_encode.verify(password,hash_password)

#Filtering user credentials using email 
def get_user(email: str):
    user = REGISTER_COL.find_one({"email": email})
    return user

#Authenticating the user by checking password #get
def authenticate_user(email : str, password : str = None, form_data : OAuth2PasswordRequestForm = None):
    if form_data:
        email = form_data.username
        password = form_data.password
    
    user = get_user(email)
    if user:
        if verify_password(password, user["password"]):
            return user
        return {"msg" : "password does not match"}
    return {"msg" : "email does not exist"}

#function for creating JWT token
def create_access_token(user_data : dict):

    #copy the user_data to preserve the original data
    encode = user_data.copy()

    #creating expire time for JWT token
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)

    #saving the expire in user_data to encode with jwt token
    encode.update({"exp" : expire})
    
    #Encoding the jwt by combining encode, secret key and algorithm
    jwt_token = jwt.encode(encode, secret_key, algorithm=algorithm)
    return jwt_token

#Fucntion to decode the jwt token 
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        print(token,"get_user")
        if not token:
            return False
        print(token,"im in get_current_user")

        #Decoding jwt token
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])

        #Saving the email in JWT token
        email = payload.get('sub')
        print(email,"im in get_current")

        #get user by email
        user = get_user(email)
        print(user, "im in get_current")
        if user:
            return user
        return None
    except ExpiredSignatureError:
        raise HTTPException(status_code=500, detail="Token has expired")