from flask import Flask, request, Response, jsonify, redirect, url_for
import json
from dotenv import load_dotenv

load_dotenv(".env")


app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('health'))


@app.route('/health')
def health():
    return "App is Up"





if __name__=='__main__':
    app.run(debug=False)