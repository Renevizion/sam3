"""
Test script to verify the backend can start without SAM 3 model weights.
This is useful for CI/CD and development environments.
"""

import sys
from pathlib import Path

# Add repo to path
repo_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(repo_root))

def test_backend_imports():
    """Test that all backend dependencies can be imported"""
    print("Testing backend imports...")
    
    try:
        import fastapi
        print("✅ FastAPI imported")
    except ImportError as e:
        print(f"❌ Failed to import FastAPI: {e}")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn imported")
    except ImportError as e:
        print(f"❌ Failed to import Uvicorn: {e}")
        return False
    
    try:
        import cv2
        print("✅ OpenCV imported")
    except ImportError as e:
        print(f"❌ Failed to import OpenCV: {e}")
        return False
    
    try:
        import numpy
        print("✅ NumPy imported")
    except ImportError as e:
        print(f"❌ Failed to import NumPy: {e}")
        return False
    
    return True


def test_app_creation():
    """Test that the FastAPI app can be created"""
    print("\nTesting FastAPI app creation...")
    
    try:
        # Mock the SAM model import to avoid requiring weights
        import sys
        from unittest.mock import MagicMock
        
        # Create mock for sam3 module
        mock_sam3 = MagicMock()
        mock_model_builder = MagicMock()
        mock_predictor = MagicMock()
        
        mock_model_builder.build_sam3_video_predictor.return_value = mock_predictor
        mock_sam3.model_builder = mock_model_builder
        
        sys.modules['sam3'] = mock_sam3
        sys.modules['sam3.model_builder'] = mock_model_builder
        
        # Now import the main module
        backend_dir = Path(__file__).parent
        sys.path.insert(0, str(backend_dir))
        
        from main import app
        print("✅ FastAPI app created successfully")
        
        # Test that routes exist
        routes = [route.path for route in app.routes]
        print(f"✅ Found {len(routes)} routes: {routes}")
        
        expected_routes = ['/', '/ws/track', '/process-video', '/health']
        for route in expected_routes:
            if route in routes:
                print(f"✅ Route {route} exists")
            else:
                print(f"❌ Route {route} missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create app: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_health_endpoint():
    """Test the health endpoint without starting the server"""
    print("\nTesting health endpoint logic...")
    
    try:
        from unittest.mock import MagicMock
        import sys
        
        # Mock sam3
        mock_sam3 = MagicMock()
        mock_model_builder = MagicMock()
        mock_predictor = MagicMock()
        mock_model_builder.build_sam3_video_predictor.return_value = mock_predictor
        mock_sam3.model_builder = mock_model_builder
        sys.modules['sam3'] = mock_sam3
        sys.modules['sam3.model_builder'] = mock_model_builder
        
        backend_dir = Path(__file__).parent
        sys.path.insert(0, str(backend_dir))
        
        from main import app, get_model
        
        # Test get_model function with mock
        model = get_model()
        print("✅ get_model() works with mock")
        
        return True
        
    except Exception as e:
        print(f"❌ Health endpoint test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("SAM 3 Web Application Backend Tests")
    print("=" * 60)
    print()
    
    results = []
    
    # Run tests
    results.append(("Import Tests", test_backend_imports()))
    results.append(("App Creation Test", test_app_creation()))
    results.append(("Health Endpoint Test", test_health_endpoint()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    return all(result for _, result in results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
