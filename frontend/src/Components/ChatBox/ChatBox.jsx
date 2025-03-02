import React, { useState } from "react";
import styled from "styled-components";
import MessageBubble from "./MessageBubble";

const ChatBoxContainer = styled.div`
  width: 400px;
  height: 400px;
  border: 1px solid #ccc;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  padding: 20px;
  background-color: #f7f7f7;
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding-right: 10px;
  margin-bottom: 20px;
`;

const ChatBox = ({messages}) => {

//   const handleSendMessage = (newMessage) => {
//     setMessages([...messages, { sender: "user", content: newMessage }]);
//     setTimeout(() => {
//       // Simulate a bot response
//       setMessages((prevMessages) => [
//         ...prevMessages,
//         { sender: "bot", content: "This is a bot reply." },
//       ]);
//     }, 1000);
//   };

  return (
    <ChatBoxContainer>
      <MessagesContainer>
        {messages.map((msg, index) => (
          <MessageBubble key={index} sender={msg.sender} content={msg.content} />
        ))}
      </MessagesContainer>
    </ChatBoxContainer>
  );
};

export default ChatBox;