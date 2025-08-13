# 🚀 Manual Deployment Guide

## Step 1: Create GitHub Repository

1. Go to: https://github.com/HypelivebytheHYPER
2. Click "+" → "New repository"
3. Repository name: `lark-mcp-telegram-agent`
4. Description: `🚀 Lark MCP LangGraph Telegram Agent v6.1 - Production-ready bot with Base-Lock security, GPT-4o integration, and 3-table mapping`
5. Public repository ✅
6. **DO NOT** initialize with README
7. Click "Create repository"

## Step 2: Push Code to GitHub

Copy and paste these commands in terminal:

```bash
cd /Users/mac/Downloads/lark-starter-temp
git remote add origin https://github.com/HypelivebytheHYPER/lark-mcp-telegram-agent.git
git push -u origin main
```

## Step 3: Deploy to Render

1. Go to: https://render.com
2. Click "New" → "Blueprint"
3. Connect your GitHub account
4. Select repository: `HypelivebytheHYPER/lark-mcp-telegram-agent`
5. Click "Connect"
6. Render will automatically use `render.yaml` configuration
7. Wait for deployment (5-10 minutes)

## Step 4: Set Telegram Webhook

After deployment, get your app URL from Render dashboard and run:

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_TG_TOKEN>/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://YOUR_APP_NAME.onrender.com/telegram/webhook"}'
```

## Step 5: Test

Send message to your Telegram bot:
- `/start`
- `memo นัดลูกค้า Table: CLIENT - Requests`

## ✅ Features Deployed

- 🔗 MCP integration (8 tools)
- 🔒 Base-Lock security 
- 📱 Telegram bot webhook
- 🤖 GPT-4o agent
- 🗂️ 3 tables mapped
- ☁️ Auto-scaling cloud deployment