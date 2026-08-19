import zipfile
import os
from io import StringIO

project_files = {}

project_files['requirements.txt'] = """Flask==2.3.3
requests==2.31.0
flask-cors==4.0.0
"""

project_files['server.py'] = """from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Gemini API Configuration
GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'
API_KEY = 'AIzaSyDeVDcQ9JkP9tellmRx9yVjqTD4rO42mtY'  # Your Gemini API key

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'reply': 'Please enter a message.'})
        
        # Prepare request to Gemini API
        gemini_payload = {
            'contents': [{
                'parts': [{
                    'text': user_message
                }]
            }],
            'generationConfig': {
                'temperature': 0.7,
                'topK': 40,
                'topP': 0.95,
                'maxOutputTokens': 1000
            }
        }
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        # Make request to Gemini API
        response = requests.post(
            f"{GEMINI_API_URL}?key={API_KEY}",
            json=gemini_payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            response_data = response.json()
            if (response_data.get('candidates') and 
                len(response_data['candidates']) > 0 and
                response_data['candidates'][0].get('content') and
                response_data['candidates'][0]['content'].get('parts') and
                len(response_data['candidates'][0]['content']['parts']) > 0):
                
                ai_reply = response_data['candidates'][0]['content']['parts'][0]['text']
                return jsonify({'reply': ai_reply})
            else:
                return jsonify({'reply': 'Sorry, I could not generate a response. Please try again.'})
        else:
            return jsonify({'reply': 'Sorry, there was an error connecting to the AI service.'})
            
    except requests.exceptions.Timeout:
        return jsonify({'reply': 'Request timed out. Please try again.'})
    except requests.exceptions.RequestException as e:
        return jsonify({'reply': 'Network error occurred. Please check your connection.'})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'reply': 'An unexpected error occurred. Please try again.'})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
"""

print("Created server.py and requirements.txt")