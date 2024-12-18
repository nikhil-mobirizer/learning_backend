from fastapi import FastAPI, HTTPException, APIRouter, Depends, File, UploadFile
from schemas import ChatRequest, ChatResponse
from services.chat import get_chat_history, convert_chat_history_to_dict, truncate_chat_history, summarize_history, calculate_tokens, save_chat_history
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from database import get_db
from services.auth import get_current_user
import openai 
import os
from models import ChatHistory


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("Missing OpenAI API key. Ensure it's set in the .env file.")



router = APIRouter()

# Constants
MAX_HISTORY_TOKENS = 1000
MODEL = "gpt-4o-mini"

@router.post("/education/chat", response_model=ChatResponse)
async def education_chat(request: ChatRequest, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user["id"]

    existing_chat = db.query(ChatHistory).filter(ChatHistory.user_id == user_id).all()

    # Prepare the context based on the existing history
    if existing_chat:
        chat_history_context = [
            {
                "user": chat.user,
                "bot": chat.bot
            } for chat in existing_chat
        ]
        print("--456--", chat_history_context)

    else:
        chat_history_context = []

    # Summarize or truncate chat history if required
    history_tokens = calculate_tokens(chat_history_context, model=MODEL)
    if history_tokens > MAX_HISTORY_TOKENS:
        truncated_history = truncate_chat_history(chat_history_context, MAX_HISTORY_TOKENS)
        summarized_context = summarize_history(truncated_history)
        print("-----123-----", summarized_context)
    else:
        summarized_context = chat_history_context
        
    # Construct the prompt for the teacher scenario
    prompt = f"""
    ### Educational Insights
    The user has asked an educational question. 

    ### Chat History Summary
    {summarized_context}  

    ### User Query
    {request.user_query}  


    ### Response
    Provide a knowledgeable, concise, and direct answer to the user's educational question.
    The AI knows everything related to education and learning.
    """

    try:
        # Generate response
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[{"role": "system", "content": prompt}],
            max_tokens=500
        )
        bot = response.choices[0].message.content.strip()
        
        # Save the chat history in the database (for both user query and bot response)
        if not existing_chat:  
            new_chat = ChatHistory(
                user_id=user_id,
                user=request.user_query,  
                bot=bot  
            )
            db.add(new_chat)
            db.commit()

        # Save both user query and bot response
        save_chat_history(db, user_id, request.user_query, bot)

        # Return structured response
        return ChatResponse(
            detailed_timeline="Generated based on educational insights.",
            educational_insights=bot 
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {e}")


@router.get("/chat_history")
async def get_chat_history_endpoint(db: Session = Depends(get_db)):
    # Fetch chat history from the database
    chat_history_list = get_chat_history(db)
    
    # Convert the list of ChatHistory objects to readable Python data (list of dictionaries)
    chat_history_data = convert_chat_history_to_dict(chat_history_list)
    
    # Return the chat history data
    return {"chat_history": chat_history_data}
