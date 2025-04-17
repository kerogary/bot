from flask import Flask
from threading import Thread
import os  # Add this

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Alive!"

def run():
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 8080))  # Use dynamic port

def keep_alive():
    Thread(target=run).start()