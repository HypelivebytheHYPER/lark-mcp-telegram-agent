#!/bin/bash

echo "🚀 Lark MCP Telegram Agent Deployment Helper"
echo "============================================="

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI not found. Please install: brew install gh"
    echo "Or create repository manually at: https://github.com/new"
    exit 1
fi

# Create GitHub repository
echo "📁 Creating GitHub repository..."
gh repo create lark-mcp-telegram-agent --public --description "🚀 Lark MCP LangGraph Telegram Agent v6.1 - Production-ready bot with Base-Lock security, GPT-4o integration, and 3-table mapping" --clone=false

if [ $? -eq 0 ]; then
    echo "✅ Repository created successfully!"
    
    # Get the repository URL
    REPO_URL=$(gh repo view --json url -q .url)
    echo "🔗 Repository URL: $REPO_URL"
    
    # Add remote and push
    echo "⬆️ Pushing code to GitHub..."
    git remote add origin $REPO_URL.git
    git push -u origin main
    
    echo "✅ Code pushed successfully!"
    echo ""
    echo "🚀 Next steps:"
    echo "1. Go to https://render.com"
    echo "2. Click 'New' → 'Blueprint'"
    echo "3. Connect your GitHub repo: $(basename $REPO_URL)"
    echo "4. Render will auto-deploy using render.yaml"
    echo ""
    echo "📱 After deployment, set Telegram webhook:"
    echo "curl -X POST \"https://api.telegram.org/bot8064188200:AAGuPzc5kVHTlouSWEDgwK_iISAjvYBcKJk/setWebhook\" \\"
    echo "  -H \"Content-Type: application/json\" \\"
    echo "  -d '{\"url\":\"https://YOUR_APP_NAME.onrender.com/telegram/webhook\"}'"
    
else
    echo "❌ Failed to create repository. Please create manually:"
    echo "1. Go to https://github.com/new"
    echo "2. Repository name: lark-mcp-telegram-agent"
    echo "3. Description: 🚀 Lark MCP LangGraph Telegram Agent v6.1"
    echo "4. Public repository"
    echo "5. Don't initialize with README"
    echo ""
    echo "Then run these commands:"
    echo "git remote add origin https://github.com/YOUR_USERNAME/lark-mcp-telegram-agent.git"
    echo "git push -u origin main"
fi