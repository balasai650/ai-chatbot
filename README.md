# Dynamic AI Chatbot

A modern web-based chatbot application built with Flask backend and vanilla JavaScript frontend, featuring advanced natural language processing capabilities.

## Features

- **Real-time Chat Interface**: Interactive conversation system with typing indicators
- **Analytics Dashboard**: Track conversations, response times, and sentiment analysis
- **Modern UI Design**: Clean, responsive interface with light/dark theme support
- **Multi-language Support**: English, Hindi, and Hinglish language options
- **Customizable Settings**: Adjust response creativity, themes, and chat features
- **Mobile Responsive**: Works seamlessly on desktop and mobile devices
- **Data Export**: Export chat history and analytics data

## Project Structure

```
dynamic-ai-chatbot/
├── server.py              # Flask backend server
├── requirements.txt       # Python dependencies
├── static/
│   ├── index.html        # Main frontend HTML
│   ├── style.css         # Stylesheet
│   └── app.js           # JavaScript functionality
└── README.md            # Project documentation
```

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- Internet connection for API access

### Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python server.py
   ```

3. **Access the Application**
   Open your web browser and navigate to `http://localhost:5000`

## Usage

### Chat Interface
- Type messages in the input box and press Enter or click Send
- Use quick reply buttons for common queries
- View message timestamps and sentiment indicators
- Clear chat history or export conversations

### Analytics Dashboard
- View conversation statistics and metrics
- Monitor API success rates and response times
- Analyze sentiment trends with interactive charts
- Track session information in real-time

### Settings Panel
- Switch between light/dark themes or use auto mode
- Select preferred language (English/Hindi/Hinglish)
- Adjust AI response creativity with temperature control
- Toggle chat features like timestamps and sentiment analysis

## Technical Implementation

### Backend (Flask)
- RESTful API endpoints for chat functionality
- Secure API integration with error handling
- Static file serving and routing
- CORS enabled for cross-origin requests

### Frontend (Vanilla JavaScript)
- Modern ES6+ JavaScript without external frameworks
- Responsive CSS with CSS custom properties
- Chart.js integration for analytics visualization
- Local storage for settings persistence

### Features
- **Sentiment Analysis**: Real-time emotion detection in messages
- **Context Awareness**: Maintains conversation history and context
- **Performance Monitoring**: Tracks response times and API metrics
- **Export Functionality**: Download chat data in JSON format
- **Theme System**: Dynamic light/dark mode switching

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## API Configuration

The application uses external language model APIs for natural language processing. API configuration is handled in the server.py file with appropriate error handling and fallback responses.

## Development

### Code Structure
- **Modular Design**: Separated concerns between UI, API, and data management
- **Event-Driven Architecture**: DOM event handling with proper cleanup
- **Responsive Layout**: CSS Grid and Flexbox for modern layouts
- **Progressive Enhancement**: Works with JavaScript disabled (basic functionality)

### Performance Optimizations
- Efficient DOM manipulation with minimal reflows
- Debounced input handling for smooth user experience
- Lazy loading of analytics charts
- Optimized CSS with minimal specificity conflicts

## License

This project is for educational purposes.

## Support

For technical support or questions about implementation, please refer to the source code comments or contact the development team.
