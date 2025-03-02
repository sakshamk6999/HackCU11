from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit
import os
from flask_cors import CORS, cross_origin
from google_speech_2_text import quickstart_v2
from google_speech_2_text_stream import transcribe_streaming_v2
import requests
import jsonpickle

app = Flask(__name__)
CORS(app, origins=["*"])
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return "WebSocket server is running"

# Handle incoming audio chunks
@socketio.on('audio_chunk')
def handle_audio_chunk(data):
    # You can store the audio chunks in a file or process them here
    print(f"received data of size: {len(data)}")
    with open("audio_stream.wav", "wb") as audio_file:
        audio_file.write(data)
    
    # response = quickstart_v2()
    # response_json = jsonpickle.decode(response)
    # print(f"the response is {response_json}")
    response = quickstart_v2()
    print(f"the response is {response}")

    response = requests.post("http://127.0.0.1:5000/ask", data={"prompt": response})
    # Optionally, send a response back to the client
    # emit('transcription', {'transcript': ' '.join(response.json()['response'])})
    reply = response.json()['response']
    # final_response = " ".join(response_list)

    print(f"response {reply}")
    emit('transcription', {'transcript': reply})
    # print(f"joined response {' '.join(response.json()['response'])}")

# Handle stop recording event
@socketio.on('stop_recording')
def stop_recording():
    print("Recording stopped")
    
    
    # You can send back an acknowledgment or process the final audio here

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80)
