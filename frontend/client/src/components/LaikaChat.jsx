import React, { useState, useEffect } from 'react';
import './LaikaChat.css';
import { IoMdSend, IoMdClose } from 'react-icons/io';

const LaikaChat = ({ logData, closeChat }) => {
    const [messages, setMessages] = useState([]);

    useEffect(() => {
        const greeting = `Hello! I'm Laika. I see you're looking at your log of the ${logData.name}. It's a beautiful ${logData.type}. What would you like to know about it?`;
        setMessages([{ from: 'laika', text: greeting }]);
    }, [logData]);

  return (
    <div className='laika-overlay'>
        <div className='laika-chat-window'>
            <div className='laika-header'>
                <h3>Chat with Laika</h3>
                <button onClick={closeChat} className='close-btn'><IoMdClose size={24} /></button>
            </div>
            <div className='laika-conversation-area'>
                {messages.map((msg, index) => (
                    <div key={index} className={`chat-bubble ${msg.from}`}>
                        {msg.text}
                    </div>
                ))}
            </div>
            <div className='laika-input-area'>
                <input type='text' placeholder='Ask about this celestial object...' />
                <button className='send-btn'><IoMdSend size={24} /></button>
            </div>
        </div>
    </div>
  )
}

export default LaikaChat