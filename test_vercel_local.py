#!/usr/bin/env python3
"""
Test Vercel serverless function locally
"""

import sys
import os

# Add api directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))

# Mock Vercel request
class MockRequest:
    def __init__(self, method='GET', path='/', body=None):
        self.method = method
        self.path = path
        self.body = body or b''
        self.headers = {}

def test_basic_import():
    """Test if we can import the handler"""
    print("Testing imports...")
    try:
        from api.index import handler
        print("✓ Handler imported successfully")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_mangum():
    """Test if Mangum wrapper works"""
    print("\nTesting Mangum wrapper...")
    try:
        from api.main import app
        from mangum import Mangum

        handler = Mangum(app, lifespan="off", api_gateway_base_path="/api")
        print("✓ Mangum handler created successfully")

        # Test with a mock event
        event = {
            'rawPath': '/api/',
            'requestContext': {
                'http': {
                    'method': 'GET',
                    'path': '/api/',
                }
            },
            'headers': {},
            'body': None,
            'isBase64Encoded': False
        }

        print("✓ Testing GET / request...")
        response = handler(event, {})
        print(f"✓ Response: {response}")

        return True
    except Exception as e:
        print(f"✗ Mangum test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fastapi_direct():
    """Test FastAPI app directly"""
    print("\nTesting FastAPI app directly...")
    try:
        from api.main import app
        from fastapi.testclient import TestClient

        client = TestClient(app)
        response = client.get("/")
        print(f"✓ FastAPI root endpoint: {response.status_code} - {response.json()}")

        return response.status_code == 200
    except Exception as e:
        print(f"✗ FastAPI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*60)
    print("Vercel Serverless Function Local Test")
    print("="*60)

    results = []

    results.append(("Import Handler", test_basic_import()))
    results.append(("FastAPI Direct", test_fastapi_direct()))
    results.append(("Mangum Wrapper", test_mangum()))

    print("\n" + "="*60)
    print("Test Results:")
    print("="*60)

    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {name}")

    all_passed = all(r[1] for r in results)

    print("\n" + "="*60)
    if all_passed:
        print("✓ All tests passed! Ready to deploy.")
    else:
        print("✗ Some tests failed. Fix issues before deploying.")
    print("="*60)

    sys.exit(0 if all_passed else 1)
