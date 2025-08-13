# Lark MCP LangGraph Telegram Agent v6.1

🚀 **Production-Ready Deployment**

## Quick Deploy to Render

1. **Upload to GitHub**: Push this entire folder to your GitHub repository
2. **Connect to Render**: 
   - Go to [render.com](https://render.com)
   - Click "New" → "Blueprint"
   - Connect your GitHub repo
   - Select this project
3. **Deploy**: Render will automatically use `render.yaml` configuration

## Environment Variables Setup

⚠️ **Important**: You must manually set environment variables in Render dashboard. See `RENDER_ENV_SETUP.md` for detailed instructions.

Required variables:
- `TG_TOKEN` - Your Telegram bot token
- `OPENAI_API_KEY` - Your OpenAI API key
- `LARK_MCP_STREAM_URL` - Your Lark MCP stream endpoint

## Post-Deployment Setup

After deployment, get your app URL and set Telegram webhook:

```bash
# Replace YOUR_TG_TOKEN and YOUR_APP_NAME with your actual values
curl -X POST "https://api.telegram.org/bot<YOUR_TG_TOKEN>/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://YOUR_APP_NAME.onrender.com/telegram/webhook"}'
```

## Test Commands

- **Health Check**: `GET /health`
- **MCP Status**: `GET /mcp/health` 
- **Direct API**: `POST /agent/run {"prompt":"memo test"}`
- **Telegram Bot**: Send `/start` in Telegram

## Features ✅

- 🔗 **MCP Integration**: 8 Lark tools connected
- 🔒 **Base-Lock Security**: URL & Base ID restrictions
- 📱 **Telegram Bot**: Interactive webhook support
- 🤖 **GPT-4o Agent**: LangGraph with OpenAI
- 🗂️ **Table Mapping**: 3 pre-configured tables
- ☁️ **Cloud Ready**: One-click Render deployment

## Usage

Send memo commands via Telegram:
```
memo นัดลูกค้า Table: CLIENT - Requests
```

The agent will intelligently map tables and create records in Lark Base.

## Security Note

🔐 All sensitive values (API keys, tokens) are configured via Render environment variables, not hardcoded in the repository for security.
