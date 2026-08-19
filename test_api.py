import requests
import json

# Updated API test with correct model
API_KEY = 'AIzaSyDeVDcQ9JkP9tellmRx9yVjqTD4rO42mtY'
GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent'

def test_gemini_api():
    print("🧪 Testing Updated Gemini API...")
    print(f"🔑 API Key: {API_KEY[:10]}...")
    print(f"🤖 Model: gemini-1.5-flash")

    # Simple test message
    payload = {
        'contents': [{
            'parts': [{
                'text': 'Hello! Just reply with "API working perfectly!" to confirm.'
            }]
        }]
    }

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(
            f"{GEMINI_API_URL}?key={API_KEY}",
            json=payload,
            headers=headers,
            timeout=30
        )

        print(f"📡 Response Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("✅ API SUCCESS!")

            if data.get('candidates'):
                ai_reply = data['candidates'][0]['content']['parts'][0]['text']
                print(f"🤖 AI Response: {ai_reply}")
                return True
            else:
                print("⚠️  No candidates in response")
                print(f"Full response: {data}")
        else:
            print("❌ API FAILED!")
            print(f"Error: {response.text}")
            return False

    except Exception as e:
        print(f"❌ CONNECTION ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_gemini_api()
    if success:
        print("\n🎉 API is working! Your chatbot should work now!")
    else:
        print("\n😞 API still not working. Let's debug further...")