@echo off
REM FloatChat Render Deployment Script for Windows

echo 🌊 FloatChat Render Deployment Script
echo ======================================

REM Check if git is available
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is not installed. Please install Git first.
    pause
    exit /b 1
)

REM Check if we're in a git repository
if not exist ".git" (
    echo ❌ Not in a git repository. Please run this script from the project root.
    pause
    exit /b 1
)

REM Check if required files exist
if not exist "Dockerfile" (
    echo ❌ Required file Dockerfile not found.
    pause
    exit /b 1
)
if not exist "render.yaml" (
    echo ❌ Required file render.yaml not found.
    pause
    exit /b 1
)
if not exist "requirements-production.txt" (
    echo ❌ Required file requirements-production.txt not found.
    pause
    exit /b 1
)
if not exist "start_streamlit.py" (
    echo ❌ Required file start_streamlit.py not found.
    pause
    exit /b 1
)

echo ✅ All required files found.

REM Check if .env.example exists
if not exist ".env.example" (
    echo ⚠️  .env.example not found. Creating one...
    echo # FloatChat Environment Variables > .env.example
    echo GROQ_API_KEY=your_groq_api_key_here >> .env.example
    echo COHERE_API_KEY=your_cohere_api_key_here >> .env.example
    echo PINECONE_API_KEY=your_pinecone_api_key_here >> .env.example
    echo OPENAI_API_KEY=your_openai_api_key_here >> .env.example
)

REM Check git status
git status --porcelain > temp_status.txt
if %errorlevel% equ 0 (
    for /f %%i in (temp_status.txt) do (
        echo 📝 Uncommitted changes detected.
        set /p commit_choice="Do you want to commit and push changes? (y/n): "
        if /i "!commit_choice!"=="y" (
            git add .
            git commit -m "Prepare for Render deployment"
            git push origin main
            echo ✅ Changes committed and pushed.
        ) else (
            echo ⚠️  Please commit and push your changes before deploying.
            del temp_status.txt
            pause
            exit /b 1
        )
        goto :skip_commit
    )
    echo ✅ No uncommitted changes.
    :skip_commit
    del temp_status.txt
)

REM Test Docker build locally (optional)
set /p docker_test="Do you want to test Docker build locally? (y/n): "
if /i "%docker_test%"=="y" (
    echo 🔨 Testing Docker build...
    docker build -t floatchat-test .
    if errorlevel 1 (
        echo ❌ Docker build failed. Please fix issues before deploying.
        pause
        exit /b 1
    ) else (
        echo ✅ Docker build successful.
        docker rmi floatchat-test
    )
)

echo.
echo 🎯 Ready for Render deployment!
echo.
echo Next steps:
echo 1. Go to https://dashboard.render.com
echo 2. Click 'New +' → 'Web Service'
echo 3. Connect your GitHub repository
echo 4. Configure environment variables (see .env.example)
echo 5. Deploy!
echo.
echo 📖 For detailed instructions, see RENDER_DEPLOYMENT.md
echo.
echo 🔗 Your repository should be at:
git remote get-url origin 2>nul || echo    (No remote repository configured)
echo.
echo 🌊 Happy deploying!
pause
