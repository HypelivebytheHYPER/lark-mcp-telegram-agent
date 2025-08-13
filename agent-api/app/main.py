from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import asyncio
import json
from .config import settings
from .agent import run_task
from .mcp_client import get_mcp_tools
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Lark MCP Agent API", version="6.1")

class AgentRequest(BaseModel):
    prompt: str

class TelegramUpdate(BaseModel):
    update_id: int
    message: dict = None

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Agent API is running"}

@app.get("/mcp/health")
async def mcp_health():
    try:
        tools = await get_mcp_tools()
        return {
            "status": "ok", 
            "tool_count": len(tools),
            "base_lock": settings.BASE_LOCK,
            "allowed_base_id": settings.LARK_ALLOWED_BASE_ID,
            "table_count": len(settings.TABLE_MAP)
        }
    except Exception as e:
        logger.error(f"MCP health check failed: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error", 
                "message": str(e),
                "mcp_config": {
                    "mode": settings.MCP_MODE,
                    "base_url": settings.LARK_MCP_BASE_URL,
                    "stream_url": settings.LARK_MCP_STREAM_URL,
                    "base_lock": settings.BASE_LOCK
                }
            }
        )

@app.get("/mcp/config")
async def mcp_config():
    return {
        "mcp_mode": settings.MCP_MODE,
        "base_url": settings.LARK_MCP_BASE_URL,
        "stream_url": settings.LARK_MCP_STREAM_URL,
        "base_lock": settings.BASE_LOCK,
        "allowed_base_id": settings.LARK_ALLOWED_BASE_ID,
        "table_map": settings.TABLE_MAP
    }

@app.post("/agent/run")
async def run_agent(request: AgentRequest):
    try:
        result = await run_task(request.prompt)
        return {"result": result}
    except Exception as e:
        logger.error(f"Agent run failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/telegram/webhook")
async def telegram_webhook(update: TelegramUpdate, background_tasks: BackgroundTasks):
    """Handle Telegram webhook updates"""
    try:
        if not update.message:
            return {"status": "ok"}
        
        chat_id = update.message.get("chat", {}).get("id")
        text = update.message.get("text", "")
        
        if not text or not chat_id:
            return {"status": "ok"}
        
        # Process in background
        background_tasks.add_task(process_telegram_message, chat_id, text)
        
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Telegram webhook error: {e}")
        return {"status": "error", "message": str(e)}

async def process_telegram_message(chat_id: int, text: str):
    """Process telegram message in background"""
    try:
        # Send typing indicator
        await send_telegram_message(chat_id, "กำลังประมวลผล... ⏳")
        
        # Run agent
        result = await run_task(text)
        
        # Send result
        await send_telegram_message(chat_id, f"✅ เสร็จแล้ว\n\n{result}")
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await send_telegram_message(chat_id, f"❌ เกิดข้อผิดพลาด: {str(e)}")

async def send_telegram_message(chat_id: int, text: str):
    """Send message to Telegram"""
    import aiohttp
    
    if not settings.TG_API:
        logger.error("Telegram token not configured")
        return
        
    url = f"{settings.TG_API}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                if response.status != 200:
                    logger.error(f"Failed to send telegram message: {await response.text()}")
    except Exception as e:
        logger.error(f"Error sending telegram message: {e}")

@app.get("/")
async def root():
    return {
        "message": "Lark MCP Agent API v6.1", 
        "endpoints": ["/health", "/mcp/health", "/agent/run", "/telegram/webhook"]
    }