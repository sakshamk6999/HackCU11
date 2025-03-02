import React from "react";
import styled from "styled-components";

const MessageContainer = styled.div`
  display: flex;
  justify-content: ${(props) => (props.sender === "bot" ? "flex-start" : "flex-end")};
  margin-bottom: 10px;
`;

const Bubble = styled.div`
  max-width: 70%;
  padding: 10px;
  border-radius: 15px;
  background-color: ${(props) => (props.sender === "bot" ? "#e1e1e1" : "#007bff")};
  color: ${(props) => (props.sender === "bot" ? "black" : "white")};
  word-wrap: break-word;
`;

const MessageBubble = ({ sender, content }) => {
  return (
    <MessageContainer sender={sender}>
      <Bubble sender={sender}>{content}</Bubble>
    </MessageContainer>
  );
};

export default MessageBubble;