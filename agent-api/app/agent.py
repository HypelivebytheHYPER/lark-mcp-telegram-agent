from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from .mcp_client import get_mcp_tools
from .config import settings
from .table_helper import resolve_table

BASE_POLICY = (    f"Use ONLY the Lark MCP base with base_id: {settings.LARK_ALLOWED_BASE_ID}. "

    f"Do NOT reference other bases. "

) if settings.LARK_ALLOWED_BASE_ID else "Use only the provided MCP tools."

TABLE_POLICY = """When the user mentions a table by name, map it to the given table_id and pass that ID in tool arguments.
Allowed tables (name -> id):
{table_map}
If the name is ambiguous or missing, ask the user to pick a table.
If a mapped table_id is not in the hard allowlist, refuse and ask admin.
""".format(table_map=settings.TABLE_MAP)

async def build_agent(user_text: str = ""):

    tools = await get_mcp_tools()

    model = ChatOpenAI(
        model="gpt-4o",
        api_key=settings.OPENAI_API_KEY
    )

    sys = SystemMessage(content=(BASE_POLICY + "\n\n" + TABLE_POLICY))

    messages = [sys]
    name, tid = resolve_table(user_text)

    if tid:
        hint = SystemMessage(content=f"Use table_id={tid} (name='{name}') for Bitable-related actions.")
        messages.append(hint)

    agent = create_react_agent(model, tools)

    return agent



async def run_task(prompt: str):

    agent = await build_agent(prompt)
    
    messages = [SystemMessage(content=(BASE_POLICY + "\n\n" + TABLE_POLICY))]
    name, tid = resolve_table(prompt)
    if tid:
        hint = SystemMessage(content=f"Use table_id={tid} (name='{name}') for Bitable-related actions.")
        messages.append(hint)
    
    messages.append({"role": "user", "content": prompt})

    result = await agent.ainvoke({"messages": messages}, debug=False)

    msgs = [getattr(m, "content", "") for m in result.get("messages", []) if getattr(m, "content", "")]

    return "\n".join(msgs) or "(no content)"

