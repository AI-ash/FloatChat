#!/bin/bash
# FloatChat Render Deployment Script

echo "🌊 FloatChat Render Deployment Script"
echo "======================================"

# Check if git is available
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository. Please run this script from the project root."
    exit 1
fi

# Check if required files exist
required_files=("Dockerfile" "render.yaml" "requirements-production.txt" "start_streamlit.py")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Required file $file not found."
        exit 1
    fi
done

echo "✅ All required files found."

# Check if .env.example exists
if [ ! -f ".env.example" ]; then
    echo "⚠️  .env.example not found. Creating one..."
    # Create basic .env.example
    cat > .env.example << EOF
# FloatChat Environment Variables
GROQ_API_KEY=your_groq_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
EOF
fi

# Check git status
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 Uncommitted changes detected."
    read -p "Do you want to commit and push changes? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .
        git commit -m "Prepare for Render deployment"
        git push origin main
        echo "✅ Changes committed and pushed."
    else
        echo "⚠️  Please commit and push your changes before deploying."
        exit 1
    fi
else
    echo "✅ No uncommitted changes."
fi

# Test Docker build locally (optional)
read -p "Do you want to test Docker build locally? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔨 Testing Docker build..."
    if docker build -t floatchat-test .; then
        echo "✅ Docker build successful."
        docker rmi floatchat-test
    else
        echo "❌ Docker build failed. Please fix issues before deploying."
        exit 1
    fi
fi

echo ""
echo "🎯 Ready for Render deployment!"
echo ""
echo "Next steps:"
echo "1. Go to https://dashboard.render.com"
echo "2. Click 'New +' → 'Web Service'"
echo "3. Connect your GitHub repository"
echo "4. Configure environment variables (see .env.example)"
echo "5. Deploy!"
echo ""
echo "📖 For detailed instructions, see RENDER_DEPLOYMENT.md"
echo ""
echo "🔗 Your repository should be at:"
git remote get-url origin 2>/dev/null || echo "   (No remote repository configured)"
echo ""
echo "🌊 Happy deploying!"
