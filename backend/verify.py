import requests
import time
import sys

def test_backend():
    base_url = "http://localhost:8000"
    
    # Wait for server
    print("Waiting for server...")
    server_up = False
    for i in range(20):
        try:
            requests.get(base_url)
            server_up = True
            break
        except:
            time.sleep(1)
    
    if not server_up:
        print("Server failed to start.")
        sys.exit(1)
            
    print("Server running.")
    
    # Ingest
    print("Ingesting...")
    try:
        res = requests.post(f"{base_url}/ingest")
        print("Ingest:", res.json())
    except Exception as e:
        print(f"Ingest failed: {e}")
    
    # Chat
    print("Chatting...")
    try:
        res = requests.post(f"{base_url}/chat", json={"message": "What is a deductible?"})
        print("Chat Response:", res.json())
    except Exception as e:
        print(f"Chat failed: {e}")

if __name__ == "__main__":
    test_backend()
