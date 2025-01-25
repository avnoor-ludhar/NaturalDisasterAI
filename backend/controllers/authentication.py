from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Union
from passlib.hash import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from database.database import get_connection

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
'''
import secrets
print(secrets.token_hex(32)) #set SECRET_KEY in .env = to this
'''
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

conn = get_connection()

users_db = {
  "m@example.com": {
    "password": bcrypt.hash("securepassword")  
  }
}

class LoginInput(BaseModel):
  email: str
  password: str

class Token(BaseModel):
  user_id: int
  email: str
  token: str
  expires_at: str

router = APIRouter()

def verify_password(plain_password: str, hashed_password: str) -> bool:
  return bcrypt.verify(plain_password, hashed_password)

#creates a token which expires in the number of minutes described in the environment variables
def create_access_token(email: str):
  expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode = {"sub": email, "exp": expire}
  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/user/login", response_model=Token)
async def login(login_input: LoginInput):
  """
  User authentication and JWT token is generated
  takes email and password and returns a JWT token
  """
  with conn.cursor() as cursor:
    # search the database for the user
    cursor.execute("SELECT password_hash FROM users WHERE email = %s;", (login_input.email,))
    user = cursor.fetchone()
    
    cursor.execute("SELECT user_id FROM users WHERE email = %s;", (login_input.email,))
    user_id_result = cursor.fetchone()

  if not user or not verify_password(login_input.password, user["password_hash"]):
    raise HTTPException(status_code=401, detail="Invalid email or password")

  token = create_access_token(email=login_input.email)
  expires_at = (datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).isoformat()

  return {"user_id": user_id_result['user_id'], "email": login_input.email, "token": token, "expires_at": expires_at}


#Here is a 
def add_user(username: str, email: str, password: str):
  password_hash = bcrypt.hash(password)

  with conn.cursor() as cursor:
    try:
      cursor.execute("""
      INSERT INTO users (username, email, password_hash)
      VALUES (%s, %s, %s);
      """, (username, email, password_hash))
      conn.commit()
      print("User added successfully!")
    except Exception as e:
      print(f"Error: {e}")
      conn.rollback()



@router.post("/user/register", response_model=Token)
async def signup(login_input: LoginInput):
  """
  Signs up a new user and logs them in.

  Takes email and password and returns a JWT token
  """
  # password is hashed
  password_hash = bcrypt.hash(login_input.password)

  conn = get_connection()
  cursor = conn.cursor()

  try:
    # add the new user to the database
    cursor.execute("""
    INSERT INTO users (username, email, password_hash)
    VALUES (%s, %s, %s);
    """, (login_input.email.split('@')[0], login_input.email, password_hash))
    conn.commit()

    cursor.execute("SELECT user_id FROM users WHERE email = %s;", (login_input.email,))
    user_id = cursor.fetchone()
     # new user token is created
    token = create_access_token(email=login_input.email)
    
    return {"user_id": user_id, "email": login_input.email, "token": token}

  except Exception as e:
    #checks if it violates the unique constraint in the email else generic error
    if "unique constraint" in str(e).lower():
      raise HTTPException(status_code=400, detail="Email already in use.")
    raise HTTPException(status_code=500, detail="An error occurred while signing up.")
  finally:
    cursor.close()
    conn.close()


@router.get("/user/session")
async def check_session(request: Request):
  """
  This checks if the user has an active session based on the token provided in the headers.
  If the session is valid the user details are returned
  """
  
  conn = get_connection()
  cursor = conn.cursor()
  #gests the authorization token from the request headers 
  auth_header = request.headers.get("Authorization")
  if not auth_header or not auth_header.startswith("Bearer "):
    raise HTTPException(status_code=401, detail="Token missing or invalid")

  token = auth_header.split(" ")[1]  # Get the token part

  try:
    # token is checked against key to ensure no tampering
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email = payload.get("sub")

    if not email:
      raise HTTPException(status_code=401, detail="Invalid token")

    cursor.execute("SELECT email FROM users WHERE email = %s", (email,))     # checking db to see if user exists

    user = cursor.fetchone()

    if not user:
      raise HTTPException(status_code=401, detail="User does not exist")

    cursor.close()
    conn.close()
    return {"email": user["email"]}
    
  except JWTError:
    raise HTTPException(status_code=401, detail="Invalid or expired token")
    