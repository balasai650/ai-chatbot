from flask import Flask, request, jsonify, send_from_directory, session, redirect
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import threading
import webbrowser
from google import genai


# ============================================================
# FLASK CONFIGURATION
# ============================================================

app = Flask(__name__, static_folder="static", static_url_path="")

app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    "dynamic-ai-chatbot-secret-key"
)

CORS(app, supports_credentials=True)


# ============================================================
# DATABASE
# ============================================================

DATABASE = "chatbot.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():

    conn = get_db()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Conversation memory table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversation_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()

    print("Database initialized successfully.")


initialize_database()


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

API_KEY = os.environ.get("GEMINI_API_KEY")

if API_KEY:
    client = genai.Client(api_key=API_KEY)
else:
    client = None


# ============================================================
# INTENT RECOGNITION
# ============================================================

def detect_intent(message):

    text = message.lower().strip()

    if any(word in text for word in [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]):
        return "greeting"

    if any(word in text for word in [
        "bye",
        "goodbye",
        "see you",
        "good night"
    ]):
        return "farewell"

    if any(word in text for word in [
        "thank you",
        "thanks",
        "thank"
    ]):
        return "gratitude"

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

    if any(word in text for word in [
        "weather",
        "temperature",
        "forecast",
        "rain",
        "climate"
    ]):
        return "weather"

    if any(word in text for word in [
        "joke",
        "funny",
        "entertain me",
        "story"
    ]):
        return "entertainment"

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

    return "general"


# ============================================================
# LANGUAGE HANDLING
# ============================================================

def get_language_instruction(language):

    language = str(language or "en").lower().strip()

    if language in ["hi", "hindi"]:

        return """
The user selected Hindi.

Answer in clear natural Hindi.
Use English only for necessary technical terms.
"""

    if language in [
        "hinglish",
        "hi-en",
        "hindi-english"
    ]:

        return """
The user selected Hinglish.

Answer naturally using a mixture of Hindi and English.
Keep the response easy to understand and conversational.
"""

    return """
The user selected English.

Answer in clear natural English.
"""


# ============================================================
# LOGIN CHECK
# ============================================================

@app.before_request
def require_login():

    public_routes = [
        "home",
        "login",
        "register",
        "logout",
        "login_api",
        "register_api",
        "logout_api",
        "forgot_password",
        "reset_password",
        "current_user",
        "static_files",
        "health"
    ]

    if request.endpoint in public_routes:
        return None

    if request.path.startswith("/static/"):
        return None

    if request.path.startswith("/chat"):

        if "user_id" not in session:

            return jsonify({
                "error": "Unauthorized",
                "message": "Please login first."
            }), 401

    if request.path.startswith("/clear-memory"):

        if "user_id" not in session:

            return jsonify({
                "error": "Unauthorized",
                "message": "Please login first."
            }), 401

    return None


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    if "user_id" not in session:
        return redirect("/login")

    return send_from_directory(
        app.static_folder,
        "index.html"
    )


# ============================================================
# STATIC FILES
# ============================================================

@app.route("/<path:filename>")
def static_files(filename):

    allowed_files = [
        "login.html",
        "register.html",
        "index.html",
        "style.css",
        "app.js"
    ]

    if filename in allowed_files:

        return send_from_directory(
            app.static_folder,
            filename
        )

    return jsonify({
        "error": "File not found"
    }), 404


# ============================================================
# LOGIN PAGE
# ============================================================

@app.route("/login")
def login():

    if "user_id" in session:
        return redirect("/")

    return send_from_directory(
        app.static_folder,
        "login.html"
    )


# ============================================================
# REGISTER PAGE
# ============================================================

@app.route("/register")
def register():

    if "user_id" in session:
        return redirect("/")

    return send_from_directory(
        app.static_folder,
        "register.html"
    )


# ============================================================
# LOGIN API
# ============================================================

@app.route("/api/login", methods=["POST"])
def login_api():

    data = request.get_json(silent=True) or {}

    username = str(
        data.get("username", "")
    ).strip()

    password = str(
        data.get("password", "")
    ).strip()

    if not username or not password:

        return jsonify({
            "success": False,
            "message": "Username and password are required."
        }), 400

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    user = cursor.fetchone()

    conn.close()

    if user is None:

        return jsonify({
            "success": False,
            "message": "Account not found. Please create an account first."
        }), 401

    if not check_password_hash(
        user["password"],
        password
    ):

        return jsonify({
            "success": False,
            "message": "Incorrect password."
        }), 401

    # Save user in Flask session
    session.clear()

    session["user_id"] = user["id"]
    session["username"] = user["username"]

    print()
    print("User logged in:", username)

    return jsonify({
        "success": True,
        "message": "Login successful.",
        "username": username
    })


# ============================================================
# REGISTER API
# ============================================================

@app.route("/api/register", methods=["POST"])
def register_api():

    data = request.get_json(silent=True) or {}

    username = str(
        data.get("username", "")
    ).strip()

    password = str(
        data.get("password", "")
    ).strip()

    confirm_password = str(
        data.get("confirmPassword", "")
    ).strip()

    if not username or not password or not confirm_password:

        return jsonify({
            "success": False,
            "message": "Please fill all fields."
        }), 400

    if password != confirm_password:

        return jsonify({
            "success": False,
            "message": "Passwords do not match."
        }), 400

    if len(password) < 6:

        return jsonify({
            "success": False,
            "message": "Password must contain at least 6 characters."
        }), 400

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    existing_user = cursor.fetchone()

    if existing_user:

        conn.close()

        return jsonify({
            "success": False,
            "message": "Username already exists."
        }), 409

    hashed_password = generate_password_hash(
        password
    )

    cursor.execute(
        """
        INSERT INTO users
        (username, password)
        VALUES (?, ?)
        """,
        (
            username,
            hashed_password
        )
    )

    conn.commit()
    conn.close()

    print()
    print("New account created:", username)

    return jsonify({
        "success": True,
        "message": "Account created successfully."
    })


# ============================================================
# LOGOUT API
# ============================================================

@app.route("/api/logout", methods=["POST"])
def logout_api():

    username = session.get("username")

    # IMPORTANT:
    # We DO NOT delete database memory here.
    # We only clear the login session.

    session.clear()

    print()
    print("User logged out:", username)

    return jsonify({
        "success": True,
        "message": "Logged out successfully."
    })


# ============================================================
# LOGOUT PAGE
# ============================================================

@app.route("/logout")
def logout():

    username = session.get("username")

    session.clear()

    print()
    print("User logged out:", username)

    return redirect("/login")


# ============================================================
# CURRENT USER
# ============================================================

@app.route("/api/current-user")
def current_user():

    if "user_id" not in session:

        return jsonify({
            "loggedIn": False
        })

    return jsonify({
        "loggedIn": True,
        "username": session.get("username")
    })


# ============================================================
# FORGOT PASSWORD PAGE
# ============================================================

@app.route("/forgot-password")
def forgot_password():

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Forgot Password</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f5f5f5;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
            }

            .box {
                background: white;
                padding: 30px;
                border-radius: 12px;
                width: 90%;
                max-width: 400px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            }

            h2 {
                margin-top: 0;
            }

            input {
                width: 100%;
                box-sizing: border-box;
                padding: 12px;
                margin: 8px 0;
                border: 1px solid #ccc;
                border-radius: 6px;
            }

            button {
                width: 100%;
                padding: 12px;
                margin-top: 10px;
                border: none;
                border-radius: 6px;
                background: #2563eb;
                color: white;
                cursor: pointer;
            }

            button:hover {
                background: #1d4ed8;
            }

            #message {
                margin-top: 15px;
                font-weight: bold;
            }

            a {
                display: block;
                margin-top: 15px;
                text-align: center;
            }
        </style>
    </head>

    <body>

        <div class="box">

            <h2>Forgot Password</h2>

            <p>Enter your username to reset your password.</p>

            <input
                type="text"
                id="username"
                placeholder="Username / Email"
            >

            <input
                type="password"
                id="newPassword"
                placeholder="New Password"
            >

            <input
                type="password"
                id="confirmPassword"
                placeholder="Confirm New Password"
            >

            <button id="resetBtn">
                Reset Password
            </button>

            <div id="message"></div>

            <a href="/login">
                Back to Login
            </a>

        </div>

        <script>

            document
                .getElementById("resetBtn")
                .addEventListener("click", async function () {

                    const username =
                        document.getElementById("username").value.trim();

                    const newPassword =
                        document.getElementById("newPassword").value;

                    const confirmPassword =
                        document.getElementById("confirmPassword").value;

                    const message =
                        document.getElementById("message");

                    if (!username || !newPassword || !confirmPassword) {

                        message.textContent =
                            "Please fill all fields.";

                        return;
                    }

                    try {

                        const response =
                            await fetch("/api/reset-password", {
                                method: "POST",
                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },
                                body: JSON.stringify({
                                    username: username,
                                    newPassword: newPassword,
                                    confirmPassword: confirmPassword
                                })
                            });

                        const data =
                            await response.json();

                        message.textContent =
                            data.message;

                        if (data.success) {

                            message.style.color = "green";

                            setTimeout(function () {
                                window.location.href = "/login";
                            }, 1500);

                        } else {

                            message.style.color = "red";
                        }

                    } catch (error) {

                        message.textContent =
                            "Unable to reset password.";

                        message.style.color = "red";
                    }

                });

        </script>

    </body>
    </html>
    """


# ============================================================
# RESET PASSWORD API
# ============================================================

@app.route("/api/reset-password", methods=["POST"])
def reset_password():

    data = request.get_json(silent=True) or {}

    username = str(
        data.get("username", "")
    ).strip()

    new_password = str(
        data.get("newPassword", "")
    ).strip()

    confirm_password = str(
        data.get("confirmPassword", "")
    ).strip()

    if not username or not new_password or not confirm_password:

        return jsonify({
            "success": False,
            "message": "Please fill all fields."
        }), 400

    if new_password != confirm_password:

        return jsonify({
            "success": False,
            "message": "Passwords do not match."
        }), 400

    if len(new_password) < 6:

        return jsonify({
            "success": False,
            "message": "Password must contain at least 6 characters."
        }), 400

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    user = cursor.fetchone()

    if user is None:

        conn.close()

        return jsonify({
            "success": False,
            "message": "Account not found."
        }), 404

    hashed_password = generate_password_hash(
        new_password
    )

    cursor.execute(
        """
        UPDATE users
        SET password = ?
        WHERE username = ?
        """,
        (
            hashed_password,
            username
        )
    )

    conn.commit()
    conn.close()

    print()
    print("Password reset for:", username)

    return jsonify({
        "success": True,
        "message": "Password reset successfully. You can login now."
    })


# ============================================================
# GET USER CONVERSATION MEMORY
# ============================================================

def get_user_memory(user_id):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role, message
        FROM conversation_memory
        WHERE user_id = ?
        ORDER BY id ASC
        LIMIT 30
        """,
        (user_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    memory = []

    for row in rows:

        memory.append({
            "role": row["role"],
            "text": row["message"]
        })

    return memory


# ============================================================
# SAVE USER MEMORY
# ============================================================

def save_memory(user_id, role, message):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO conversation_memory
        (user_id, role, message)
        VALUES (?, ?, ?)
        """,
        (
            user_id,
            role,
            message
        )
    )

    conn.commit()
    conn.close()


# ============================================================
# CHAT API
# ============================================================

@app.route("/chat", methods=["POST"])
def chat():

    try:

        # ----------------------------------------------------
        # CHECK LOGIN
        # ----------------------------------------------------

        if "user_id" not in session:

            return jsonify({
                "reply": "Please login first.",
                "intent": "error"
            }), 401

        user_id = session["user_id"]
        username = session.get("username")

        # ----------------------------------------------------
        # CHECK GEMINI
        # ----------------------------------------------------

        if not API_KEY or client is None:

            return jsonify({
                "reply": (
                    "Gemini API key is not configured. "
                    "Please configure GEMINI_API_KEY."
                ),
                "intent": "error"
            }), 500

        # ----------------------------------------------------
        # GET REQUEST
        # ----------------------------------------------------

        data = request.get_json(silent=True) or {}

        user_message = str(
            data.get("message", "")
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

        if not user_message:

            return jsonify({
                "reply": "Please enter a message.",
                "intent": "unknown"
            }), 400

        # ----------------------------------------------------
        # TEMPERATURE
        # ----------------------------------------------------

        try:

            temperature = float(
                temperature
            )

        except (TypeError, ValueError):

            temperature = 0.7

        temperature = max(
            0.0,
            min(temperature, 1.0)
        )

        # ----------------------------------------------------
        # INTENT
        # ----------------------------------------------------

        intent = detect_intent(
            user_message
        )

        print()
        print("-----------------------------------------")
        print("User:", username)
        print("Message:", user_message)
        print("Intent:", intent)
        print("Language:", language)
        print("-----------------------------------------")

        # ----------------------------------------------------
        # SAVE USER MESSAGE
        # ----------------------------------------------------

        save_memory(
            user_id,
            "user",
            user_message
        )

        # ----------------------------------------------------
        # GET MEMORY
        # ----------------------------------------------------

        if context_memory:

            memory = get_user_memory(
                user_id
            )

            memory_text = ""

            for message in memory:

                memory_text += (
                    f"{message['role'].upper()}: "
                    f"{message['text']}\n"
                )

        else:

            memory_text = (
                "Conversation memory is disabled "
                "for this request."
            )

        # ----------------------------------------------------
        # LANGUAGE
        # ----------------------------------------------------

        language_instruction = (
            get_language_instruction(
                language
            )
        )

        # ----------------------------------------------------
        # GEMINI PROMPT
        # ----------------------------------------------------

        prompt = f"""

You are a helpful Dynamic AI Assistant.

The currently logged-in user's username is:

{username}

IMPORTANT MEMORY RULES:

1. Use the conversation history when answering follow-up questions.
2. Remember information the user previously provided.
3. If the user previously said "My name is Sai", remember that.
4. If the user asks "What is my name?", look through the conversation history.
5. Do not say the user has not provided their name if their name exists in the history.
6. Do not invent personal information.
7. Use the most recent reliable information from the conversation.
8. Each user has separate conversation memory.
9. The current user's stored conversation history belongs only to this user.

GENERAL RULES:

1. Answer clearly and naturally.
2. Follow the selected language.
3. Help with coding, explanations, questions, learning and general conversations.
4. If the user asks a follow-up question, use previous conversation context.
5. Do not expose internal database information.

SELECTED LANGUAGE:

{language}

LANGUAGE INSTRUCTION:

{language_instruction}

DETECTED INTENT:

{intent}

CONVERSATION HISTORY:

{memory_text}

LATEST USER MESSAGE:

{user_message}

Give the best possible answer.
"""

        # ----------------------------------------------------
        # GEMINI
        # ----------------------------------------------------

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        ai_reply = response.text

        if not ai_reply:

            return jsonify({
                "reply": "Sorry, I received an empty response.",
                "intent": intent
            }), 500

        # ----------------------------------------------------
        # SAVE AI RESPONSE
        # ----------------------------------------------------

        save_memory(
            user_id,
            "assistant",
            ai_reply
        )

        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        return jsonify({
            "reply": ai_reply,
            "intent": intent,
            "language": language
        })

    except Exception as error:

        print()
        print("Gemini API Error:")
        print(error)

        return jsonify({
            "reply": (
                "I'm having trouble connecting to my AI brain "
                "right now. Please try again in a moment."
            ),
            "intent": "error"
        }), 500


# ============================================================
# CLEAR MEMORY
# ============================================================

@app.route("/clear-memory", methods=["POST"])
def clear_memory():

    if "user_id" not in session:

        return jsonify({
            "error": "Unauthorized",
            "message": "Please login first."
        }), 401

    user_id = session["user_id"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM conversation_memory
        WHERE user_id = ?
        """,
        (user_id,)
    )

    conn.commit()
    conn.close()

    print()
    print(
        "Conversation memory cleared for:",
        session.get("username")
    )

    return jsonify({
        "message": "Conversation memory cleared successfully."
    })


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():

    if "user_id" in session:

        memory_count = 0

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM conversation_memory
            WHERE user_id = ?
            """,
            (session["user_id"],)
        )

        memory_count = cursor.fetchone()[0]

        conn.close()

    else:

        memory_count = 0

    return jsonify({

        "status": "online",

        "gemini_configured":
            bool(API_KEY),

        "logged_in":
            "user_id" in session,

        "username":
            session.get("username"),

        "memory_messages":
            memory_count
    })


# ============================================================
# 404
# ============================================================

@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "error": "File not found"
    }), 404


# ============================================================
# OPEN BROWSER
# ============================================================

def open_browser():

    webbrowser.open(
        "http://127.0.0.1:5000"
    )


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("Dynamic AI Chatbot")
    print("Server: http://127.0.0.1:5000")

    if API_KEY:

        print("Gemini API key: Configured")

    else:

        print("Gemini API key: NOT CONFIGURED")

    print("Authentication: Enabled")
    print("Persistent accounts: Enabled")
    print("Persistent user memory: Enabled")
    print("Intent recognition: Enabled")
    print("Multilingual support: Enabled")
    print("Forgot password: Enabled")

    print("=" * 60)

    threading.Timer(
        1.5,
        open_browser
    ).start()

    app.run(
        debug=False,
        host="127.0.0.1",
        port=5000
    )