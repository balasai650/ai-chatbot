# 🤖 Dynamic AI Chatbot

A modern web-based AI chatbot built using **Python, Flask, JavaScript, and Google Gemini API**. The application provides conversational AI with conversation memory, intent recognition, sentiment analysis, multilingual support, customizable settings, and an interactive analytics dashboard.

## ✨ Features

* 🤖 **AI-Powered Conversations** using Google Gemini API
* 🧠 **Conversation Memory** for maintaining context across messages
* 🎯 **Intent Recognition** for identifying user message categories
* 😊 **Sentiment Analysis** with positive, negative, and neutral classification
* 🌐 **Multi-language Support** with English, Hindi, and Hinglish options
* 📊 **Analytics Dashboard** for monitoring chatbot performance
* 📈 **Response Time Tracking** and API success-rate monitoring
* 🌓 **Light/Dark/Auto Theme**
* ⚙️ **Customizable Settings**
* 💾 **Chat History Export** in JSON format
* 🗑️ **Clear Conversation Memory**
* 📱 **Responsive Web Interface**
* ⚡ **Typing Indicator** for better user experience
* 🛡️ **Error Handling and Fallback Responses**

## 🛠️ Technologies Used

### Backend

* Python
* Flask
* Flask-CORS
* Google Gemini API

### Frontend

* HTML5
* CSS3
* JavaScript (ES6+)
* Chart.js

### Development Tools

* Git
* GitHub
* Python Virtual Environment

## 📁 Project Structure

```text
ai-chatbot/
│
├── server.py              # Flask backend and Gemini API integration
├── run.py                 # Application runner
├── requirements.txt       # Python dependencies
├── test_api.py            # API testing
├── README.md              # Project documentation
├── .gitignore             # Git ignored files
│
└── static/
    ├── index.html         # Chatbot user interface
    ├── style.css          # Application styling
    └── app.js             # Frontend functionality
```

## ⚙️ Requirements

* Python 3.10+
* Git
* Internet connection
* Google Gemini API key

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/balasai650/ai-chatbot.git
```

### 2. Open the Project Directory

```bash
cd ai-chatbot
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

#### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🔑 API Configuration

The chatbot requires a **Google Gemini API key**.

Set the API key as an environment variable.

### Windows PowerShell

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

Verify the configuration:

```powershell
$env:GEMINI_API_KEY
```

> ⚠️ Never upload your actual API key to GitHub.

## ▶️ Running the Application

Start the Flask server:

```bash
python server.py
```

The application will run at:

```text
http://127.0.0.1:5000
```

Open the address in your browser to use the chatbot.

## 💬 Chat Interface

The chatbot allows users to:

* Send natural-language questions
* Receive AI-generated responses
* Continue conversations using previous context
* View message timestamps
* View sentiment indicators
* Use quick-reply options
* Clear conversation history
* Export chat history

## 🧠 Conversation Memory

The backend maintains conversation history during the active session.

Example:

```text
User: My name is Sai.

AI: Nice to meet you, Sai!

User: What is my name?

AI: Your name is Sai.
```

This allows the chatbot to understand follow-up questions and maintain conversational context.

## 🎯 Intent Recognition

The chatbot identifies common user intents such as:

* Greeting
* Farewell
* Gratitude
* Coding
* Weather
* Entertainment
* Information
* General conversation

The detected intent is included in the context provided to the AI model.

## 😊 Sentiment Analysis

User messages are analyzed and classified into:

* 😊 Positive
* 😔 Negative
* 😐 Neutral

The detected sentiment is displayed in the chat interface and summarized in the analytics dashboard.

## 🌐 Multi-language Support

The chatbot provides language options including:

* English
* Hindi
* Hinglish

The selected language is included in the AI response instructions so that responses can be generated in the requested language.

## 📊 Analytics Dashboard

The dashboard provides chatbot performance information.

### Conversation Metrics

* Total conversations
* Total messages
* Average response time
* API success rate

### Sentiment Analysis

Displays the distribution of:

* Positive messages
* Negative messages
* Neutral messages

### Response Time Trend

Displays recent AI response times using interactive charts.

### Session Information

Shows:

* Number of messages
* Current session sentiment
* Session duration
* API calls

### Recent Topics

Displays topics detected from recent user messages.

## ⚙️ Settings

The settings panel provides controls for:

* Language selection
* AI response temperature
* Light/Dark/Auto theme
* Message timestamps
* Sentiment analysis
* Conversation context memory

## 🛡️ Error Handling

The application includes error handling for:

* Network failures
* API failures
* Invalid API responses
* Missing API configuration
* Empty user messages

Fallback responses are displayed when the AI service is temporarily unavailable.

## 🧪 Testing

The project was tested for:

* Chat message processing
* Gemini API communication
* Conversation memory
* Name/context recall
* Intent recognition
* Sentiment analysis
* Language selection
* Theme switching
* Analytics dashboard
* Response-time tracking
* Chat history export
* Clear conversation functionality
* API error handling

## 🔐 Security

Sensitive configuration files and development files are excluded from Git using `.gitignore`.

The following files and folders are intentionally not uploaded:

```text
venv/
.env
__pycache__/
*.pyc
```

API keys should always be stored using environment variables rather than directly inside the source code.

## 📌 Future Improvements

Possible future enhancements include:

* User authentication
* Persistent database-based conversation storage
* Voice input and output
* Advanced NLP-based sentiment analysis
* Conversation search
* Cloud deployment
* User-specific chat history
* More language options
* Advanced analytics and reporting

## 🎓 Project Purpose

This project was developed as an educational AI application to demonstrate the integration of:

**Artificial Intelligence + Natural Language Processing + Web Development + Data Analytics**

It demonstrates how a conversational AI system can be developed using a Flask backend, JavaScript frontend, and a generative AI model.

## 📄 License

This project is developed for educational purposes.
