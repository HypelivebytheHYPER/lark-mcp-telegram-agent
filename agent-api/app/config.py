import os, json

class Settings:
    # Telegram
    TG_TOKEN = os.getenv("TG_TOKEN")
    TG_API = f"https://api.telegram.org/bot{TG_TOKEN}" if TG_TOKEN else None
    TG_WEBHOOK_URL = os.getenv("TG_WEBHOOK_URL")

    # Agent
    AGENT_JWT_SECRET = os.getenv("AGENT_JWT_SECRET", "change_me")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # MCP modes
    MCP_MODE = os.getenv("MCP_MODE", "base")  # base | stream | sse

    # Streamable HTTP - base path
    LARK_MCP_BASE_URL = os.getenv("LARK_MCP_BASE_URL")
    # Streamable HTTP - explicit stream endpoint
    LARK_MCP_STREAM_URL = os.getenv("LARK_MCP_STREAM_URL")
    # SSE URL (official lark-openapi-mcp)
    LARK_MCP_URL = os.getenv("LARK_MCP_URL", "http://lark-mcp:3000/sse")

    LARK_MCP_AUTH_HEADER = os.getenv("LARK_MCP_AUTH_HEADER")
    LARK_MCP_AUTH_VALUE = os.getenv("LARK_MCP_AUTH_VALUE")

    # === Base Lock (URL prefix) ===
    BASE_LOCK = os.getenv("BASE_LOCK", "true").lower() in ("1","true","yes","y")
    LARK_ALLOWED_BASE_PREFIX = os.getenv("LARK_ALLOWED_BASE_PREFIX")  # e.g., https://anycross.../mcp/lark_base/

    # === Base ID Lock (Bitable base id) ===
    LARK_ALLOWED_BASE_ID = os.getenv("LARK_ALLOWED_BASE_ID")  # e.g., SEkObxgDpaPZbss1T3RlHzamgac

    # === Table Map (name->id) and hard allowlist ===
    TABLE_MAP_JSON = os.getenv("TABLE_MAP_JSON", "{}")
    try:
        TABLE_MAP = json.loads(TABLE_MAP_JSON)
    except Exception:
        TABLE_MAP = {}

    ALLOWED_TABLE_IDS_JSON = os.getenv("ALLOWED_TABLE_IDS_JSON", "[]")
    try:
        ALLOWED_TABLE_IDS = json.loads(ALLOWED_TABLE_IDS_JSON)
    except Exception:
        ALLOWED_TABLE_IDS = []

settings = Settings()
