from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from .mcp_client import get_mcp_tools
from .config import settings
from .table_helper import resolve_table
import re

BASE_POLICY = (    f"Use ONLY the Lark MCP base with base_id: {settings.LARK_ALLOWED_BASE_ID}. "

    f"Do NOT reference other bases. "

) if settings.LARK_ALLOWED_BASE_ID else "Use only the provided MCP tools."

TABLE_POLICY = """When the user mentions a table by name, map it to the given table_id and pass that ID in tool arguments.
Allowed tables (name -> id):
{table_map}
If the name is ambiguous or missing, ask the user to pick a table.
If a mapped table_id is not in the hard allowlist, refuse and ask admin.
""".format(table_map=settings.TABLE_MAP)

# Enhanced Task Expert Manager system prompt in Thai with staff greeting capability
TASK_EXPERT_MANAGER_PROMPT = """
คุณเป็น Task Expert Manager ที่เก่งกาจและเฉลียวใจ เหมือนเลขานุการส่วนตัวที่เก่งที่สุด

บทบาทของคุณ:
- จัดการงานให้พนักงานอย่างชาญฉลาด ไม่ต้องถามรายละเอียดเล็กน้อย
- เข้าใจความต้องการจากบริบท และตัดสินใจเลือก table/field ที่เหมาะสมเอง
- ตอบคำถามเกี่ยวกับ Telegram, การตั้งค่า inline, และเครื่องมือต่างๆ ได้
- พูดจาเป็นธรรมชาติ เหมือนมนุษย์ ใช้ภาษาไทยที่เข้าใจง่าย
- ทักทายพนักงานด้วยชื่อที่ถูกต้องจากฐานข้อมูล

การตัดสินใจ Table/Field อัจฉริยะ:
1. เข้าใจ Context และ Intent ของพนักงาน
2. ถ้าเป็นเรื่องงาน/task → เลือก table งาน
3. ถ้าเป็นเรื่องลูกค้า → เลือก table ลูกค้า  
4. ถ้าเป็นเรื่องขาย/การเงิน → เลือก table ขาย
5. ถ้าเป็นเรื่องคน/HR → เลือก table พนักงาน
6. เข้าใจคำย่อ เช่น "ลค" = ลูกค้า, "งน" = งาน, "ขย" = ขาย

การจัดการภาษาธรรมชาติ:
- เข้าใจคำพิมผิด เช่น "งน" → "งาน", "ลค" → "ลูกค้า"
- เข้าใจคำย่อ เช่น "เพิ่ม" → "บันทึกข้อมูลใหม่"
- เข้าใจ context เช่น "คนใหม่" → เพิ่มในตารางพนักงาน
- เข้าใจเวลา เช่น "วันนี้" → วันที่ปัจจุบัน

ตัวอย่างการตัดสินใจ:
- "เพิ่มลูกค้าใหม่" → ใช้ customer table
- "งานวันนี้" → ใช้ task table + filter วันที่วันนี้
- "ยอดขายเดือนนี้" → ใช้ sales table + filter เดือนปัจจุบัน
- "คนใหม่เข้างาน" → ใช้ employee table

สิ่งที่ห้ามทำ:
- ไม่แสดงข้อความเทคนิคให้ผู้ใช้เห็น
- ไม่ถามรายละเอียดเล็กน้อยเกินไป
- ไม่บอกว่าทำอะไรไม่ได้ถ้าเป็นคำถามธรรมดา
- ไม่ถาม table ถ้าเดาได้จาก context

เมื่อไหร่ถึงจะถาม:
- เมื่อข้อความกำกวมมาก เช่น "เพิ่มข้อมูล" โดยไม่บอกประเภท
- เมื่อมีหลาย table เป็นไปได้ และไม่แน่ใจ
- เมื่อเป็นข้อมูลสำคัญ เช่น การลบ หรือแก้ไขข้อมูลใหญ่

สำหรับคำถามเกี่ยวกับ Telegram:
- inline settings: ไปที่ Settings > Privacy and Security > Inline Bots
- การตั้งค่าบอท: ใช้ @BotFather ใน Telegram
- การจัดการ channel/group: เข้า admin panel ของ channel/group นั้น

การทักทายพนักงาน:
- ใช้ MCP tools ค้นหาชื่อพนักงานจาก ChatId ใน Lark Base
- ค้นหาด้วย filter ChatId = {telegram_chat_id} 
- เมื่อพบชื่อแล้ว ให้ทักทายด้วยชื่อที่ถูกต้อง เช่น "สวัสดีครับคุณ {NameStaff}!"
"""

def analyze_user_intent(user_text: str) -> dict:
    """Analyze user intent and suggest appropriate table/action"""
    text = user_text.lower()
    
    # Intent patterns for different table types
    intent_mapping = {
        "customer": {
            "keywords": ["ลูกค้า", "ลค", "customer", "client", "คัสเตอเมอร์"],
            "actions": ["เพิ่มลูกค้า", "ข้อมูลลูกค้า", "แก้ไขลูกค้า"]
        },
        "task": {
            "keywords": ["งาน", "งน", "task", "work", "ทำงาน", "โปรเจค", "project"],
            "actions": ["งานวันนี้", "งานใหม่", "เพิ่มงาน", "สถานะงาน"]
        },
        "sales": {
            "keywords": ["ขาย", "ขย", "sale", "ยอดขาย", "เงิน", "รายได้", "กำไร"],
            "actions": ["ยอดขาย", "สถิติขาย", "รายงานขาย"]
        },
        "employee": {
            "keywords": ["พนักงาน", "คน", "ทีม", "staff", "employee", "hr"],
            "actions": ["คนใหม่", "เพิ่มพนักงาน", "ข้อมูลพนักงาน"]
        },
        "inventory": {
            "keywords": ["สินค้า", "สต็อก", "คลัง", "product", "inventory"],
            "actions": ["เช็คสินค้า", "เพิ่มสินค้า", "สต็อกสินค้า"]
        }
    }
    
    # Check for specific table indicators
    detected_table = None
    confidence = 0
    
    for table_type, patterns in intent_mapping.items():
        score = 0
        # Check keywords
        for keyword in patterns["keywords"]:
            if keyword in text:
                score += 2
        
        # Check action patterns
        for action in patterns["actions"]:
            if action in text:
                score += 3
        
        if score > confidence:
            confidence = score
            detected_table = table_type
    
    # Detect actions
    action_type = None
    if any(word in text for word in ["เพิ่ม", "สร้าง", "ใหม่", "add", "create"]):
        action_type = "create"
    elif any(word in text for word in ["ดู", "แสดง", "ข้อมูล", "รายการ", "list", "show"]):
        action_type = "read"
    elif any(word in text for word in ["แก้", "อัปเดต", "เปลี่ยน", "update", "edit"]):
        action_type = "update"
    elif any(word in text for word in ["ลบ", "delete", "remove"]):
        action_type = "delete"
    
    return {
        "table": detected_table,
        "action": action_type,
        "confidence": confidence,
        "should_ask": confidence < 2  # Ask if confidence is low
    }

def normalize_user_text(text: str) -> str:
    """Normalize common typos and abbreviations in Thai"""
    normalizations = {
        "งน": "งาน",
        "ลค": "ลูกค้า", 
        "ขย": "ขาย",
        "ขข": "ข้อมูล",
        "เพิ่ม": "เพิ่มข้อมูล",
        "ดู": "ดูข้อมูล",
        "ลบ": "ลบข้อมูล"
    }
    
    normalized = text
    for old, new in normalizations.items():
        normalized = normalized.replace(old, new)
    
    return normalized

async def get_staff_name_by_chat_id(chat_id: str) -> str:
    """Get staff name from Lark Base using Telegram chat ID"""
    try:
        # Use MCP tools to search for staff name by chat_id
        # This will search in the configured tables for ChatId field
        tools = await get_mcp_tools()
        
        # Build a search query to find staff by chat_id
        # This assumes there's a table with ChatId and NameStaff fields
        search_hint = f"ค้นหาพนักงานที่มี ChatId = {chat_id} และดึงชื่อ NameStaff มาให้"
        return search_hint
        
    except Exception as e:
        return ""

def extract_ai_response_only(messages) -> str:
    """Extract only the final AI response, filtering out system messages and intermediate steps"""
    if not messages:
        return ""
    
    # Get the last AIMessage from the conversation
    ai_responses = []
    for msg in reversed(messages):
        if isinstance(msg, AIMessage):
            content = getattr(msg, "content", "")
            if content and content.strip():
                # Skip if it looks like a tool call or system response
                if not any(pattern in content for pattern in [
                    "I'll", "I will", "Let me", "I need to", "I should",
                    "Based on", "According to", "The result", "Here's what",
                    "tool_calls", "function_call", "mcp__", "base_id",
                    "table_id", "app_token"
                ]):
                    ai_responses.append(content)
                    break
    
    return ai_responses[0] if ai_responses else ""

def filter_response(raw_response: str) -> str:
    """Filter out technical system messages from user-facing responses"""
    if not raw_response:
        return "ไม่พบข้อมูล กรุณาลองใหม่อีกครั้ง"
    
    lines = raw_response.split('\n')
    filtered_lines = []
    
    # Patterns to hide from users
    skip_patterns = [
        "Use only the provided MCP tools",
        "Use ONLY the Lark MCP base",
        "Allowed tables (name -> id):",
        "If the name is ambiguous or missing",
        "If a mapped table_id is not in the hard allowlist",
        "When the user mentions a table by name",
        "table_id=",
        "base_id:",
        "Use table_id",
        "MCP tools",
        "Do NOT reference other bases",
        "SystemMessage",
        "HumanMessage",
        "AIMessage",
        "I'll help you",
        "I will search",
        "Let me search",
        "Based on the search",
        "According to",
        "The result shows",
        "mcp__",
        "app_token",
        "tool_calls",
        "function_call"
    ]
    
    for line in lines:
        # Skip lines that contain technical patterns
        should_skip = any(pattern in line for pattern in skip_patterns)
        
        # Skip lines that look like system messages or debug info
        if line.strip().startswith(('System:', 'DEBUG:', 'Error:', 'Tool:', 'Human:', 'AI:', 'I\'ll', 'I will', 'Let me', 'Based on')):
            should_skip = True
            
        # Skip empty lines and lines with only technical symbols
        if not line.strip() or line.strip() in ['(no content)', '---', '***']:
            should_skip = True
            
        if not should_skip:
            filtered_lines.append(line)
    
    # Join the filtered content
    result = '\n'.join(filtered_lines).strip()
    
    # If result is empty or too technical, provide a friendly response
    if not result or len(result) < 10:
        return "เสร็จสิ้นแล้วครับ! มีอะไรให้ช่วยอีกไหม?"
    
    return result

def make_response_natural(response: str, staff_name: str = "") -> str:
    """Make the response more natural and human-like in Thai with staff greeting"""
    if not response:
        return "ขออภัย ไม่สามารถประมวลผลได้ กรุณาลองใหม่อีกครั้ง"
    
    # Add staff name if available
    natural_response = response
    
    # Add personalized greeting if staff name is provided
    if staff_name and staff_name.strip():
        if not any(name in response for name in [staff_name, "คุณ"]):
            natural_response = f"สวัสดีครับคุณ{staff_name}! " + natural_response
    
    # Add appropriate Thai politeness if missing
    if not any(word in natural_response.lower() for word in ['ครับ', 'ค่ะ', 'นะครับ', 'นะคะ']):
        natural_response += " ครับ"
    
    # Make it more conversational
    if "เสร็จ" in natural_response and "แล้ว" not in natural_response:
        natural_response = natural_response.replace("เสร็จ", "เสร็จแล้ว")
    
    return natural_response

async def build_agent(user_text: str = "", chat_id: str = ""):

    tools = await get_mcp_tools()

    model = ChatOpenAI(
      model="gpt-5-mini",
      api_key=settings.OPENAI_API_KEY,
      temperature=0.1,  # Make responses more consistent
      model_kwargs={
          "reasoning_effort": "medium",  # Options: minimal, low, medium, high
          "verbosity": "medium"          # Options: low, medium, high
      }
  )

    # Enhanced prompt with chat_id context for staff lookup
    enhanced_prompt = TASK_EXPERT_MANAGER_PROMPT
    if chat_id:
        enhanced_prompt += f"\n\nปัจจุบันผู้ใช้มี Telegram Chat ID: {chat_id} - ใช้ข้อมูลนี้ในการค้นหาชื่อพนักงานจากฐานข้อมูล"

    sys = SystemMessage(content=enhanced_prompt)

    messages = [sys]
    name, tid = resolve_table(user_text)

    if tid:
        # Create a more natural hint message
        hint = SystemMessage(content=f"ใช้ตาราง '{name}' (ID: {tid}) สำหรับการทำงานกับฐานข้อมูล")
        messages.append(hint)

    agent = create_react_agent(model, tools)

    return agent


async def run_task(prompt: str, chat_id: str = ""):
    # Normalize user input and analyze intent
    normalized_prompt = normalize_user_text(prompt)
    intent_analysis = analyze_user_intent(normalized_prompt)

    agent = await build_agent(normalized_prompt, chat_id)
    
    # Enhanced prompt with chat_id context and intelligent guidance
    enhanced_prompt = TASK_EXPERT_MANAGER_PROMPT
    if chat_id:
      enhanced_prompt += f"""

  ขั้นตอนสำคัญ - ค้นหาชื่อพนักงาน:
  1. ใช้ MCP tools ค้นหาใน TEAM table (table_id: tbljNtxUp5aB5ID7)
  2. ค้นหาด้วย filter: chat_id = {chat_id}  
  3. ดึงข้อมูล name field มา
  4. ทักทายด้วยชื่อจริง เช่น "สวัสดีครับคุณ[ชื่อ]!"

  ตัวอย่าง MCP search:
  {{
      "filter": {{
          "conditions": [
              {{
                  "field_name": "chat_id",
                  "operator": "is",
                  "value": ["{chat_id}"]
              }}
          ],
          "conjunction": "and"
      }},
      "field_names": ["name", "chat_id"],
      "table_id": "tbljNtxUp5aB5ID7"
  }}
  """
    # Add intelligent table guidance based on intent analysis
    if intent_analysis["table"] and intent_analysis["confidence"] >= 2:
        enhanced_prompt += f"\n\nจากการวิเคราะห์: ควรใช้ตาราง {intent_analysis['table']} สำหรับคำขอนี้ (confidence: {intent_analysis['confidence']})"
        if intent_analysis["action"]:
            enhanced_prompt += f" และดำเนินการ {intent_analysis['action']}"
    
    messages = [SystemMessage(content=enhanced_prompt)]
    
    # Try existing table resolution first, then fall back to intelligent analysis
    name, tid = resolve_table(normalized_prompt)
    if tid:
        hint = SystemMessage(content=f"ใช้ตาราง '{name}' (ID: {tid}) สำหรับการทำงานนี้")
        messages.append(hint)
    elif intent_analysis["table"] and not intent_analysis["should_ask"]:
        # Use intelligent table suggestion when confidence is high
        hint = SystemMessage(content=f"ตามการวิเคราะห์ ควรใช้ตาราง {intent_analysis['table']} สำหรับงานนี้")
        messages.append(hint)
    
    messages.append({"role": "user", "content": normalized_prompt})

    result = await agent.ainvoke({"messages": messages}, debug=False)

    # Extract only the final AI response, not intermediate steps or system messages
    ai_response = extract_ai_response_only(result.get("messages", []))
    
    # Try to extract staff name from the response (if the agent found it)
    staff_name = ""
    # Look for patterns like "คุณ{name}" or similar
    name_pattern = r'คุณ([^\s\!\?\\.]+)'
    name_match = re.search(name_pattern, ai_response)
    if name_match:
        staff_name = name_match.group(1)
    
    # Filter out technical messages and make response natural
    filtered_response = filter_response(ai_response)
    natural_response = make_response_natural(filtered_response, staff_name)
    
    return natural_response

# Enhanced run_task function that can be called with chat_id
async def run_task_with_greeting(prompt: str, telegram_chat_id: str = ""):
    """Main function to run task with personalized greeting based on chat_id"""
    return await run_task(prompt, telegram_chat_id)
