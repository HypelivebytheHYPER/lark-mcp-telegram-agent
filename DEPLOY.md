# Lark MCP LangGraph Telegram Agent v6.1

## ✅ Local Setup Complete

The system is fully configured and running locally with:
- 🔗 MCP integration (8 tools connected)
- 🔒 Base-Lock security enabled
- 📱 Telegram bot ready
- 🗂️ 3 tables mapped correctly

## 🚀 Quick Deploy to Render

1. **Fork/Upload to GitHub**
2. **Connect to Render** and select this repository
3. **Add Environment Variables:**
   - `OPENAI_API_KEY` = your OpenAI API key
   - `TG_WEBHOOK_URL` = `https://your-app-name.onrender.com/telegram/webhook`

## 📱 Telegram Setup

After deployment:
```bash
curl -X POST "https://api.telegram.org/bot8064188200:AAGuPzc5kVHTlouSWEDgwK_iISAjvYBcKJk/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://your-app-name.onrender.com/telegram/webhook"}'
```

## 🧪 Test Commands

- Health: `GET /health`
- MCP Status: `GET /mcp/health`
- Direct API: `POST /agent/run {"prompt":"memo นัดลูกค้า Table: CLIENT - Requests"}`

## 🔒 Security Features

- **Base-Lock**: Only allows authorized MCP URLs
- **Table Allowlist**: Restricts access to specific tables
- **JWT Authentication**: Secure agent endpoints