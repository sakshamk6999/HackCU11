import React, { useState, useEffect } from 'react';

const AudioRecorder = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [audioChunks, setAudioChunks] = useState([]);
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    // Connect to the backend WebSocket server
    const ws = new WebSocket('ws://your-backend-server.com');
    ws.onopen = () => {
      console.log('WebSocket connection established');
    };
    ws.onmessage = (message) => {
      console.log('Received from backend: ', message.data);
    };
    setSocket(ws);

    return () => {
      ws.close(); // Close WebSocket connection when component unmounts
    };
  }, []);

  // Start recording
  const startRecording = async () => {
    // Request user microphone access
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    // Create a MediaRecorder instance
    const recorder = new MediaRecorder(stream);
    setMediaRecorder(recorder);

    // When data is available, push the chunk to the audioChunks array
    recorder.ondataavailable = (event) => {
      // Send audio chunk to the WebSocket backend
      if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(event.data);
      }
    };

    // When the recording stops, close the WebSocket connection
    recorder.onstop = () => {
      socket.close();
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
