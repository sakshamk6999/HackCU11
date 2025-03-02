import React, { useState, useEffect, useRef } from 'react';

// Assuming you are using Socket.IO client to handle WebSocket communication
import io from 'socket.io-client';

const AudioRecorder = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [socket, setSocket] = useState(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const audioStreamRef = useRef(null);

  useEffect(() => {
    // Initialize WebSocket connection
    const socketConnection = io('http://localhost:80');
    setSocket(socketConnection);

    socketConnection.on('connected', (message) => {
      console.log(message.status);
    });

    socketConnection.on('transcription', (data) => {
      console.log('Audio data received confirmation:', data);
    });

    return () => {
      socketConnection.disconnect();
    };
  }, []);


  // // Start recording
  const startRecording = () => {
    if (!navigator.mediaDevices) {
      alert("Your browser doesn't support audio recording.");
      return;
    }

    navigator.mediaDevices
      .getUserMedia({ audio: true })
      .then((stream) => {
        audioStreamRef.current = stream;
        mediaRecorderRef.current = new MediaRecorder(stream);

        mediaRecorderRef.current.ondataavailable = (event) => {
          // Push the chunk of audio data to the audioChunks array
          audioChunksRef.current.push(event.data);

          // Send the audio chunk over WebSocket
          sendAudioToBackend(event.data);
        };

        mediaRecorderRef.current.start(100); // Start recording, every 100ms a chunk is captured
        setIsRecording(true);
      })
      .catch((err) => console.error('Error accessing media devices:', err));
  };

  const sendAudioToBackend = (audioData) => {
    if (socket) {
      // Send audio data as a Blob to Flask backend over WebSocket
      socket.emit('audio_chunk', audioData);
    }
  };

  // // Stop recording
  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      audioStreamRef.current.getTracks().forEach((track) => track.stop()); // Stop all tracks
      setIsRecording(false);
    }
  };

  return (
    <div>
      <h1>Audio Streaming via WebSocket</h1>
      <button onClick={startRecording} disabled={isRecording}>
        Start Recording
      </button>
      <button onClick={stopRecording} disabled={!isRecording}>
        Stop Recording
      </button>
    </div>
  );
};

export default AudioRecorder;
