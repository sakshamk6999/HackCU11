import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import { AvatarVideo } from './AvatarVideo';


const AudioRecorder = ({resetMessages, addMessage}) => {
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
//   const [audioChunks, setAudioChunks] = useState([]);
  const [socket, setSocket] = useState(null);
  const [transciption, setTranscription] = useState("");
  const [startSession, setStartSession] = useState(false);

  useEffect(() => {
    // Connect to the backend WebSocket server
    const ws = io('http://localhost:80');
    
    ws.on('connected', (message) => {
        console.log(message.status);
    });
  
    ws.on('transcription', (data) => {
    console.log('Audio data received confirmation:', data);
    setTranscription(data.transcript);
    addMessage({sender: 'user', content: data.question});
    addMessage({sender: 'bot', content: data.trancript})
    });

    setSocket(ws);

    return () => {
      ws.close(); // Close WebSocket connection when component unmounts
    };
  }, []);


  const startRecording = async () => {
    // Request user microphone access
    console.log("in the start recording")
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    
    // Create a MediaRecorder instance
    const recorder = new MediaRecorder(stream,{type:'audio/webm'});

    setMediaRecorder(recorder);
    const audioChunks = [];
    // When data is available, push the chunk to the audioChunks array
    recorder.ondataavailable = (event) => {
      // Send audio chunk to the WebSocket backend
      console.log("recorder ready")
    //   if (socket && socket.readyState === WebSocket.OPEN) {
        console.log("emitting ", event.data)
        socket.emit('audio_chunk', event.data)
    //   }
    };

    recorder.onstop = () => {
        socket.emit('stop_recording')
    };

    // Start recording
    recorder.start();
    setIsRecording(true);
  };

  // Stop recording
  const stopRecording = () => {
    mediaRecorder.stop();
    setIsRecording(false);
  };

  const handleSession = () => {
    setStartSession(startSession ? false : true);
  }

  return (
    <div>
        <AvatarVideo transcript={transciption} sessionStart={startSession}/><br />
        <h2 className="media-title">Audio Memo 🎙️</h2>
        <div style={{display: 'flex'}}>
        <button style={{flexGrow: 1}} onClick={handleSession}>Toggle Session</button>
        <button style={{flexGrow: 1}} onClick={isRecording ? stopRecording : startRecording} >{isRecording ? 'Stop Recording' : 'Start Recording'}
      </button>
        </div>
    </div>
  );
};

export default AudioRecorder;