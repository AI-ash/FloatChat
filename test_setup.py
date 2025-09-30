<<<<<<< HEAD
#!/usr/bin/env python3
"""
Test script to verify FloatChat setup
"""
import asyncio
import sys
from pathlib import Path

async def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from config.settings import settings
        print("✅ Config settings imported")
        
        from backend.models import QueryRequest, QueryResponse
        print("✅ Backend models imported")
        
        from backend.database import create_tables, get_db_session
        print("✅ Database modules imported")
        
        from backend.services.llm_service import LLMService
        print("✅ LLM service imported")
        
        from backend.services.data_service import DataService
        print("✅ Data service imported")
        
        from backend.services.visualization_service import VisualizationService
        print("✅ Visualization service imported")
        
        from ai.query_processor import QueryProcessor
        print("✅ Query processor imported")
        
        from data.ingestion.argo_ingester import ArgoIngester
        print("✅ ARGO ingester imported")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

async def test_services():
    """Test if services can be initialized"""
    print("\n🔧 Testing service initialization...")
    
    try:
        # Test LLM service
        from backend.services.llm_service import LLMService
        llm_service = LLMService()
        print("✅ LLM service created")
        
        # Test Data service
        from backend.services.data_service import DataService
        data_service = DataService()
        await data_service.initialize()
        print("✅ Data service initialized")
        
        # Test Visualization service
        from backend.services.visualization_service import VisualizationService
        viz_service = VisualizationService()
        await viz_service.initialize()
        print("✅ Visualization service initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ Service initialization error: {e}")
        return False

async def test_api_keys():
    """Test if API keys are configured"""
    print("\n🔑 Testing API key configuration...")
    
    try:
        from config.settings import settings
        
        # Check critical API keys
        if settings.GROQ_API_KEY and not settings.GROQ_API_KEY.startswith("your_"):
            print("✅ Groq API key configured")
        else:
            print("⚠️ Groq API key not configured")
        
        if settings.PINECONE_API_KEY and not settings.PINECONE_API_KEY.startswith("your_"):
            print("✅ Pinecone API key configured")
        else:
            print("⚠️ Pinecone API key not configured")
        
        if settings.COHERE_API_KEY and not settings.COHERE_API_KEY.startswith("your_"):
            print("✅ Cohere API key configured")
        else:
            print("⚠️ Cohere API key not configured")
        
        if settings.DATABASE_URL and not settings.DATABASE_URL.startswith("postgresql://postgres:your_password"):
            print("✅ Database URL configured")
        else:
            print("⚠️ Database URL not configured")
        
        # Check data sources
        if settings.ARGO_API_BASE:
            print("✅ ARGO API configured")
        else:
            print("⚠️ ARGO API not configured")
        
        if settings.ERDDAP_BASE:
            print("✅ ERDDAP API configured")
        else:
            print("⚠️ ERDDAP API not configured")
        
        return True
        
    except Exception as e:
        print(f"❌ API key check error: {e}")
        return False

async def test_database():
    """Test database connection"""
    print("\n🗄️ Testing database connection...")
    
    try:
        from backend.database import engine
        
        # Try to connect
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✅ Database connection successful")
            return True
            
    except Exception as e:
        print(f"⚠️ Database connection failed: {e}")
        print("💡 This is expected if you haven't set up your cloud database yet")
        return False

async def main():
    """Run all tests"""
    print("🧪 FloatChat Setup Test")
    print("=" * 30)
    
    # Check if .env exists
    if not Path(".env").exists():
        print("❌ .env file not found!")
        print("📝 Please copy .env.example to .env and configure your API keys")
        sys.exit(1)
    
    tests_passed = 0
    total_tests = 4
    
    # Test imports
    if await test_imports():
        tests_passed += 1
    
    # Test services
    if await test_services():
        tests_passed += 1
    
    # Test API keys
    if await test_api_keys():
        tests_passed += 1
    
    # Test database
    if await test_database():
        tests_passed += 1
    
    print(f"\n📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! FloatChat is ready to run.")
        print("🚀 Run 'python start.py' to start the application")
    elif tests_passed >= 2:
        print("⚠️ Some tests failed, but basic functionality should work")
        print("📖 Check docs/CLOUD_APIS_SETUP.md for configuration help")
    else:
        print("❌ Multiple tests failed. Please check your setup.")
        print("📖 See docs/CLOUD_APIS_SETUP.md for detailed setup instructions")

if __name__ == "__main__":
=======
#!/usr/bin/env python3
"""
Test script to verify FloatChat setup
"""
import asyncio
import sys
from pathlib import Path

async def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from config.settings import settings
        print("✅ Config settings imported")
        
        from backend.models import QueryRequest, QueryResponse
        print("✅ Backend models imported")
        
        from backend.database import create_tables, get_db_session
        print("✅ Database modules imported")
        
        from backend.services.llm_service import LLMService
        print("✅ LLM service imported")
        
        from backend.services.data_service import DataService
        print("✅ Data service imported")
        
        from backend.services.visualization_service import VisualizationService
        print("✅ Visualization service imported")
        
        from ai.query_processor import QueryProcessor
        print("✅ Query processor imported")
        
        from data.ingestion.argo_ingester import ArgoIngester
        print("✅ ARGO ingester imported")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

async def test_services():
    """Test if services can be initialized"""
    print("\n🔧 Testing service initialization...")
    
    try:
        # Test LLM service
        from backend.services.llm_service import LLMService
        llm_service = LLMService()
        print("✅ LLM service created")
        
        # Test Data service
        from backend.services.data_service import DataService
        data_service = DataService()
        await data_service.initialize()
        print("✅ Data service initialized")
        
        # Test Visualization service
        from backend.services.visualization_service import VisualizationService
        viz_service = VisualizationService()
        await viz_service.initialize()
        print("✅ Visualization service initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ Service initialization error: {e}")
        return False

async def test_api_keys():
    """Test if API keys are configured"""
    print("\n🔑 Testing API key configuration...")
    
    try:
        from config.settings import settings
        
        # Check critical API keys
        if settings.GROQ_API_KEY and not settings.GROQ_API_KEY.startswith("your_"):
            print("✅ Groq API key configured")
        else:
            print("⚠️ Groq API key not configured")
        
        if settings.PINECONE_API_KEY and not settings.PINECONE_API_KEY.startswith("your_"):
            print("✅ Pinecone API key configured")
        else:
            print("⚠️ Pinecone API key not configured")
        
        if settings.COHERE_API_KEY and not settings.COHERE_API_KEY.startswith("your_"):
            print("✅ Cohere API key configured")
        else:
            print("⚠️ Cohere API key not configured")
        
        if settings.DATABASE_URL and not settings.DATABASE_URL.startswith("postgresql://postgres:your_password"):
            print("✅ Database URL configured")
        else:
            print("⚠️ Database URL not configured")
        
        # Check data sources
        if settings.ARGO_API_BASE:
            print("✅ ARGO API configured")
        else:
            print("⚠️ ARGO API not configured")
        
        if settings.ERDDAP_BASE:
            print("✅ ERDDAP API configured")
        else:
            print("⚠️ ERDDAP API not configured")
        
        return True
        
    except Exception as e:
        print(f"❌ API key check error: {e}")
        return False

async def test_database():
    """Test database connection"""
    print("\n🗄️ Testing database connection...")
    
    try:
        from backend.database import engine
        
        # Try to connect
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✅ Database connection successful")
            return True
            
    except Exception as e:
        print(f"⚠️ Database connection failed: {e}")
        print("💡 This is expected if you haven't set up your cloud database yet")
        return False

async def main():
    """Run all tests"""
    print("🧪 FloatChat Setup Test")
    print("=" * 30)
    
    # Check if .env exists
    if not Path(".env").exists():
        print("❌ .env file not found!")
        print("📝 Please copy .env.example to .env and configure your API keys")
        sys.exit(1)
    
    tests_passed = 0
    total_tests = 4
    
    # Test imports
    if await test_imports():
        tests_passed += 1
    
    # Test services
    if await test_services():
        tests_passed += 1
    
    # Test API keys
    if await test_api_keys():
        tests_passed += 1
    
    # Test database
    if await test_database():
        tests_passed += 1
    
    print(f"\n📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! FloatChat is ready to run.")
        print("🚀 Run 'python start.py' to start the application")
    elif tests_passed >= 2:
        print("⚠️ Some tests failed, but basic functionality should work")
        print("📖 Check docs/CLOUD_APIS_SETUP.md for configuration help")
    else:
        print("❌ Multiple tests failed. Please check your setup.")
        print("📖 See docs/CLOUD_APIS_SETUP.md for detailed setup instructions")

if __name__ == "__main__":
>>>>>>> 5347d1d (Initial commit: FloatChat AI-Powered ARGO Data System)
    asyncio.run(main())