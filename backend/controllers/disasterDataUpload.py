from typing import Dict
from fastapi import APIRouter, Body, File, HTTPException, UploadFile
from utils.pinecone_db import extract_insights_from_chatlog, generate_embeddings, store_embeddings_in_pinecone, generate_query_embedding, search_in_pinecone
from database.database import get_connection
import re
from pydantic import BaseModel
from datetime import datetime 



router = APIRouter()

class userData(BaseModel):
    City: str
    Province: str
    disasterType: str
    disasterDescription: str
    user_id: int

@router.post("/disaster-upload")
async def disasterUpload(data: userData = Body(...)):
    
    if not data.user_id:
        raise HTTPException(status_code=400, detail="User ID is required.")
    

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Insert into the database
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
    

@router.get("/disaster-posts")
async def disasterUpload():    
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Insert into the database
        query = """
        SELECT * FROM  messages LIMIT 10;
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        return {"data": rows}
        
    except Exception as e:
        print(f"Error inserting trade decision: {e}")
        raise HTTPException(status_code=400, detail="DB error.")
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()