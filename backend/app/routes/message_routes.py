"""
Message Routes
API endpoints for message operations
"""
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from typing import List
from pydantic import BaseModel
from app.controllers.message_controller import MessageController
from app.models.message import Message
from app.dependencies import get_message_controller

router = APIRouter()


class SendMessageRequest(BaseModel):
    """Request model for sending a message"""
    chat_id: str
    content: str


class SendMessageResponse(BaseModel):
    """Response model for sending a message"""
    user_message: Message
    bot_message: Message


@router.post("/send", response_model=SendMessageResponse)
async def send_message(
    request: SendMessageRequest,
    controller: MessageController = Depends(get_message_controller)
):
    """Send a message and get bot response"""
    try:
        result = await controller.send_message(request.chat_id, request.content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chat/{chat_id}", response_model=List[Message])
async def get_chat_messages(
    chat_id: str,
    controller: MessageController = Depends(get_message_controller)
):
    """Get all messages for a chat"""
    try:
        messages = await controller.get_chat_messages(chat_id)
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload-pdf")
async def upload_pdf(
    chat_id: str = Form(...),
    file: UploadFile = File(...),
    controller: MessageController = Depends(get_message_controller)
):
    """Upload a PDF file and extract its content"""
    try:
        print(f"[PDF UPLOAD] Received upload for chat_id: {chat_id}")
        
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Read file content
        content = await file.read()
        
        # Extract text from PDF using the controller's chatbot service instance
        text = controller.chatbot_service.extract_pdf_text(content)
        
        if not text:
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
        # Save PDF content for this chat session
        controller.chatbot_service.save_pdf_content(chat_id, text)
        
        print(f"[PDF UPLOAD] Saved PDF content for chat_id: {chat_id}, text length: {len(text)}")
        print(f"[PDF UPLOAD] Current PDF storage keys: {list(controller.chatbot_service.pdf_content.keys())}")
        
        return {
            "message": "PDF uploaded successfully",
            "filename": file.filename,
            "characters": len(text),
            "preview": text[:200] + "..." if len(text) > 200 else text
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{message_id}", response_model=Message)
async def get_message(
    message_id: str,
    controller: MessageController = Depends(get_message_controller)
):
    """Get a specific message by ID"""
    message = await controller.get_message(message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message
