from flask import Flask, request, Response, jsonify, redirect, url_for
import json
from dotenv import load_dotenv

from ollama_chat import OllamaModel

load_dotenv(".env")


app = Flask(__name__)

ollama_model = OllamaModel()

@app.route('/')
def index():
    return redirect(url_for('health'))


@app.route('/health')
def health():
    return "App is Up"

@app.route('/ask', methods=['POST'])
def ask_ollama():
    try:
        prompt = request.form['prompt']
        print(prompt)

        
        model_response = ollama_model.ask(prompt)

        return jsonify({"response" : model_response}), 200
    except Exception as e:
        print(e)

        return jsonify({"error" : str(e)}), 500


if __name__=='__main__':
    app.run(debug=True)