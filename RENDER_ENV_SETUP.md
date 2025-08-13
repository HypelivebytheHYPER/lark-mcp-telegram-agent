# 🔐 Render Environment Variables Setup

After connecting your GitHub repository to Render, you'll need to manually set these environment variables in the Render dashboard:

## Required Environment Variables

1. **TG_TOKEN**
   - Value: `<YOUR_TELEGRAM_BOT_TOKEN>`
   - Description: Your Telegram bot token from @BotFather

2. **OPENAI_API_KEY** 
   - Value: `<YOUR_OPENAI_API_KEY>`
   - Description: Your OpenAI API key for GPT-4o (starts with sk-proj-)

3. **LARK_MCP_STREAM_URL**
   - Value: `<YOUR_LARK_MCP_STREAM_URL>`
   - Description: Your Lark MCP stream endpoint with auth key

## How to Set in Render

1. Go to your Render service dashboard
2. Click "Environment" tab
3. Add each variable manually:
   - Click "Add Environment Variable"
   - Enter Key and Value
   - Click "Save Changes"

## Security Note

These sensitive values are intentionally excluded from the public repository for security. Only set them in your private Render environment variables panel.

## Getting Your Values

- **TG_TOKEN**: Get from @BotFather on Telegram
- **OPENAI_API_KEY**: Get from https://platform.openai.com/api-keys
- **LARK_MCP_STREAM_URL**: Get from your Lark MCP configuration
