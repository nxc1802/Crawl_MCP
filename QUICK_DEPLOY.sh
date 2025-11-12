#!/bin/bash

# Quick Deploy Script for Vercel
# Usage: ./QUICK_DEPLOY.sh

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           🚀 VERCEL QUICK DEPLOY SCRIPT                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if we're in the right directory
if [ ! -f "vercel.json" ]; then
    echo "❌ Error: vercel.json not found!"
    echo "   Please run this script from the project root directory."
    exit 1
fi

echo "✅ Project structure verified"
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit - Ready for Vercel deployment"
else
    echo "✅ Git repository found"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 Pre-deployment checklist:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check Python
echo -n "Checking Python... "
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo "✅ Python $PYTHON_VERSION"
else
    echo "❌ Python not found"
    exit 1
fi

# Check requirements.txt
echo -n "Checking requirements.txt... "
if [ -f "requirements.txt" ]; then
    PACKAGE_COUNT=$(grep -v "^#" requirements.txt | grep -v "^$" | wc -l | tr -d ' ')
    echo "✅ $PACKAGE_COUNT packages"
else
    echo "❌ requirements.txt not found"
    exit 1
fi

# Check API directory
echo -n "Checking API directory... "
if [ -d "api" ]; then
    API_FILES=$(ls api/*.py 2>/dev/null | wc -l | tr -d ' ')
    echo "✅ $API_FILES files"
else
    echo "❌ api/ directory not found"
    exit 1
fi

# Check core modules
echo -n "Checking core modules... "
if [ -d "core" ] && [ -d "utils" ] && [ -d "web" ]; then
    echo "✅ All modules present"
else
    echo "❌ Missing core modules"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 Deployment Options:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Option 1: Vercel CLI (Fast)"
echo "   npm i -g vercel"
echo "   vercel login"
echo "   vercel --prod"
echo ""
echo "Option 2: Vercel Dashboard (Recommended)"
echo "   1. git add . && git commit -m 'Deploy' && git push"
echo "   2. Visit: https://vercel.com/new"
echo "   3. Import repository"
echo "   4. Click Deploy"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Prompt for action
read -p "Do you want to commit and push now? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "📝 Committing changes..."
    git add .
    git status
    
    echo ""
    read -p "Enter commit message (or press Enter for default): " COMMIT_MSG
    
    if [ -z "$COMMIT_MSG" ]; then
        COMMIT_MSG="Ready for Vercel deployment"
    fi
    
    git commit -m "$COMMIT_MSG"
    
    echo ""
    read -p "Do you want to push to remote? (y/n): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        echo "🚀 Pushing to remote..."
        
        # Check if remote exists
        if git remote get-url origin &> /dev/null; then
            git push origin main || git push origin master
            echo ""
            echo "✅ Pushed successfully!"
            echo ""
            echo "🎉 Next step: Import project at https://vercel.com/new"
        else
            echo ""
            echo "⚠️  No remote repository configured."
            echo "   Add remote with: git remote add origin <your-repo-url>"
            echo "   Then push with: git push -u origin main"
        fi
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📚 Documentation:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📄 README_DEPLOYMENT.md      - Full deployment guide"
echo "📄 DEPLOYMENT_CHECKLIST.md   - Complete checklist"
echo "📄 VERCEL_DEPLOY_SUMMARY.md  - Changes summary"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ All set! Your project is ready for deployment! ✨"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

