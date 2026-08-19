from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import threading
import webbrowser

from google import genai


# ============================================================
# FLASK CONFIGURATION
# ============================================================

app = Flask(
    __name__,
    static_folder="static",
    static_url_path=""
)

CORS(app)


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

API_KEY = os.environ.get("GEMINI_API_KEY")

if API_KEY:
    client = genai.Client(api_key=API_KEY)
else:
    client = None


# ============================================================
# CONVERSATION MEMORY
# ============================================================

conversation_history = []


# ============================================================
# INTENT RECOGNITION
# ============================================================

def detect_intent(message):

    text = message.lower().strip()

    # Greeting
    if any(word in text for word in [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]):
        return "greeting"

    # Farewell
    if any(word in text for word in [
        "bye",
        "goodbye",
        "see you",
        "good night"
    ]):
        return "farewell"

    # Gratitude
    if any(word in text for word in [
        "thank you",
        "thanks",
        "thank"
    ]):
        return "gratitude"

    # Coding
    if any(word in text for word in [
        "write code",
        "python program",
        "program",
        "coding",
        "code",
        "debug",
        "syntax error"
    ]):
        return "coding"

    # Weather
    if any(word in text for word in [
        "weather",
        "temperature",
        "forecast",
        "rain",
        "climate"
    ]):
        return "weather"

    # Entertainment
    if any(word in text for word in [
        "joke",
        "funny",
        "entertain me",
        "story"
    ]):
        return "entertainment"

    # Information
    if any(word in text for word in [
        "explain",
        "what is",
        "what are",
        "how does",
        "how do",
        "meaning of",
        "define",
        "tell me about"
    ]):
        return "information"

    # General conversation
    return "general"


# ============================================================
# LANGUAGE HANDLING
# ============================================================

def get_language_instruction(language):

    language = str(language or "en").lower().strip()

    if language in ["hi", "hindi"]:
        return """
LANGUAGE INSTRUCTION:
The user selected Hindi.

Answer the user entirely in natural, clear Hindi.
Use Devanagari script wherever appropriate.
Do not answer in English unless an English technical term,
programming keyword, product name, or other term is necessary.
"""

    if language in ["hinglish", "hi-en", "hindi-english"]:
        return """
LANGUAGE INSTRUCTION:
The user selected Hinglish.

Answer naturally using a mixture of Hindi and English.
Use Hindi in Devanagari or simple Roman Hindi where natural,
combined with English technical terms when appropriate.
Keep the response conversational and easy to understand.
Do not answer entirely in English.
"""

    return """
LANGUAGE INSTRUCTION:
The user selected English.

Answer entirely in clear, natural English.
"""


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return send_from_directory(
        app.static_folder,
        "index.html"
    )


# ============================================================
# STATIC FILES
# ============================================================

@app.route("/<path:filename>")
def static_files(filename):

    return send_from_directory(
        app.static_folder,
        filename
    )


# ============================================================
# CHAT API
# ============================================================

@app.route("/chat", methods=["POST"])
def chat():

    try:

        # ----------------------------------------------------
        # CHECK GEMINI API
        # ----------------------------------------------------

        if not API_KEY or client is None:

            return jsonify({
                "reply": (
                    "Gemini API key is not configured. "
                    "Please configure GEMINI_API_KEY "
                    "and restart the server."
                ),
                "intent": "error"
            }), 500


        # ----------------------------------------------------
        # GET REQUEST DATA
        # ----------------------------------------------------

        data = request.get_json(silent=True) or {}

        user_message = data.get(
            "message",
            ""
        ).strip()

        language = data.get(
            "language",
            "en"
        )

        context_memory = data.get(
            "contextMemory",
            True
        )

        temperature = data.get(
            "temperature",
            0.7
        )


        # ----------------------------------------------------
        # VALIDATE MESSAGE
        # ----------------------------------------------------

        if not user_message:

            return jsonify({
                "reply": "Please enter a message.",
                "intent": "unknown"
            }), 400


        # ----------------------------------------------------
        # VALIDATE TEMPERATURE
        # ----------------------------------------------------

        try:
            temperature = float(temperature)
        except (TypeError, ValueError):
            temperature = 0.7

        temperature = max(
            0.0,
            min(temperature, 1.0)
        )


        # ----------------------------------------------------
        # DETECT INTENT
        # ----------------------------------------------------

        intent = detect_intent(user_message)

        print()
        print("Detected Intent:", intent)
        print("Selected Language:", language)
        print("Temperature:", temperature)


        # ----------------------------------------------------
        # SAVE USER MESSAGE
        # ----------------------------------------------------

        conversation_history.append({
            "role": "user",
            "text": user_message
        })


        # ----------------------------------------------------
        # CREATE CONVERSATION MEMORY
        # ----------------------------------------------------

        memory_text = ""

        if context_memory:

            for message in conversation_history:

                if message["role"] == "user":

                    memory_text += (
                        f"USER: {message['text']}\n"
                    )

                elif message["role"] == "assistant":

                    memory_text += (
                        f"ASSISTANT: {message['text']}\n"
                    )

        else:

            memory_text = (
                "Conversation memory is disabled for this request."
            )


        # ----------------------------------------------------
        # LANGUAGE INSTRUCTION
        # ----------------------------------------------------

        language_instruction = get_language_instruction(
            language
        )


        # ----------------------------------------------------
        # CREATE GEMINI PROMPT
        # ----------------------------------------------------

        prompt = f"""
You are a helpful Dynamic AI Assistant.

You have access to the conversation history below.

IMPORTANT MEMORY RULES:

1. Use the conversation history when answering
   follow-up questions.

2. If the user provides a personal fact such as
   their name, remember it during this conversation.

3. If the user asks about something mentioned earlier,
   use the previous conversation to answer.

4. If information is clearly present in the conversation
   history, use it instead of saying you do not know.

5. Do not invent personal information.

6. Answer naturally and clearly.

7. If the user asks "What is my name?" and their name
   appears in the conversation history, answer using
   that name.

8. Maintain the context of the conversation.

9. Give useful and understandable answers.

10. Follow the selected language instruction below.

==================================================
SELECTED LANGUAGE
==================================================

{language}

{language_instruction}

==================================================
DETECTED USER INTENT
==================================================

{intent}

==================================================
CONVERSATION HISTORY
==================================================

{memory_text}

==================================================
END CONVERSATION HISTORY
==================================================

The user's latest message is:

{user_message}

Answer the latest message according to:

- the conversation history
- the detected intent
- the selected language

IMPORTANT:
Always follow the selected language.
Do not ignore the language selection.
"""


        # ----------------------------------------------------
        # SHOW INFORMATION IN TERMINAL
        # ----------------------------------------------------

        print()
        print("========== CONVERSATION MEMORY ==========")
        print(memory_text)
        print("==========================================")
        print("Language instruction applied:", language)


        # ----------------------------------------------------
        # SEND REQUEST TO GEMINI
        # ----------------------------------------------------

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )


        # ----------------------------------------------------
        # GET AI RESPONSE
        # ----------------------------------------------------

        ai_reply = response.text


        if not ai_reply:

            return jsonify({
                "reply": "Sorry, I received an empty response.",
                "intent": intent
            }), 500


        # ----------------------------------------------------
        # SAVE AI RESPONSE
        # ----------------------------------------------------

        conversation_history.append({
            "role": "assistant",
            "text": ai_reply
        })


        # ----------------------------------------------------
        # LIMIT MEMORY
        # ----------------------------------------------------

        if len(conversation_history) > 20:

            del conversation_history[:-20]


        # ----------------------------------------------------
        # RETURN RESPONSE
        # ----------------------------------------------------

        return jsonify({
            "reply": ai_reply,
            "intent": intent,
            "language": language
        })


    # --------------------------------------------------------
    # ERROR HANDLING
    # --------------------------------------------------------

    except Exception as error:

        print()
        print("Gemini API Error:", error)

        return jsonify({
            "reply": (
                "I'm having trouble connecting to my AI brain "
                "right now. Please try again in a moment."
            ),
            "intent": "error"
        }), 500


# ============================================================
# CLEAR CONVERSATION MEMORY
# ============================================================

@app.route(
    "/clear-memory",
    methods=["POST"]
)
def clear_memory():

    conversation_history.clear()

    print()
    print("Conversation memory cleared.")

    return jsonify({
        "message": "Conversation memory cleared successfully."
    })


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():

    return jsonify({
        "status": "online",
        "gemini_configured": bool(API_KEY),
        "memory_enabled": True,
        "memory_messages": len(conversation_history)
    })


# ============================================================
# 404 ERROR HANDLER
# ============================================================

@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "error": "File not found"
    }), 404


# ============================================================
# AUTOMATIC BROWSER OPEN
# ============================================================

def open_browser():

    webbrowser.open(
        "http://127.0.0.1:5000"
    )


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    print("=" * 55)
    print("Dynamic AI Chatbot")
    print("Server: http://127.0.0.1:5000")

    if API_KEY:
        print("Gemini API key: Configured")
    else:
        print("Gemini API key: NOT CONFIGURED")

    print("Conversation memory: Enabled")
    print("Intent recognition: Enabled")
    print("Multilingual support: Enabled")
    print("=" * 55)

    # Open browser automatically
    threading.Timer(
        1.5,
        open_browser
    ).start()

    # Start Flask server
    app.run(
        debug=False,
        host="127.0.0.1",
        port=5000
    )