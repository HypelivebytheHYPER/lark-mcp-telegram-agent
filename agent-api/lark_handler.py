# Comprehensive Lark Operations Handler
# Integrated with agent system for natural Thai workplace interactions

import asyncio
import json
from typing import Dict, List, Any, Optional
import random
import logging

logger = logging.getLogger(__name__)

class LarkOperationsHandler:
    def __init__(self, mcp_client):
        self.mcp = mcp_client
        self.base_id = "SEkObxgDpaPZbss1T3RlHzamgac"  # Your base ID
        
    async def handle_lark_command(self, chat_id: int, command: str, params: Dict = None) -> str:
        """Route Lark commands to appropriate handlers"""
        try:
            command_lower = command.lower()
            
            # Table Operations
            if "create table" in command_lower or "สร้างตาราง" in command_lower:
                return await self.create_table(params or {})
            elif "list tables" in command_lower or "ดูตาราง" in command_lower:
                return await self.list_tables()
            elif "delete table" in command_lower or "ลบตาราง" in command_lower:
                return await self.delete_table(params or {})
            elif "update table" in command_lower or "แก้ไขตาราง" in command_lower:
                return await self.update_table(params or {})
                
            # Field Operations
            elif "create field" in command_lower or "สร้างฟิลด์" in command_lower:
                return await self.create_field(params or {})
            elif "list fields" in command_lower or "ดูฟิลด์" in command_lower:
                return await self.list_fields(params or {})
            elif "delete field" in command_lower or "ลบฟิลด์" in command_lower:
                return await self.delete_field(params or {})
            elif "update field" in command_lower or "แก้ไขฟิลด์" in command_lower:
                return await self.update_field(params or {})
                
            # Record Operations
            elif "create record" in command_lower or "สร้างข้อมูล" in command_lower:
                return await self.create_record(params or {})
            elif "batch create" in command_lower or "สร้างหลายรายการ" in command_lower:
                return await self.batch_create_records(params or {})
            elif "update record" in command_lower or "แก้ไขข้อมูล" in command_lower:
                return await self.update_record(params or {})
            elif "batch update" in command_lower or "แก้ไขหลายรายการ" in command_lower:
                return await self.batch_update_records(params or {})
            elif "delete record" in command_lower or "ลบข้อมูล" in command_lower:
                return await self.delete_record(params or {})
            elif "batch delete" in command_lower or "ลบหลายรายการ" in command_lower:
                return await self.batch_delete_records(params or {})
            elif "search records" in command_lower or "ค้นหาข้อมูล" in command_lower:
                return await self.search_records(params or {})
                
            # Contact Operations
            elif "get user" in command_lower or "ดูข้อมูลผู้ใช้" in command_lower:
                return await self.get_user_info(params or {})
            elif "list users" in command_lower or "ดูรายชื่อผู้ใช้" in command_lower:
                return await self.list_users(params or {})
            elif "get department" in command_lower or "ดูแผนก" in command_lower:
                return await self.get_department_info(params or {})
            elif "list departments" in command_lower or "ดูรายชื่อแผนก" in command_lower:
                return await self.list_departments(params or {})
                
            # Document Operations
            elif "get document" in command_lower or "ดูเอกสาร" in command_lower:
                return await self.get_document(params or {})
            elif "update document" in command_lower or "แก้ไขเอกสาร" in command_lower:
                return await self.update_document(params or {})
            elif "get document content" in command_lower or "ดูเนื้อหาเอกสาร" in command_lower:
                return await self.get_document_content(params or {})
                
            # Messaging Operations
            elif "create chat" in command_lower or "สร้างแชท" in command_lower:
                return await self.create_chat(params or {})
            elif "list chats" in command_lower or "ดูแชท" in command_lower:
                return await self.list_chats()
            elif "send message" in command_lower or "ส่งข้อความ" in command_lower:
                return await self.send_im_message(params or {})
            elif "get chat members" in command_lower or "ดูสมาชิกแชท" in command_lower:
                return await self.get_chat_members(params or {})
                
            # Wiki Operations
            elif "get wiki" in command_lower or "ดู wiki" in command_lower:
                return await self.get_wiki_node(params or {})
                
            else:
                return await self.send_help_message()
                
        except Exception as e:
            logger.error(f"Lark command error: {e}")
            return await self.handle_operation_error(str(e), command)

    # === TABLE OPERATIONS ===
    async def create_table(self, params: Dict) -> str:
        """Create a new table in Lark Base"""
        try:
            result = await self.mcp.call_tool("mcp__lark-tenant__bitable_v1_appTable_create", {
                "data": {
                    "table": {
                        "name": params.get("name", "New Table"),
                        "default_view_name": params.get("view_name", "Default View"),
                        "fields": params.get("fields", [])
                    }
                },
                "path": {"app_token": self.base_id},
                "useUAT": False
            })
            return f"✅ สร้างตาราง '{params.get('name')}' เรียบร้อยแล้วครับ 📊"
        except Exception as e:
            return await self.handle_operation_error(str(e), "create_table")

    async def list_tables(self) -> str:
        """List all tables in the base"""
        try:
            result = await self.mcp.call_tool("mcp__lark-tenant__bitable_v1_appTable_list", {
                "params": {"page_size": 50},
                "path": {"app_token": self.base_id},
                "useUAT": False
            })
            
            tables = result.get("items", [])
            if not tables:
                return "ไม่พบตารางในฐานข้อมูล ครับ 📋"
            
            table_list = "📊 **รายการตาราง**\n\n"
            for i, table in enumerate(tables, 1):
                table_list += f"{i}. {table['name']} (ID: {table['table_id']})\n"
            
            return table_list
        except Exception as e:
            return await self.handle_operation_error(str(e), "list_tables")

    async def delete_table(self, params: Dict) -> str:
        """Delete a table"""
        try:
            table_id = params.get("table_id")
            result = await self.mcp.call_tool("mcp__lark-tenant__bitable_v1_appTable_delete", {
                "path": {"app_token": self.base_id, "table_id": table_id},
                "useUAT": False
            })
            return f"✅ ลบตารางเรียบร้อยแล้วครับ 🗑️"
        except Exception as e:
            return await self.handle_operation_error(str(e), "delete_table")

    async def update_table(self, params: Dict) -> str:
        """Update table name"""
        try:
            table_id = params.get("table_id")
            new_name = params.get("name")
            result = await self.mcp.call_tool("mcp__lark-tenant__bitable_v1_appTable_patch", {
                "data": {"name": new_name},
                "path": {"app_token": self.base_id, "table_id": table_id},
                "useUAT": False
            })
            return f"✅ แก้ไขชื่อตารางเป็น '{new_name}' เรียบร้อยแล้วครับ ✏️"
        except Exception as e:
            return await self.handle_operation_error(str(e), "update_table")

    # === FIELD OPERATIONS ===
    async def create_field(self, params: Dict) -> str:
        """Create a new field in a table"""
        try:
            result = await self.mcp.call_tool("mcp__lark-tenant__bitable_v1_appTableField_create", {
                "data": {
                    "field_name": params.get("field_name"),
                    "type": params.get("type", 1),  # Default to text
                    "ui_type": params.get("ui_type", "Text"),
                    "property": params.get("property", {})
                },
                "params": {"client_token": f"field_{random.randint(1000, 9999)}"},
                "path": {"app_token": self.base_id, "table_id": params.get("table_id")},
                "useUAT": False
            })
            return f"✅ สร้างฟิลด์ '{params.get('field_name')}' เรียบร้อยแล้วครับ 📝"
        except Exception as e:
            return await self.handle_operation_error(str(e), "create_field")

    async def list_fields(self, params: Dict) -> str:
        """List all fields in a table"""
        try:
            result = await self.mcp.call_tool("mcp__lark-tenant__bitable_v1_appTableField_list", {
                "params": {"page_size": 50},
                "path": {"app_token": self.base_id, "table_id": params.get("table_id")},
                "useUAT": False
            })
            
            fields = result.get("items", [])
            if not fields:
                return "ไม่พบฟิลด์ในตารางนี้ ครับ 📝"
            
            field_list = f"📝 **รายการฟิลด์**\n\n"
            for i, field in enumerate(fields, 1):
                field_list += f"{i}. {field['field_name']} ({field['ui_type']})\n"
            
            return field_list
        except Exception as e:
            return await self.handle_operation_error(str(e), "list_fields")

    async def delete_field(self, params: Dict) -> str:
        """Delete a field"""
        try:
            result = await self.mcp.call_tool("mcp__lark-tenant__bitable_v1_appTableField_delete", {
                "path": {
                    "app_token": self.base_id, 
                    "table_id": params.get("table_id"),
                    "field_id": params.get("field_id")
                },
                "useUAT": False
            })
            return f"✅ ลบฟิลด์เรียบร้อยแล้วครับ 🗑️"
        except Exception as e:
            return await self.handle_operation_error(str(e), "delete_field")

    async def update_field(self, params: Dict) -> str:
        """Update a field"""
        try:
            result = await self.mcp.call_tool("mcp__lark-tenant__bitable_v1_appTableField_update", {
                "data": {
                    "field_name": params.get("field_name"),
                    "type": params.get("type"),
                    "ui_type": params.get("ui_type"),
                    "property": params.get("property", {})
                },
                "path": {
                    "app_token": self.base_id,
                    "table_id": params.get("table_id"),
                    "field_id": params.get("field_id")
                },
                "useUAT": False
            })
            return f"✅ แก้ไขฟิลด์เรียบร้อยแล้วครับ ✏️"
        except Exception as e:
            return await self.handle_operation_error(str(e), "update_field")

    # === RECORD OPERATIONS ===
    async def create_record(self, params: Dict) -> str:
        """Create a single record"""
        try:
            result = await self.mcp.call_tool("mcp__lark-tenant__bitable_v1_appTableRecord_create", {
                "data": {"fields": params.get("fields", {})},
                "params": {
                    "client_token": f"record_{random.randint(1000, 9999)}",
                    "user_id_type": "open_id"
                },
                "path": {"app_token": self.base_id, "table_id": params.get("table_id")},
                "useUAT": False
            })
            return f"✅ เพิ่มข้อมูลใหม่เรียบร้อยแล้วครับ 📝"
        except Exception as e:
            return await self.handle_operation_error(str(e), "create_record")

    async def batch_create_records(self, params: Dict) -> str:
        """Create multiple records at once"""
        try:
            records = params.get("records", [])
            result = await self.mcp.call_tool("mcp__lark-tenant__bitable_v1_appTableRecord_batchCreate", {
                "data": {"records": records},
                "params": {
                    "client_token": f"batch_{random.randint(1000, 9999)}",
                    "user_id_type": "open_id"
                },
                "path": {"app_token": self.base_id, "table_id": params.get("table_id")},
                "useUAT": False
            })
            return f"✅ เพิ่มข้อมูล {len(records)} รายการเรียบร้อยแล้วครับ 📊"
        except Exception as e:
            return await self.handle_operation_error(str(e), "batch_create")

    async def update_record(self, params: Dict) -> str:
        """Update a single record"""
        try:
            result = await self.mcp.call_tool("mcp__lark-tenant__bitable_v1_appTableRecord_update", {
                "data": {"fields": params.get("fields", {})},
                "params": {"user_id_type": "open_id"},
                "path": {
                    "app_token": self.base_id,
                    "table_id": params.get("table_id"),
                    "record_id": params.get("record_id")
                },
                "useUAT": False
            })
            return f"✅ แก้ไขข้อมูลเรียบร้อยแล้วครับ ✏️"
        except Exception as e:
            return await self.handle_operation_error(str(e), "update_record")

    async def batch_update_records(self, params: Dict) -> str:
        """Update multiple records at once"""
        try:
            records = params.get("records", [])
            result = await self.mcp.call_tool("mcp__lark-tenant__bitable_v1_appTableRecord_batchUpdate", {
                "data": {"records": records},
                "params": {"user_id_type": "open_id"},
                "path": {"app_token": self.base_id, "table_id": params.get("table_id")},
                "useUAT": False
            })
            return f"✅ แก้ไขข้อมูล {len(records)} รายการเรียบร้อยแล้วครับ 🔄"
        except Exception as e:
            return await self.handle_operation_error(str(e), "batch_update")

    async def delete_record(self, params: Dict) -> str:
        """Delete a single record"""
        try:
            result = await self.mcp.call_tool("mcp__lark-tenant__bitable_v1_appTableRecord_delete", {
                "path": {
                    "app_token": self.base_id,
                    "table_id": params.get("table_id"),
                    "record_id": params.get("record_id")
                },
                "useUAT": False
            })
            return f"✅ ลบข้อมูลเรียบร้อยแล้วครับ 🗑️"
        except Exception as e:
            return await self.handle_operation_error(str(e), "delete_record")

    async def batch_delete_records(self, params: Dict) -> str:
        """Delete multiple records at once"""
        try:
            record_ids = params.get("record_ids", [])
            result = await self.mcp.call_tool("mcp__lark-tenant__bitable_v1_appTableRecord_batchDelete", {
                "data": {"records": record_ids},
                "path": {"app_token": self.base_id, "table_id": params.get("table_id")},
                "useUAT": False
            })
            return f"✅ ลบข้อมูล {len(record_ids)} รายการเรียบร้อยแล้วครับ 🗑️"
        except Exception as e:
            return await self.handle_operation_error(str(e), "batch_delete")

    async def search_records(self, params: Dict) -> str:
        """Search records with filters"""
        try:
            result = await self.mcp.call_tool("mcp__lark-tenant__bitable_v1_appTableRecord_search", {
                "data": {
                    "field_names": params.get("field_names", []),
                    "filter": params.get("filter"),
                    "sort": params.get("sort", [])
                },
                "params": {"page_size": params.get("limit", 10)},
                "path": {"app_token": self.base_id, "table_id": params.get("table_id")},
                "useUAT": False
            })
            
            records = result.get("items", [])
            if not records:
                return "ไม่พบข้อมูลที่ตรงกับเงื่อนไข ครับ 🔍"
            
            return f"🔍 พบข้อมูล {len(records)} รายการ\n\n{self.format_records(records)}"
        except Exception as e:
            return await self.handle_operation_error(str(e), "search_records")

    # === CONTACT OPERATIONS ===
    async def get_user_info(self, params: Dict) -> str:
        """Get user information"""
        try:
            result = await self.mcp.call_tool("mcp__lark-tenant__contact_v3_user_get", {
                "params": {"user_id_type": "open_id"},
                "path": {"user_id": params.get("user_id")},
                "useUAT": False
            })
            
            user = result.get("user", {})
            name = user.get("name", "ไม่ระบุ")
            email = user.get("enterprise_email", "ไม่ระบุ")
            
            return f"👤 **ข้อมูลผู้ใช้**\n\n📛 ชื่อ: {name}\n📧 อีเมล: {email}"
        except Exception as e:
            return await self.handle_operation_error(str(e), "get_user")

    async def list_users(self, params: Dict) -> str:
        """List users in department"""
        try:
            result = await self.mcp.call_tool("mcp__lark-tenant__contact_v3_user_list", {
                "params": {
                    "user_id_type": "open_id",
                    "department_id": params.get("department_id"),
                    "page_size": params.get("limit", 20)
                },
                "useUAT": False
            })
            
            users = result.get("items", [])
            if not users:
                return "ไม่พบผู้ใช้ในแผนกนี้ ครับ 👥"
            
            user_list = "👥 **รายชื่อผู้ใช้**\n\n"
            for i, user in enumerate(users, 1):
                name = user.get("name", "ไม่ระบุ")
                email = user.get("enterprise_email", "ไม่ระบุ")
                user_list += f"{i}. {name} ({email})\n"
            
            return user_list
        except Exception as e:
            return await self.handle_operation_error(str(e), "list_users")

    async def get_department_info(self, params: Dict) -> str:
        """Get department information"""
        try:
            result = await self.mcp.call_tool("mcp__lark-tenant__contact_v3_department_get", {
                "params": {"department_id_type": "open_department_id"},
                "path": {"department_id": params.get("department_id")},
                "useUAT": False
            })
            
            dept = result.get("department", {})
            name = dept.get("name", "ไม่ระบุ")
            member_count = dept.get("member_count", 0)
            
            return f"🏢 **ข้อมูลแผนก**\n\n📛 ชื่อแผนก: {name}\n👥 จำนวนสมาชิก: {member_count} คน"
        except Exception as e:
            return await self.handle_operation_error(str(e), "get_department")

    async def list_departments(self, params: Dict) -> str:
        """List departments"""
        try:
            result = await self.mcp.call_tool("mcp__lark-tenant__contact_v3_department_list", {
                "params": {
                    "department_id_type": "open_department_id",
                    "page_size": params.get("limit", 20)
                },
                "useUAT": False
            })
            
            departments = result.get("items", [])
            if not departments:
                return "ไม่พบแผนก ครับ 🏢"
            
            dept_list = "🏢 **รายชื่อแผนก**\n\n"
            for i, dept in enumerate(departments, 1):
                name = dept.get("name", "ไม่ระบุ")
                member_count = dept.get("member_count", 0)
                dept_list += f"{i}. {name} ({member_count} คน)\n"
            
            return dept_list
        except Exception as e:
            return await self.handle_operation_error(str(e), "list_departments")

    # === DOCUMENT OPERATIONS ===
    async def get_document(self, params: Dict) -> str:
        """Get document blocks"""
        try:
            result = await self.mcp.call_tool("mcp__lark-tenant__docx_v1_documentBlock_list", {
                "params": {"page_size": 50},
                "path": {"document_id": params.get("document_id")},
                "useUAT": False
            })
            
            blocks = result.get("items", [])
            if not blocks:
                return "ไม่พบเนื้อหาในเอกสารนี้ ครับ 📄"
            
            return f"📄 **เอกสาร**\n\nพบ {len(blocks)} บล็อกข้อมูล"
        except Exception as e:
            return await self.handle_operation_error(str(e), "get_document")

    async def get_document_content(self, params: Dict) -> str:
        """Get document raw content"""
        try:
            result = await self.mcp.call_tool("mcp__lark-tenant__docx_v1_document_rawContent", {
                "params": {"lang": 0},
                "path": {"document_id": params.get("document_id")},
                "useUAT": False
            })
            
            content = result.get("content", "")
            if not content:
                return "เอกสารนี้ว่างเปล่า ครับ 📄"
            
            # Truncate if too long
            if len(content) > 1000:
                content = content[:1000] + "..."
            
            return f"📄 **เนื้อหาเอกสาร**\n\n{content}"
        except Exception as e:
            return await self.handle_operation_error(str(e), "get_document_content")

    async def update_document(self, params: Dict) -> str:
        """Update document block"""
        try:
            result = await self.mcp.call_tool("mcp__lark-tenant__docx_v1_documentBlock_patch", {
                "data": params.get("update_data", {}),
                "params": {"client_token": f"doc_{random.randint(1000, 9999)}"},
                "path": {
                    "document_id": params.get("document_id"),
                    "block_id": params.get("block_id")
                },
                "useUAT": False
            })
            return f"✅ แก้ไขเอกสารเรียบร้อยแล้วครับ 📝"
        except Exception as e:
            return await self.handle_operation_error(str(e), "update_document")

    # === MESSAGING OPERATIONS ===
    async def create_chat(self, params: Dict) -> str:
        """Create a group chat"""
        try:
            result = await self.mcp.call_tool("mcp__lark-tenant__im_v1_chat_create", {
                "data": {
                    "name": params.get("name", "New Chat"),
                    "description": params.get("description", ""),
                    "chat_type": params.get("chat_type", "private"),
                    "user_id_list": params.get("user_ids", [])
                },
                "params": {"user_id_type": "open_id"},
                "useUAT": False
            })
            return f"✅ สร้างแชทกลุ่ม '{params.get('name')}' เรียบร้อยแล้วครับ 💬"
        except Exception as e:
            return await self.handle_operation_error(str(e), "create_chat")

    async def list_chats(self) -> str:
        """List user's chats"""
        try:
            result = await self.mcp.call_tool("mcp__lark-tenant__im_v1_chat_list", {
                "params": {"page_size": 20, "user_id_type": "open_id"},
                "useUAT": False
            })
            
            chats = result.get("items", [])
            if not chats:
                return "ไม่พบแชทกลุ่ม ครับ 💬"
            
            chat_list = "💬 **รายการแชท**\n\n"
            for i, chat in enumerate(chats, 1):
                name = chat.get("name", "ไม่มีชื่อ")
                member_count = chat.get("member_count", 0)
                chat_list += f"{i}. {name} ({member_count} คน)\n"
            
            return chat_list
        except Exception as e:
            return await self.handle_operation_error(str(e), "list_chats")

    async def send_im_message(self, params: Dict) -> str:
        """Send message to Lark chat"""
        try:
            result = await self.mcp.call_tool("mcp__lark-tenant__im_v1_message_create", {
                "data": {
                    "receive_id": params.get("receive_id"),
                    "msg_type": params.get("msg_type", "text"),
                    "content": params.get("content")
                },
                "params": {"receive_id_type": params.get("receive_id_type", "chat_id")},
                "useUAT": False
            })
            return f"✅ ส่งข้อความเรียบร้อยแล้วครับ 📤"
        except Exception as e:
            return await self.handle_operation_error(str(e), "send_message")

    async def get_chat_members(self, params: Dict) -> str:
        """Get chat members"""
        try:
            result = await self.mcp.call_tool("mcp__lark-tenant__im_v1_chatMembers_get", {
                "params": {"member_id_type": "open_id", "page_size": 50},
                "path": {"chat_id": params.get("chat_id")},
                "useUAT": False
            })
            
            members = result.get("items", [])
            if not members:
                return "ไม่พบสมาชิกในแชทนี้ ครับ 👥"
            
            member_list = "👥 **สมาชิกแชท**\n\n"
            for i, member in enumerate(members, 1):
                name = member.get("name", "ไม่ระบุ")
                member_list += f"{i}. {name}\n"
            
            return member_list
        except Exception as e:
            return await self.handle_operation_error(str(e), "get_chat_members")

    # === WIKI OPERATIONS ===
    async def get_wiki_node(self, params: Dict) -> str:
        """Get wiki node information"""
        try:
            result = await self.mcp.call_tool("mcp__lark-tenant__wiki_v2_space_getNode", {
                "params": {
                    "token": params.get("token"),
                    "obj_type": params.get("obj_type", "wiki")
                },
                "useUAT": False
            })
            
            node = result.get("node", {})
            title = node.get("title", "ไม่ระบุ")
            
            return f"📚 **Wiki Node**\n\n📛 ชื่อ: {title}"
        except Exception as e:
            return await self.handle_operation_error(str(e), "get_wiki")

    # === UTILITY FUNCTIONS ===
    def format_records(self, records: List[Dict]) -> str:
        """Format records for display"""
        formatted = ""
        for i, record in enumerate(records[:5], 1):  # Show max 5 records
            formatted += f"{i}. "
            fields = record.get("fields", {})
            for field_name, value in list(fields.items())[:3]:  # Show max 3 fields
                if isinstance(value, list) and value:
                    if isinstance(value[0], dict):
                        display_value = value[0].get("text", str(value[0]))
                    else:
                        display_value = str(value[0])
                else:
                    display_value = str(value)
                formatted += f"{field_name}: {display_value[:50]} | "
            formatted = formatted.rstrip(" | ") + "\n"
        return formatted

    async def handle_operation_error(self, error_msg: str, operation: str) -> str:
        """Handle errors with natural Thai responses"""
        error_lower = error_msg.lower()
        
        if "fieldnamenotfound" in error_lower:
            return f"❌ ไม่พบฟิลด์ที่ระบุ กรุณาตรวจสอบชื่อฟิลด์ใหม่ครับ 📝"
        elif "tablenotfound" in error_lower:
            return f"❌ ไม่พบตารางที่ระบุ กรุณาตรวจสอบ Table ID ครับ 📊"
        elif "permission" in error_lower or "access" in error_lower:
            return f"❌ ไม่มีสิทธิ์เข้าถึง กรุณาติดต่อ Admin ครับ 🔐"
        elif "validation" in error_lower:
            return f"❌ ข้อมูลไม่ถูกต้อง กรุณาตรวจสอบรูปแบบข้อมูลครับ ✏️"
        else:
            return f"❌ เกิดข้อผิดพลาดในการ{operation} ลองใหม่อีกครั้งครับ 🔄"

    async def send_help_message(self) -> str:
        """Send help message with all available commands"""
        help_text = """
🤖 **คำสั่ง Lark ที่ใช้ได้**

📊 **ตาราง (Tables)**
• `list tables` - ดูรายการตาราง
• `create table` - สร้างตารางใหม่
• `delete table` - ลบตาราง
• `update table` - แก้ไขชื่อตาราง

📝 **ฟิลด์ (Fields)**
• `list fields` - ดูรายการฟิลด์
• `create field` - สร้างฟิลด์ใหม่
• `delete field` - ลบฟิลด์
• `update field` - แก้ไขฟิลด์

📋 **ข้อมูล (Records)**
• `search records` - ค้นหาข้อมูล
• `create record` - เพิ่มข้อมูลใหม่
• `batch create` - เพิ่มหลายรายการ
• `update record` - แก้ไขข้อมูล
• `batch update` - แก้ไขหลายรายการ
• `delete record` - ลบข้อมูล
• `batch delete` - ลบหลายรายการ

👥 **ผู้ใช้ (Users)**
• `list users` - ดูรายชื่อผู้ใช้
• `get user` - ดูข้อมูลผู้ใช้
• `list departments` - ดูรายชื่อแผนก
• `get department` - ดูข้อมูลแผนก

💬 **แชท (Messaging)**
• `list chats` - ดูรายการแชท
• `create chat` - สร้างแชทกลุ่ม
• `send message` - ส่งข้อความ
• `get chat members` - ดูสมาชิกแชท

📄 **เอกสาร (Documents)**
• `get document` - ดูเอกสาร
• `get document content` - ดูเนื้อหาเอกสาร
• `update document` - แก้ไขเอกสาร

📚 **Wiki**
• `get wiki` - ดูข้อมูล Wiki

พิมพ์คำสั่งเหล่านี้เพื่อใช้งาน Lark ครับ! 🚀
"""
        return help_text
