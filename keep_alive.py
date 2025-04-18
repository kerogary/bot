from flask import Flask
from threading import Thread
import os
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Alive!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))  # Must use int()


def keep_alive():
    Thread(target=run).start()
