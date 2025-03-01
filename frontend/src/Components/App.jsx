// import React, { useState } from "react";

// export const App = () => {
//     return (
//         <div>Hello World</div>
//     )
// }

import React, { useEffect, useRef } from "react";
import AudioRecorder from "./Audio";
import Hls from "hls.js";

// HLSVideoPlayer component that plays an HLS (m3u8) stream
const HLSVideoPlayer = ({ streamUrl }) => {
  const videoRef = useRef(null);

  useEffect(() => {
    const video = videoRef.current;
    if (Hls.isSupported()) {
      const hls = new Hls();
      hls.loadSource(streamUrl);
      hls.attachMedia(video);
      hls.on(Hls.Events.MANIFEST_PARSED, () => {
        video.play();
      });
      return () => {
        hls.destroy();
      };
    } else if (video.canPlayType("application/vnd.apple.mpegurl")) {
      // For browsers like Safari with native HLS support
      video.src = streamUrl;
      video.addEventListener("loadedmetadata", () => {
        video.play();
      });
    }
  }, [streamUrl]);

  return (
    <video
      ref={videoRef}
      controls
      style={{ width: "100%", maxWidth: "800px" }}
    />
  );
};

export const App = () => {
  // Replace with your actual HeyGen HLS stream URL
  const heyGenStreamUrl = "https://your-heygen-stream-url/path/playlist.m3u8";

  return (
    <div>
      <h1>HeyGen Live Stream</h1>
      <HLSVideoPlayer streamUrl={heyGenStreamUrl} />
      <hr />
      <h2>Audio Recorder</h2>
      <AudioRecorder />
    </div>
  );
};

export default App;