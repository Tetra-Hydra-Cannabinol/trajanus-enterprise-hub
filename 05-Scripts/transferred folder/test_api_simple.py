"""
Simple Anthropic API Test - Using requests library
"""

import requests
import json

def test_api_simple():
    print("=" * 60)
    print("ANTHROPIC API TEST (requests library)")
    print("=" * 60)
    
    # Read API key
    key_path = r"G:\My Drive\00 - Trajanus USA\00-Command-Center\Credentials\Trajanus Command Center api key.txt"
    
    try:
        with open(key_path, 'r') as f:
            api_key = f.read().strip()
        print(f"✓ API key loaded")
    except Exception as e:
        print(f"✗ Error reading API key: {e}")
        return
    
    # API endpoint
    url = "https://api.anthropic.com/v1/messages"
    
    # Headers
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    # Request body
    data = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 100,
        "messages": [
            {
                "role": "user",
                "content": "Say 'Trajanus Command Center API test successful!' and nothing else."
            }
        ]
    }
    
    print("\nSending request to Anthropic API...")
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            print("\n" + "=" * 60)
            print("SUCCESS!")
            print("=" * 60)
            print(f"\nClaude's Response: {result['content'][0]['text']}")
            print(f"\nUsage Statistics:")
            print(f"  Input tokens:  {result['usage']['input_tokens']}")
            print(f"  Output tokens: {result['usage']['output_tokens']}")
            
            # Calculate cost
            input_cost = (result['usage']['input_tokens'] / 1_000_000) * 3
            output_cost = (result['usage']['output_tokens'] / 1_000_000) * 15
            total_cost = input_cost + output_cost
            
            print(f"\nCost: ${total_cost:.6f}")
            print("\n" + "=" * 60)
            print("API is working! Ready for Command Center!")
            print("=" * 60)
        else:
            print(f"\n✗ API returned error code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.SSLError as e:
        print(f"\n✗ SSL Certificate Error: {e}")
        print("\nTrying without SSL verification...")
        # Try again without SSL verification (not recommended for production)
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30, verify=False)
            if response.status_code == 200:
                print("✓ API works without SSL verification")
                print("NOTE: You'll need to fix SSL certificates for production use")
        except Exception as e2:
            print(f"✗ Still failed: {e2}")
            
    except requests.exceptions.ConnectionError as e:
        print(f"\n✗ Connection Error: {e}")
        print("\nPossible causes:")
        print("1. Firewall blocking Python")
        print("2. Antivirus blocking requests")
        print("3. Corporate proxy requiring authentication")
        
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")

if __name__ == "__main__":
    test_api_simple()
