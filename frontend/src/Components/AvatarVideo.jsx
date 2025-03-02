import StreamingAvatar, {
    AvatarQuality,
    StreamingEvents, TaskMode, TaskType, VoiceEmotion,
  } from '@heygen/streaming-avatar';
import React, { useState, useEffect, useRef } from 'react';

// const avatar = new StreamingAvatar({ token: 'your-access-token' });

export const AvatarVideo = ({transcript, sessionStart}) => {
    const mediaStream = useRef(null);
    const avatar = useRef(null);
    const [stream, setStream] = useState();
    // const [text, setText] = useState(transcript);

    useEffect(() => {
        if(transcript.length > 0) {
            makeAvatarTalk(transcript)
        }
    }, [transcript])

    useEffect(() => {
        if(sessionStart){
        startSession();
    }
    }, [sessionStart])

    async function fetchAccessToken() {
        try {
          const response = await fetch('https://api.heygen.com/v1/streaming.create_token', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-Api-Key': "NjdkODY3OGM4ZWEwNGMzOGIyOGM2ZDgzNjIyMzhiNDYtMTc0MDg2Mzg0Ng==",
              },
          });
          const token = await response.json();
    
          console.log("Access Token:", token); // Log the token to verify
    
          return token.data.token;
        } catch (error) {
          console.error("Error fetching access token:", error);
        }
    
        return "";
    }

    const startSession = async () => {
        const newToken = await fetchAccessToken();
        console.log("got token: ", newToken)
        //start session
        avatar.current = new StreamingAvatar({
            token: newToken,
        })

        avatar.current.on(StreamingEvents.AVATAR_START_TALKING, (e) => {
            console.log("Avatar started talking", e);
        });

        avatar.current.on(StreamingEvents.AVATAR_STOP_TALKING, (e) => {
        console.log("Avatar stopped talking", e);
        });

        avatar.current.on(StreamingEvents.STREAM_DISCONNECTED, () => {
        console.log("Stream disconnected");
        endSession();
        });

        avatar.current?.on(StreamingEvents.STREAM_READY, (event) => {
        console.log(">>>>> Stream ready:", event.detail);
        setStream(event.detail);
        });


        const res = await avatar.current.createStartAvatar({
            quality: AvatarQuality.Low,
            avatarId: "Nico_public",
            // knowledgeId: knowledgeId, // Or use a custom `knowledgeBase`.
            // voice: {
            //   rate: 1.5, // 0.5 ~ 1.5
            //   emotion: VoiceEmotion.EXCITED,
            //   // elevenlabsSettings: {
            //   //   stability: 1,
            //   //   similarity_boost: 1,
            //   //   style: 1,
            //   //   use_speaker_boost: false,
            //   // },
            // },
            // language: 'en',
            // disableIdleTimeout: true,
          });
    }

    useEffect(async () => {

        return () => {
            //stop session
            endSession();
        }

    }, [])

    const endSession = async () => {
        await avatar.current?.stopAvatar();
        setStream(undefined);
    }

    // const startSession = async () => {
    //     const sessionData = await avatar.createStartAvatar({
    //       avatarName: 'MyAvatar',
    //       quality: 'high',
    //     });
        
    //     console.log('Session started:', sessionData.session_id);
      
    //     await avatar.speak({
    //       sessionId: sessionData.session_id,
    //       text: 'Hello, world!',
    //       task_type: TaskType.REPEAT
    //     });
    // };

    useEffect(() => {
        if (stream && mediaStream.current) {
          mediaStream.current.srcObject = stream;
          mediaStream.current.onloadedmetadata = () => {
            mediaStream.current.play();
            // setDebug("Playing");
          };
        }
      }, [mediaStream, stream]);
    
    const makeAvatarTalk = async (text) => {
        await avatar.current.speak(
            { text: text, taskType: TaskType.REPEAT, taskMode: TaskMode.SYNC }
        )
    }

    return (
        <div className='avatar-video' style={{ height: "300px", overflow: 'hidden'}}>
            {/* <button onClick={startSession}>Start Session</button> */}
            {/* <input placeholder='enter the text that you want the avatar to say'
            value={text}
            onChange={(e) => setText(e.target.value)}
            /> */}
            {/* <button onClick={makeAvatarTalk}>Talk!</button> */}
            <video 
                ref={mediaStream}
                autoPlay
                playsInline
                style={{
                    height: "300px",
                //   objectFit: "contain",
                    // position: 'absolute',
                    margin: 'auto',
                    display: "inline-block"
                }}
            >
                {/* <track kind="captions" /> */}
            </video>
        </div>
    )
}