from fastapi import APIRouter, HTTPException
from typing import List
from models import Conversation
from database import collection
from llama2_api import llama2_local_response
from requests.exceptions import RequestException
import httpx
from fastapi import HTTPException

import requests
import time
conversation_router = APIRouter()


def conversation_helper(conversation) -> dict:
    return {
        "id": str(conversation["_id"]),
        "user_id": conversation["user_id"],
        "conversation_id": conversation["conversation_id"],
        "message": conversation["message"],
        "response": conversation["response"],
    }

@conversation_router.get("/api/conversations/{user_id}", response_model=List[Conversation])
async def get_conversations(user_id: str):
    conversations = list(collection.find({"user_id": user_id}))
    return [conversation_helper(conv) for conv in conversations]

@conversation_router.post("/api/conversations", response_model=Conversation)
async def add_conversation(conversation: Conversation):
    new_conversation = conversation.dict()
    result = collection.insert_one(new_conversation)
    new_conversation["_id"] = result.inserted_id
    return conversation_helper(new_conversation)

@conversation_router.post("/api/message/{user_id}", response_model=Conversation)
async def handle_message(user_id: str, conversation_id: str, message: str):
    response = llama2_local_response(message)  
    new_conversation = Conversation(user_id=user_id, conversation_id=conversation_id, message=message, response=response)
    return await add_conversation(new_conversation)
