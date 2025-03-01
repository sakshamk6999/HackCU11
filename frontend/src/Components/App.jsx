// // import React, { useState } from "react";

// // export const App = () => {
// //     return (
// //         <div>Hello World</div>
// //     )
// // }

// import React, { useEffect, useRef } from "react";
// import AudioRecorder from "./Audio";
// import VideoPlayer from "./VideoPlayer";
// import Hls from "hls.js";

// // HLSVideoPlayer component that plays an HLS (m3u8) stream
// const HLSVideoPlayer = ({ streamUrl }) => {
//   const videoRef = useRef(null);

//   useEffect(() => {
//     const video = videoRef.current;
//     if (Hls.isSupported()) {
//       const hls = new Hls();
//       hls.loadSource(streamUrl);
//       hls.attachMedia(video);
//       hls.on(Hls.Events.MANIFEST_PARSED, () => {
//         video.play();
//       });
//       return () => {
//         hls.destroy();
//       };
//     } else if (video.canPlayType("application/vnd.apple.mpegurl")) {
//       // For browsers like Safari with native HLS support
//       video.src = streamUrl;
//       video.addEventListener("loadedmetadata", () => {
//         video.play();
//       });
//     }
//   }, [streamUrl]);

//   return (
//     <video
//       ref={videoRef}
//       controls
//       style={{ width: "100%", maxWidth: "800px" }}
//     />
//   );
// };

// export const App = () => {
//   // Replace with your actual HeyGen HLS stream URL
//   const heyGenVideoUrl = "https://files2.heygen.ai/aws_pacific/avatar_tmp/b95540c6fb1a4d3c99ae6cf0cfc72a01/6bf760b21e7b402687e41711703e7c2c.mp4?Expires=1741464851&Signature=Js8djrT~AoeGx8evi53l~CeQx8Usv9SOrTmuLoe5pFxLtMuXyLcY1LeZRhbSMONoBWFE5ctSZ3g3ySFeaYNodp03EC2PZWZDSn7UeqdYptBIH0faWIYolijEbDNDNffVyW5Eom8mAzq2~yV1P7dimlR1cBYznpPMyK2aeC65a0flGylCgLzc-2z3xCALer~o6AsUBml4c~O6zT1E--QBZj8DQqTA98iQrN8NMBBo7M8suSKbri3CZ79qWxtrV8Rb35l6JmcjAIObKQRKTniCKB5~OgQijL4TTI36xNEr0rElouhE~M9hdM7gvVnNgfuR18NUj8NqEFXUTFHZ~LMsCQ__&Key-Pair-Id=K38HBHX5LX3X2H";

//   return (
//     <div>
//       <h1>HeyGen Live Stream</h1>
//       <VideoPlayer videoUrl={heyGenVideoUrl} />
//       <hr />
//       <h2>Audio Recorder</h2>
//       <AudioRecorder />
//     </div>
//   );
// };

// export default App;


import React from "react";
import './Diary.css';
import VideoPlayer from './VideoPlayer';
import AudioRecorder from './Audio';

const App = () => {
    const heyGenVideoUrl = "https://files2.heygen.ai/aws_pacific/avatar_tmp/b95540c6fb1a4d3c99ae6cf0cfc72a01/6bf760b21e7b402687e41711703e7c2c.mp4?Expires=1741464851&Signature=Js8djrT~AoeGx8evi53l~CeQx8Usv9SOrTmuLoe5pFxLtMuXyLcY1LeZRhbSMONoBWFE5ctSZ3g3ySFeaYNodp03EC2PZWZDSn7UeqdYptBIH0faWIYolijEbDNDNffVyW5Eom8mAzq2~yV1P7dimlR1cBYznpPMyK2aeC65a0flGylCgLzc-2z3xCALer~o6AsUBml4c~O6zT1E--QBZj8DQqTA98iQrN8NMBBo7M8suSKbri3CZ79qWxtrV8Rb35l6JmcjAIObKQRKTniCKB5~OgQijL4TTI36xNEr0rElouhE~M9hdM7gvVnNgfuR18NUj8NqEFXUTFHZ~LMsCQ__&Key-Pair-Id=K38HBHX5LX3X2H"; // Replace with actual if needed

    return (
      <div className="diary-book-container">
          <div className="diary-book">
              <div className="book-page left-page">
                  <h1 className="page-title">My Personal Diary 📖</h1>
                  <p className="page-date">March 1, 2025</p>
                  <p className="diary-text">
                      Today I decided to give my diary a complete makeover — now it looks like a real open book! 
                      This diary holds my memories, thoughts, and reflections. 🌸
                  </p>
                  <p className="diary-text">
                      Each page carries a story, and today's story is about this transformation.
                  </p>
              </div>

              <div className="book-spine"></div> {/* Center Spine */}

              <div className="book-page right-page">
                  <h2 className="media-title">Video Memory 📹</h2>
                  <VideoPlayer videoUrl={heyGenVideoUrl} />

                  <h2 className="media-title">Audio Memo 🎙️</h2>
                  <AudioRecorder />

                  <p className="page-footer">“Fill your paper with the breathings of your heart.”</p>
              </div>
          </div>
      </div>
  );
};

export default App;