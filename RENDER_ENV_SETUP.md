# 🔐 Render Environment Variables Setup

After connecting your GitHub repository to Render, you'll need to manually set these environment variables in the Render dashboard:

## Required Environment Variables

1. **TG_TOKEN**
   - Value: `8064188200:AAGuPzc5kVHTlouSWEDgwK_iISAjvYBcKJk`
   - Description: Your Telegram bot token

2. **OPENAI_API_KEY** 
   - Value: `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`
   - Description: Your OpenAI API key for GPT-4o

3. **LARK_MCP_STREAM_URL**
   - Value: `https://anycross-sg.larksuite.com/mcp/lark_base/stream?key=45NUNQAniKb0clWvcNzfaDSW8MRIeshn9PfLJSNfDKHsN98GgAi3C77sS046DFGT`
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