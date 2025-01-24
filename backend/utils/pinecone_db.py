import json
from fastapi import HTTPException
from openai import OpenAI
from sentence_transformers import SentenceTransformer
import torch
from transformers import CLIPModel, CLIPProcessor
import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

client = OpenAI(
    base_url="https://api.studio.nebius.ai/v1/",
    api_key=os.environ.get("NEBIUS_API_KEY")
)

clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

index_name = "item-context-embeddings-512"

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=512,
        spec=ServerlessSpec(
            cloud="aws",  
            region="us-east-1"  
        ),
        metric="cosine"  
    )

index = pc.Index(index_name)

result = index.describe_index_stats()
print('inserted vectors: ', result)

def clear_index():
    """
    vectors are cleared from the Pinecone index without deleting the index.
    """
    try:
        index.delete(delete_all=True)
    except Exception as e:
        print(f"Error clearing the index '{index_name}': {e}")

def query_index(query_vector):
    index_stats = index.describe_index_stats()
    print('total vector count: ', index_stats['total_vector_count'])   
    '''
    query_vector = query_vector.tolist()
    response = index.query(query_vector=query_vector, top_k=1)
    '''
    response = index.query(query_vector=query_vector, top_k=1)

    index_stats =  index.describe_index_stats()
    print('total vector count? ', index_stats['total_vector_count'])
    return response


def extract_insights_from_chatlog(chatlog_content):
    completion = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-fast",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that assists users with navigating the hazards of natural disasters and viral diseases"
            },
            {
                "role": "user",
                "content": f"Extract key items, contexts, and messages from this chat log:\n{chatlog_content}\n\nFormat as:\n* Item: [item]\n* Context: [context]\n* Message: [Original Message]"
            }
        ],
        temperature=0
    )
    
    response = json.loads(completion.to_json())
    content = response['choices'][0]['message']['content'].split('*')

    items = []
    context = []
    messages = []

    for i in range(1, len(content) - 2, 3):
        items.append(content[i].strip())
        context.append(content[i+1].strip())
        messages.append(content[i+2].strip())
    
    dict_item_context = {
        "ids": [],
        "items": items,
        "context": context,
        "messages": messages
    }

    return dict_item_context

def generate_embeddings(dict_item_context):
    """
    embeddings are generated for a list of insights using CLIP.
    key phrases are passed in and a list of embeddings is returned
    """
    texts = [item + ' ' + context for item, context in zip(dict_item_context["items"], dict_item_context["context"])]
    
    inputs = clip_processor(text=texts, return_tensors="pt", padding=True, truncation=True)
    
    with torch.no_grad():
        text_embeddings = clip_model.get_text_features(**inputs)

    return text_embeddings


def generate_query_embedding(key_item):
    if not key_item:
        raise HTTPException(status_code=400, detail="Key item is empty.")
    
    inputs = clip_processor(text=[key_item], return_tensors="pt", padding=True, truncation=True)

    with torch.no_grad():
        query_embedding = clip_model.get_text_features(**inputs)

    return query_embedding


def store_embeddings_in_pinecone(dict_item_context, embeddings, chat_id, file, user_id, image_id, type):
    """
    we store embeddings in Pinecone with the metadata.
    dictionary with items and context as well as embeddings and the filename).
    """

    print(file)
    if (type=="message"):
        pinecone_data = [
            {
                "id": file + '_' + str(dict_item_context["ids"][i]),
                "values": embedding.tolist(),  
                "metadata": {
                    "chat_id": chat_id,
                    "message_id": dict_item_context["ids"][i],
                    "type": type,
                    "item": dict_item_context["items"][i],
                    "context": dict_item_context["context"][i],
                    "message": dict_item_context["messages"][i],
                    "user_id": user_id
                }
            }
            for i, embedding in enumerate(embeddings)
        ]
    else:
        pinecone_data = [
            {
                "id": file + '_' + str(image_id),
                "values": embeddings[0].tolist(),  
                "metadata": {
                    "type": type,
                    "image_id": image_id,
                    "user_id": user_id,
                    "items": dict_item_context["items"],
                    "filename": file,
                }
            }
        ]

    try:
        index.upsert(vectors=pinecone_data)
        return pinecone_data
    except Exception as e:
        print(f"Error upserting data to Pinecone: {e}")
        raise

def search_in_pinecone(query_embedding, user_id, type, top_k):
    
    # first we query Pinecone to get the top 5 closest results
    query_vector = query_embedding.cpu().numpy().tolist()
    result = index.query(
        vector=query_vector, 
        top_k=top_k, 
        include_metadata=True, 
        metric="cosine",
        filter={"user_id": user_id, "type": type}
    )
    
    # then parse and return results
    results = []
    
    for match in result['matches']:
        item_metadata = match['metadata']
        results.append(item_metadata)

    return results
