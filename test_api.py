import requests
import json
import time

BASE_URL = "http://127.0.0.1:8001"

def test_health():
    print("Testing /health...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")

def test_query():
    print("\nTesting /query...")
    payload = {
        "query": "Calculate 5 * 5"
    }
    try:
        response = requests.post(f"{BASE_URL}/query", json=payload)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        assert response.status_code == 200
        assert "25" in data["response"]
    except Exception as e:
        print(f"Query failed: {e}")

def test_history():
    print("\nTesting /history...")
    try:
        response = requests.get(f"{BASE_URL}/history")
        print(f"Status: {response.status_code}")
        print(f"Items: {len(response.json()['history'])}")
        assert response.status_code == 200
    except Exception as e:
        print(f"History check failed: {e}")

if __name__ == "__main__":
    # Wait for server to start
    time.sleep(1)
    test_health()
    test_query()
    test_history()
