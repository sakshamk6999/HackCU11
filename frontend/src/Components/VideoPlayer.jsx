import React from "react";

const VideoPlayer = ({ videoUrl }) => (
  <video controls style={{ width: "100%", maxWidth: "600px", height: "400px" }}>
    <source src={videoUrl} type="video/mp4" />
    Your browser does not support the video tag.
  </video>
);

export default VideoPlayer;