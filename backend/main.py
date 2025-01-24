from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.chatLogProcessing import router as chatlog_upload_router
from controllers.disasterDataUpload import router as disaster_data_router
from controllers.nebius import router as nebius_router
from controllers.authentication import router as authentication_router
from database.database import get_connection
from utils.pinecone_db import clear_index

app = FastAPI()

origins = [
  "http://localhost:5173", 
  "https://yourfrontenddomain.com",  
]

# cors middleware is added
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


app.include_router(disaster_data_router, prefix="/api", tags=["disaster_upload"])
app.include_router(chatlog_upload_router, prefix="/api", tags=["chatlog_upload"])
app.include_router(nebius_router, prefix="/api", tags=["nebius"])
app.include_router(authentication_router, prefix="/api", tags=["authentication"])


conn = get_connection()
cursor = conn.cursor()


@app.get("/")
def read_root():
  return {"message": "Hello, World!"}

#clear_index()