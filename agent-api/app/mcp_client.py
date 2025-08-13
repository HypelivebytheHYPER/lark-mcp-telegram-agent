from langchain_mcp_adapters.client import MultiServerMCPClient
from .config import settings

def _assert_base_lock(url: str):
    if settings.BASE_LOCK and settings.LARK_ALLOWED_BASE_PREFIX:
        if not str(url).startswith(settings.LARK_ALLOWED_BASE_PREFIX):
            raise ValueError(f"Blocked: MCP URL not allowed by BASE_LOCK. url={url}")

def _build_cfg():
    mode = (settings.MCP_MODE or "base").lower()
    cfg = {"transport": None, "url": None}

    if mode == "base":
        cfg["transport"] = "streamable_http"
        cfg["url"] = settings.LARK_MCP_BASE_URL
    elif mode == "stream":
        cfg["transport"] = "streamable_http"
        cfg["url"] = settings.LARK_MCP_STREAM_URL
    else:
        cfg["transport"] = "sse"
        cfg["url"] = settings.LARK_MCP_URL

    if not cfg["url"]:
        raise ValueError("MCP URL not configured for mode=%s" % mode)

    _assert_base_lock(cfg["url"])

    if settings.LARK_MCP_AUTH_HEADER and settings.LARK_MCP_AUTH_VALUE:
        cfg["headers"] = {settings.LARK_MCP_AUTH_HEADER: settings.LARK_MCP_AUTH_VALUE}

    return cfg

async def get_mcp_tools():
    cfg = _build_cfg()
    client = MultiServerMCPClient({"lark": cfg})
    return await client.get_tools()
