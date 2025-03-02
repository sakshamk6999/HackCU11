import React, { useState, useEffect } from 'react';
import './Diary.css';
import VideoPlayer from './VideoPlayer';
import AudioRecorder from './Audio';
import { AvatarVideo } from "./AvatarVideo";
import { Conversation } from "./Conversation";
import ChatBox from "./ChatBox/ChatBox";


const App = () => {
    // const heyGenVideoUrl = "https://files2.heygen.ai/aws_pacific/avatar_tmp/b95540c6fb1a4d3c99ae6cf0cfc72a01/6bf760b21e7b402687e41711703e7c2c.mp4?Expires=1741464851&Signature=Js8djrT~AoeGx8evi53l~CeQx8Usv9SOrTmuLoe5pFxLtMuXyLcY1LeZRhbSMONoBWFE5ctSZ3g3ySFeaYNodp03EC2PZWZDSn7UeqdYptBIH0faWIYolijEbDNDNffVyW5Eom8mAzq2~yV1P7dimlR1cBYznpPMyK2aeC65a0flGylCgLzc-2z3xCALer~o6AsUBml4c~O6zT1E--QBZj8DQqTA98iQrN8NMBBo7M8suSKbri3CZ79qWxtrV8Rb35l6JmcjAIObKQRKTniCKB5~OgQijL4TTI36xNEr0rElouhE~M9hdM7gvVnNgfuR18NUj8NqEFXUTFHZ~LMsCQ__&Key-Pair-Id=K38HBHX5LX3X2H"; // Replace with actual if needed

    const [messages, setMessages] = useState([
        { sender: "bot", content: "Hi, how can I help you today?" }, { sender: "user", content: "This is a user reply." }
      ]);

    const addMessage = (message) => {
        setMessages((m) => [
            ...m,
            message
        ]);
    }

    const resetMessages = () => {
        setMessages([])
    }

    return (
      <div className="diary-book-container">
          <div className="diary-book">
              <div className="book-page left-page">
                  <ChatBox messages={messages} />
              </div>

              <div className="book-spine"></div> {/* Center Spine */}

              <div className="book-page right-page">
                  <h2 className="media-title">Video Memory 📹</h2>
                  {/* <VideoPlayer videoUrl={heyGenVideoUrl} />
                   */}
                   {/* <AvatarVideo /> */}
                   <AudioRecorder addMessage={addMessage} resetMessages={resetMessages} />

                  <p className="page-footer">“Fill your paper with the breathings of your heart.”</p>
              </div>
          </div>
      </div>
  );
};

export default App;
