import json
from models import ChatHistory
import tiktoken
from typing import List
import openai
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

# Constants
MAX_HISTORY_TOKENS = 1000
MODEL = "gpt-4"

def calculate_tokens(text, model: str = MODEL) -> int:
    # Ensure text is a string if it's a list of objects
    if isinstance(text, list):
        # If text is a list (e.g., a list of ChatHistory objects), extract the relevant text from each item
        combined_text = " ".join([str(item.text) if hasattr(item, 'text') else str(item) for item in text])
    else:
        # If it's already a string, just use it directly
        combined_text = str(text)
    
    # Now pass the combined text to tiktoken for encoding
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(combined_text))



# Summarize history
def summarize_history(chat_history_context: List[ChatHistory]) -> str:
    full_text = "\n".join([f"User: {m['user']}\nBot: {m['bot']}" for m in chat_history_context])
    prompt = f"Summarize the following conversation for context:\n\n{full_text}\n\nProvide a concise summary:"
    
    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[{"role": "system", "content": prompt}],
            max_tokens=200
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error during summarization: {e}")
        return "Summary could not be generated due to an error."

# Truncate history
def truncate_chat_history(chat_history_context: List[ChatHistory], max_tokens: int) -> List[ChatHistory]:
    total_tokens = 0
    truncated_history = []
    for message in reversed(chat_history_context):
        message_tokens = calculate_tokens(message['user'] + message['bot'], model=MODEL)
        if total_tokens + message_tokens > max_tokens:
            break
        truncated_history.insert(0, message)
        total_tokens += message_tokens
    return truncated_history



def save_chat_history(db: Session, user_id: str, user_message: str, bot_response: str):
    new_chat = ChatHistory(
        user_id=user_id,
        user=user_message,
        bot=bot_response
    )
    db.add(new_chat)
    db.commit()

def get_chat_history(db: Session):
    return db.query(ChatHistory).all()

def convert_chat_history_to_dict(chat_history_list):
    # Convert each ChatHistory object into a dictionary
    chat_history_data = [
        {
            "id": chat.id,
            "user_id": chat.user_id,
            "user": chat.user,
            "bot": chat.bot,
            "timestamp": chat.timestamp.isoformat()  # Format the datetime as string
        }
        for chat in chat_history_list
    ]
    return chat_history_data
