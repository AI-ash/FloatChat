<<<<<<< HEAD
@echo off
REM FloatChat Deployment Script for Windows

echo 🌊 FloatChat Deployment Script
echo ==============================

REM Check if .env file exists
if not exist .env (
    echo ❌ Error: .env file not found!
    echo 💡 Please copy .env.example to .env and configure your API keys
    exit /b 1
)

REM Build and start services
echo 🔨 Building FloatChat...
docker-compose build

echo 🚀 Starting FloatChat services...
docker-compose up -d

echo ⏳ Waiting for services to start...
timeout /t 30 /nobreak > nul

REM Health check
echo 🔍 Checking service health...
curl -f http://localhost:8000/ > nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Backend is healthy
) else (
    echo ❌ Backend health check failed
    docker-compose logs floatchat
    exit /b 1
)

curl -f http://localhost:8501/ > nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Frontend is healthy
) else (
    echo ⚠️ Frontend may still be starting...
)

echo.
echo 🎉 FloatChat deployed successfully!
echo ==================================
echo 🔧 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo 🌊 Frontend: http://localhost:8501
echo ==================================
echo.
echo 📊 To view logs: docker-compose logs -f
echo 🛑 To stop: docker-compose down
=======
@echo off
REM FloatChat Deployment Script for Windows

echo 🌊 FloatChat Deployment Script
echo ==============================

REM Check if .env file exists
if not exist .env (
    echo ❌ Error: .env file not found!
    echo 💡 Please copy .env.example to .env and configure your API keys
    exit /b 1
)

REM Build and start services
echo 🔨 Building FloatChat...
docker-compose build

echo 🚀 Starting FloatChat services...
docker-compose up -d

echo ⏳ Waiting for services to start...
timeout /t 30 /nobreak > nul

REM Health check
echo 🔍 Checking service health...
curl -f http://localhost:8000/ > nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Backend is healthy
) else (
    echo ❌ Backend health check failed
    docker-compose logs floatchat
    exit /b 1
)

curl -f http://localhost:8501/ > nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Frontend is healthy
) else (
    echo ⚠️ Frontend may still be starting...
)

echo.
echo 🎉 FloatChat deployed successfully!
echo ==================================
echo 🔧 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo 🌊 Frontend: http://localhost:8501
echo ==================================
echo.
echo 📊 To view logs: docker-compose logs -f
echo 🛑 To stop: docker-compose down
>>>>>>> 5347d1d (Initial commit: FloatChat AI-Powered ARGO Data System)
echo 🔄 To restart: docker-compose restart