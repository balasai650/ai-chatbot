project_files['README.md'] = """# Dynamic AI Chatbot

A modern AI-powered chatbot built with Flask backend and vanilla JavaScript frontend, integrated with Google's Gemini AI.

## Features

- 🤖 **Gemini AI Integration**: Powered by Google's advanced Gemini Pro model
- 💬 **Real-time Chat**: Interactive conversation interface with typing indicators
- 📊 **Analytics Dashboard**: Track conversations, response times, and sentiment analysis
- 🎨 **Modern UI**: Clean, responsive design with light/dark theme support
- 🌍 **Multi-language Support**: English, Hindi, and Hinglish support
- ⚙️ **Customizable Settings**: Adjust AI temperature, themes, and chat features
- 📱 **Mobile Responsive**: Works perfectly on desktop and mobile devices

## Project Structure

```
dynamic-ai-chatbot/
├── server.py              # Flask backend server
├── requirements.txt       # Python dependencies
├── static/
│   ├── index.html        # Main frontend HTML
│   ├── style.css         # Stylesheet
│   └── app.js           # JavaScript functionality
└── README.md            # This file
```

## Setup Instructions

### 1. Prerequisites

Make sure you have Python 3.7+ installed on your system.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. API Key Configuration

The Gemini API key is already configured in the code, but you can replace it with your own:

1. Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Replace the `API_KEY` in `server.py` line 9
3. Replace the `apiKey` in `static/app.js` line 3

### 4. Run the Application

```bash
python server.py
```

The application will start on `http://127.0.0.1:5000`

### 5. Open in Browser

Navigate to `http://localhost:5000` in your web browser to start chatting!

## Usage

1. **Start Chatting**: Type your message in the input box and press Enter or click send
2. **Quick Replies**: Use the preset quick reply buttons for common queries
3. **Analytics**: Switch to the Analytics tab to view conversation statistics and charts
4. **Settings**: Customize the AI behavior, theme, and chat features in Settings
5. **About**: Learn more about the features in the About section

## Features Overview

### Chat Interface
- Real-time messaging with AI responses
- Typing indicators and message timestamps
- Sentiment analysis for user messages
- Message history and context awareness

### Analytics Dashboard
- Conversation statistics (total messages, response times, etc.)
- Sentiment analysis charts
- API success rate monitoring
- Response time trends

### Settings Panel
- Theme switching (Light/Dark/Auto)
- Language selection (English/Hindi/Hinglish)
- AI creativity control (temperature setting)
- Chat feature toggles (timestamps, sentiment, context memory)

### Mobile Support
- Responsive design that works on all screen sizes
- Mobile-optimized navigation
- Touch-friendly interface elements

## Customization

### Changing AI Behavior
Modify the `systemPrompt` in `static/app.js` to change how the AI responds.

### Adding New Features
- Add new navigation items in the sidebar
- Create new content sections in `index.html`
- Implement corresponding JavaScript functions in `app.js`

### Styling
Modify `static/style.css` to customize the appearance. The CSS uses CSS custom properties for easy theming.

## API Integration

The application uses Google's Gemini Pro API for AI responses. The Flask backend handles API calls to avoid CORS issues and provide better error handling.

## Troubleshooting

### Common Issues

1. **Server won't start**: Make sure you have Flask installed (`pip install Flask`)
2. **AI not responding**: Check your API key and internet connection
3. **Styling issues**: Clear your browser cache and refresh the page

### Error Handling

The application includes comprehensive error handling:
- Network connection failures
- API rate limiting
- Invalid API responses
- Fallback responses when AI is unavailable

## Contributing

Feel free to fork this project and submit pull requests for any improvements!

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

If you encounter any issues or have questions, please check the troubleshooting section above or create an issue in the project repository.
"""

# Create a simple run script
project_files['run.py'] = """#!/usr/bin/env python3
"""
Simple script to run the Dynamic AI Chatbot
"""

import os
import sys
import webbrowser
import time
from server import app

def main():
    print("🤖 Starting Dynamic AI Chatbot...")
    print("📡 Server will start on http://127.0.0.1:5000")
    print("🌐 Opening browser in 3 seconds...")
    
    # Start the server in a separate thread so we can open browser
    import threading
    
    def run_server():
        app.run(debug=False, host='127.0.0.1', port=5000, use_reloader=False)
    
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Wait a moment for server to start, then open browser
    time.sleep(3)
    try:
        webbrowser.open('http://127.0.0.1:5000')
    except:
        pass
    
    print("✅ Chatbot is running!")
    print("💬 Open http://127.0.0.1:5000 in your browser to start chatting")
    print("⏹️  Press Ctrl+C to stop the server")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\\n🛑 Shutting down the chatbot...")
        sys.exit(0)

if __name__ == "__main__":
    main()
"""

print("Created README.md and run.py")