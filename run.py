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

    import threading

    def run_server():
        app.run(debug=False, host='127.0.0.1', port=5000, use_reloader=False)

    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    time.sleep(3)
    try:
        webbrowser.open('http://127.0.0.1:5000')
    except:
        pass

    print("✅ Chatbot is running!")
    print("💬 Open http://127.0.0.1:5000 in your browser to start chatting")
    print("⏹️  Press Ctrl+C to stop the server")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down the chatbot...")
        sys.exit(0)

if __name__ == "__main__":
    main()
