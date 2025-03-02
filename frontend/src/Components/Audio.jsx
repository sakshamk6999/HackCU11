import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const AudioRecorder = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
//   const [audioChunks, setAudioChunks] = useState([]);
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    // Connect to the backend WebSocket server
    const ws = io('http://localhost:80');
    
    ws.on('connected', (message) => {
        console.log(message.status);
    });
  
    ws.on('transcription', (data) => {
    console.log('Audio data received confirmation:', data);
    });

    setSocket(ws);

    return () => {
      ws.close(); // Close WebSocket connection when component unmounts
    };
  }, []);

  // Start recording
  const startRecording = async () => {
    // Request user microphone access
    console.log("in the start recording")
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    // Create a MediaRecorder instance
    const recorder = new MediaRecorder(stream);
    setMediaRecorder(recorder);
    const audioChunks = [];
    // When data is available, push the chunk to the audioChunks array
    recorder.ondataavailable = (event) => {
      // Send audio chunk to the WebSocket backend
      console.log("recorder ready")
    //   if (socket && socket.readyState === WebSocket.OPEN) {
        console.log("emitting")
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

  return (
    <div>
      <button onClick={isRecording ? stopRecording : startRecording}>
        {isRecording ? 'Stop Recording' : 'Start Recording'}
      </button>
    </div>
  );
};

export default AudioRecorder;