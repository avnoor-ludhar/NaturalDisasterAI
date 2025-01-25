from typing import Dict
from fastapi import APIRouter, Body, HTTPException
from database.database import get_connection
from pydantic import BaseModel
from datetime import datetime 

# Gets a router to modularize the code
router = APIRouter()

# Pydantic model for the data from the front-end form
class userData(BaseModel):
    City: str
    Province: str
    disasterType: str
    disasterDescription: str
    user_id: int

#post route to upload the disaster input, checks for the user_id for securing the backend
@router.post("/disaster-upload")
async def disasterUpload(data: userData = Body(...)):
    
    if not data.user_id:
        raise HTTPException(status_code=400, detail="User ID is required.")
    

    #opens a connection to the database
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Insertion logic for the database
        query = """
        INSERT INTO messages (user_id, disaster, content, city, province, curr_time)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        values = (
            data.user_id,
            data.disasterType,
            data.disasterDescription,
            data.City,
            data.Province,
            datetime.now()
        )
        cursor.execute(query, values)
        conn.commit()

        return {"Result": "Success on disaster data upload to db"}
        
    except Exception as e:
        print(f"Error inserting data: {e}")
        raise HTTPException(status_code=400, detail="DB error.")
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    

#route to return 10 retu
@router.get("/disaster-posts")
async def disasterUpload():    
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Gets data from the database ordering by the date
        query = """
        SELECT * FROM  messages ORDER BY curr_time DESC LIMIT 10;
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        return {"data": rows}
        
    except Exception as e:
        print(f"Error inserting disaster information: {e}")
        raise HTTPException(status_code=400, detail="DB error.")
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()