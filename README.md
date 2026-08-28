# 🤖 Dynamic AI Chatbot

A modern web-based AI chatbot built using **Python, Flask, JavaScript, SQLite, and Google Gemini API**. The application provides conversational AI with conversation memory, intent recognition, sentiment analysis, multilingual support, customizable settings, user authentication, and an interactive analytics dashboard.

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
* 🔐 **User Registration and Login Authentication**
* 🚪 **Secure User Logout**
* 🔑 **Forgot Password and Password Reset**
* 📱 **Responsive Web Interface**
* ⚡ **Typing Indicator** for better user experience
* 🛡️ **Error Handling and Fallback Responses**

## 🛠️ Technologies Used

### Backend

* Python
* Flask
* Flask-CORS
* Google Gemini API
* SQLite
* Werkzeug Security

### Frontend

* HTML5
* CSS3
* JavaScript (ES6+)
* Chart.js

### Development Tools

* Git
* GitHub
* Python Virtual Environment
* Render

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
    ├── index.html         # Main chatbot interface
    ├── login.html         # User login page
    ├── register.html      # User registration page
    ├── style.css          # Application styling
    └── app.js             # Frontend functionality
```

> **Note:** `chatbot.db` is created automatically when the application starts and is not required to be included in the repository.

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

> ⚠️ **Never upload your actual API key to GitHub.**

## 🔐 User Authentication

The application includes a user authentication system using **Flask sessions, SQLite, and password hashing**.

Users can:

* Create a new account using the registration page
* Log in using their registered credentials
* Access the chatbot after successful authentication
* Maintain separate conversation memory
* Log out securely
* Reset their password using the forgot-password option

Authentication helps restrict access to the chatbot and keeps user conversation memory associated with the logged-in user.

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

The backend maintains conversation history for each logged-in user.

Example:

```text
User: My name is Sai.

AI: Nice to meet you, Sai!

User: What is my name?

AI: Your name is Sai.
```

The conversation memory is stored in SQLite and associated with the logged-in user's account.

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
* Unauthorized access
* Expired login sessions

Fallback responses are displayed when the AI service is temporarily unavailable.

## 🧪 Testing

The project was tested for:

* User registration
* User login
* User logout
* Password reset
* Chat message processing
* Gemini API communication
* Conversation memory
* User-specific memory
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
* Login protection
* Deployment functionality

## 🔐 Security

The application uses authentication to restrict access to the chatbot.

Passwords are stored using secure password hashing rather than plain text.

Sensitive configuration files and development files are excluded from Git using `.gitignore`.

The following files and folders are intentionally not uploaded:

```text
venv/
.env
__pycache__/
*.pyc
```

API keys should always be stored using environment variables rather than directly inside the source code.

> ⚠️ **Do not upload API keys, passwords, or sensitive user information to GitHub.**

## 🌐 Live Deployment

The Dynamic AI Chatbot is deployed as a live web application using **Render**.

### 🚀 Live Demo

**Live Application:**

https://dynamic-ai-chatbot-sai.onrender.com

The deployed application provides:

* 🔐 User Registration and Login
* 🤖 Gemini AI-powered conversations
* 🧠 Conversation memory
* 🎯 Intent recognition
* 😊 Sentiment analysis
* 🌐 English, Hindi and Hinglish support
* 📊 Analytics dashboard
* ⚙️ Customizable chatbot settings
* 🔑 Password reset
* 🚪 Secure logout

### 💻 Source Code

**GitHub Repository:**

https://github.com/balasai650/ai-chatbot

### ☁️ Deployment Platform

The application is deployed using:

* **Hosting:** Render
* **Backend:** Flask
* **Runtime:** Python 3
* **Database:** SQLite
* **AI Service:** Google Gemini API

### 🔑 Deployment Environment Variables

The following environment variables are configured in the Render deployment environment:

```text
GEMINI_API_KEY
FLASK_SECRET_KEY
```

Sensitive API keys and secret values are not stored in the GitHub repository.

> **Note:** The application uses Render's free instance. The service may automatically spin down after inactivity, so the first request after a period of inactivity may take longer while the server starts again.

## 📸 Project Screenshots

Screenshots of the following application pages can be added to this README:

* Login Page
* Registration Page
* Chatbot Interface
* Analytics Dashboard
* Settings Panel

Example:

```text
screenshots/
├── login.png
├── register.png
├── chatbot.png
├── analytics.png
└── settings.png
```

## 📌 Future Improvements

Possible future enhancements include:

* Persistent database-based conversation storage improvements
* Voice input and output
* Advanced NLP-based sentiment analysis
* Conversation search
* User-specific chat history improvements
* More language options
* Advanced analytics and reporting
* Improved cloud deployment
* Email-based password recovery

## 🎓 Project Purpose

This project was developed as an educational AI application to demonstrate the integration of:

**Artificial Intelligence + Natural Language Processing + Web Development + Data Analytics**

It demonstrates how a conversational AI system can be developed using a Flask backend, JavaScript frontend, SQLite database, and a generative AI model.

## 📄 License

This project is developed for educational purposes.
