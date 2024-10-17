from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment variables from .env
load_dotenv()

# Create a FastAPI instance
app = FastAPI()

# Create a ChatOpenAI model
model = ChatOpenAI(model="gpt-4o")


# Define the request body model
class TranslationRequest(BaseModel):
    message: str
    source_language: str
    target_language: str


@app.post("/translate/")
async def translate(request: TranslationRequest):
    # Prepare messages for the AI model
    messages = [
        SystemMessage(content="Act like an expert in translation"),
        HumanMessage(
            content=f"Translate the following message from {request.source_language} to {request.target_language} and provide only the translation: {request.message}"
        ),
    ]

    # Invoke the model with messages
    result = model.invoke(messages)

    # Return the translation result
    return {"translated_message": result.content}


# To run the application, use the following command in the terminal:
# uvicorn your_script_name:app --reload
