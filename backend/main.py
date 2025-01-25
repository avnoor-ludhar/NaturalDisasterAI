from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.disasterDataUpload import router as disaster_data_router
from controllers.authentication import router as authentication_router
from database.database import get_connection

app = FastAPI()

#origins 
origins = [
  "http://localhost:5173", 
]

# cors middleware is added to the server
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# includes the routers for modularized programming, tags are for the /docs route
app.include_router(disaster_data_router, prefix="/api", tags=["disaster_upload"])
app.include_router(authentication_router, prefix="/api", tags=["authentication"])


#just a basic endpoint to test
@app.get("/")
def read_root():
  return {"message": "Hello, World!"}