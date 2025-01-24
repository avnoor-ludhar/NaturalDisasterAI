from typing import Dict
from fastapi import APIRouter, Body, File, HTTPException, UploadFile
from utils.pinecone_db import extract_insights_from_chatlog, generate_embeddings, store_embeddings_in_pinecone, generate_query_embedding, search_in_pinecone
from database.database import get_connection
from datetime import datetime
import re

router = APIRouter()

@router.post("/process_chatlog")
async def process_chatlog(file: UploadFile = File(...), user_id: int = Body(...)):
    # we check user_id
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required.")
    
    # check file type
    if not file.content_type.startswith("text/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a valid text file.")
    
    try:
        chatlog_content = await file.read()
        try:
            chatlog_content = chatlog_content.decode('utf-8')
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="Failed to decode the file. Ensure it is UTF-8 encoded.")
        
        # extract insights from the chatlog
        dict_item_context = extract_insights_from_chatlog(chatlog_content)

        # check if insights extraction was successful
        if not dict_item_context.get("items"):
            raise HTTPException(status_code=400, detail="No insights extracted from the chat log.")

        embeddings = generate_embeddings(dict_item_context)

        chat_id = save_chatlog_to_db(user_id=user_id, chat_title=file.filename)
        if not chat_id:
            raise HTTPException(status_code=500, detail="Error saving chat log to the database.")

        if dict_item_context.get("messages", []) and chat_id:
            dict_item_context = save_message_to_db(dict_item_context, chat_id=chat_id)
            store_embeddings_in_pinecone(
                dict_item_context, embeddings, chat_id=chat_id,
                file=file.filename, user_id=user_id, image_id=0, type="message"
            )

        # if successful provide feedback
        return {
            "message": "Chat log processed successfully",
            "items": dict_item_context["items"],
            "context": dict_item_context["context"],
            "messages": dict_item_context["messages"],
        }

    except Exception as e:
        # error handling
        print(f"Error processing chat log: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the chat log.")



def save_chatlog_to_db(user_id, chat_title):
    conn = get_connection()
    cursor = None

    try:
        query = f"""
            INSERT INTO chat_logs (user_id, chat_title)
            VALUES (%s, %s) RETURNING chat_id
        """
        cursor = conn.cursor()
        cursor.execute(query, (user_id, chat_title))
        chat_id = cursor.fetchone()['chat_id']
        conn.commit()

       
        return chat_id

    except Exception as e:
        print("Error saving chat log to DB:", e)
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def save_message_to_db(dict_item_context, chat_id):
    conn = None
    cursor = None
    messages = dict_item_context["messages"]

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # prepare the SQL query
        query = """
            INSERT INTO messages (chat_id, sender, receiver, message, timestamp)
            VALUES (%s, %s, %s, %s, %s) RETURNING message_id
        """

        for message in messages:
            parsed_message = parse_message(message)
            if parsed_message:
                cursor.execute(query, (
                    chat_id,
                    parsed_message["sender"],
                    parsed_message.get("receiver", None),
                    parsed_message["message"],
                    parsed_message["timestamp"]
                ))

                dict_item_context["ids"].append(cursor.fetchone()["message_id"])
        print('messages length: ', len(messages))
        print('ids length: ', len(dict_item_context["ids"]))



        conn.commit()
        print("All messages have been uploaded successfully!")

        return dict_item_context

    except Exception as e:
        print("Error saving messages to DB:", e)
        return dict_item_context

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def parse_message(message):
    """
    message is parsed to get the timestamp, sender and text

    """
    try:
        pattern = r"^Message: \[([^\]]+)\]\s+(\w+):\s*(.+)$"
        match = re.match(pattern, message)
        if match:
            timestamp, sender, message_text = match.groups()
            return {
                "timestamp": timestamp,
                "sender": sender,
                "message": message_text.strip()
            }

    except Exception as e:
        print(f"Error parsing message: {message}, Error: {e}")

    return None

@router.get("/chatlog_from_chatid/{chatid}")
def chatlog_from_chatid(chatid: int):
    conn = get_connection()
    cursor = None

    try:
        query = f"""
            SELECT
                *
            FROM
                messages
            WHERE
                chat_id = %s
            ORDER BY
                timestamp DESC
        """
        cursor = conn.cursor()
        cursor.execute(query, (chatid,))
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        if not result:
            return {"chatlog": []}  # return emty array if chatlog is we have no result

        return {"chatlog": result}  # otherwise return the result

    except Exception as e:
        print(f"Error fetching all chats of chatid: {chatid}: ", e)
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
