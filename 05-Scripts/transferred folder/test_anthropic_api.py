"""
Test Anthropic API Connection
Verifies your API key works and shows you the cost breakdown
"""

import anthropic
import os

def test_api():
    print("=" * 60)
    print("ANTHROPIC API CONNECTION TEST")
    print("=" * 60)
    
    # Read API key
    key_path = r"G:\My Drive\00 - Trajanus USA\00-Command-Center\Credentials\Trajanus Command Center api key.txt"
    
    try:
        with open(key_path, 'r') as f:
            api_key = f.read().strip()
        print(f"✓ API key loaded from: {key_path}")
    except Exception as e:
        print(f"✗ Error reading API key: {e}")
        return
    
    # Initialize client
    try:
        client = anthropic.Anthropic(api_key=api_key)
        print("✓ Anthropic client initialized")
    except Exception as e:
        print(f"✗ Error initializing client: {e}")
        return
    
    # Test message
    print("\nSending test message to Claude...")
    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=100,
            messages=[
                {
                    "role": "user",
                    "content": "Say 'Trajanus Command Center API test successful!' and nothing else."
                }
            ]
        )
        
        # Get response
        response_text = message.content[0].text
        
        # Show results
        print("\n" + "=" * 60)
        print("SUCCESS!")
        print("=" * 60)
        print(f"\nClaude's Response: {response_text}")
        print(f"\nUsage Statistics:")
        print(f"  Input tokens:  {message.usage.input_tokens}")
        print(f"  Output tokens: {message.usage.output_tokens}")
        
        # Calculate cost
        # Sonnet 4.5 pricing: $3 per million input, $15 per million output
        input_cost = (message.usage.input_tokens / 1_000_000) * 3
        output_cost = (message.usage.output_tokens / 1_000_000) * 15
        total_cost = input_cost + output_cost
        
        print(f"\nCost Breakdown:")
        print(f"  Input cost:  ${input_cost:.6f}")
        print(f"  Output cost: ${output_cost:.6f}")
        print(f"  Total cost:  ${total_cost:.6f}")
        
        print("\n" + "=" * 60)
        print("API is ready for Command Center integration!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ API call failed: {e}")
        print("\nIf you see an authentication error, verify:")
        print("1. API key is correct in the file")
        print("2. You have credits in your Anthropic account")
        print("3. API key has not been revoked")

if __name__ == "__main__":
    test_api()
