from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit
import os
from flask_cors import CORS, cross_origin
from google_speech_2_text import quickstart_v2
from google_speech_2_text_stream import transcribe_streaming_v2

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
    with open("audio_stream.wav", "ab") as audio_file:
        audio_file.write(data)
    
    response = transcribe_streaming_v2()

    print(f"the response is {response[-1]}")

    # Optionally, send a response back to the client
    emit('transcription', {'status': 'success'})

# Handle stop recording event
@socketio.on('stop_recording')
def stop_recording():
    print("Recording stopped")
    
    # You can send back an acknowledgment or process the final audio here

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80)
