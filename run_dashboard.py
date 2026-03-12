import threading
import webview
from Test import app

def start_flask():
    app.run(host="127.0.0.1", port=5000)

if __name__ == "__main__":

    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    webview.create_window(
        "SERRT Dashboard",
        "http://127.0.0.1:5000",
        fullscreen=True
    )

    webview.start()
