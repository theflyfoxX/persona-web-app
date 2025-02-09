import React, { useEffect, useState } from "react";
import "../styles/chat.css";
import { FaUserCircle, FaSearch, FaBars, FaPaperPlane } from "react-icons/fa";
import { fetchUsers, startConversation, checkConversation, fetchMessages, sendMessage } from "../services/api";

const ChatPage = () => {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [conversationId, setConversationId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [messageInput, setMessageInput] = useState("");
  const token = localStorage.getItem("token");
  const currentUser = JSON.parse(localStorage.getItem("user"));

  useEffect(() => {
    if (token) {
      fetchUsers(token)
        .then((data) => setUsers(data))
        .catch((error) => console.error("Error fetching users:", error));
    }
  }, [token]);
  const handleUserSelect = async (user) => {
    setSelectedUser(user);
    setConversationId(null);
    setMessages([]); // Reset messages

    // Sort user IDs to match backend check
    const sortedIds = [currentUser.id, user.id].sort();
    const sortedUser1 = sortedIds[0];
    const sortedUser2 = sortedIds[1];

    // Check if a conversation exists
    const response = await checkConversation(sortedUser1, sortedUser2, token);
    if (response.exists) {
        setConversationId(response.conversation_id);
        loadMessages(response.conversation_id);
    }
};

  const loadMessages = async (conversationId) => {
    const fetchedMessages = await fetchMessages(conversationId, token);
    setMessages(fetchedMessages);
  };

  const handleSendMessage = async () => {
    if (!messageInput.trim()) return; // Prevent empty messages

    try {
        let convId = conversationId;

        // If no conversation exists, create one first
        if (!convId) {
            const newConversation = await startConversation(currentUser.id, selectedUser.id, token);
            convId = newConversation.id; // Update conversationId
            setConversationId(convId); // Set in state
        }

        // Send the message
        const newMessage = await sendMessage(convId, currentUser.id, selectedUser.id, messageInput, token);

        // Update chat UI instantly
        setMessages([...messages, newMessage]);
        setMessageInput(""); // Clear input

    } catch (error) {
        console.error("Failed to send message:", error.message);
    }
};


  return (
    <div className="chat-container">
      {/* Sidebar for Contacts */}
      <div className="chat-sidebar">
        <div className="sidebar-header">
          <h2>Contacts</h2>
          <FaBars className="menu-icon" />
        </div>
        <div className="search-box">
          <FaSearch className="search-icon" />
          <input type="text" placeholder="Search users..." />
        </div>
        <div className="chat-list">
          {users.length > 0 ? (
            users.map((user) => (
              <div
                key={user.id}
                className={`chat-item ${selectedUser?.id === user.id ? "active" : ""}`}
                onClick={() => handleUserSelect(user)}
              >
                <FaUserCircle className="chat-avatar" />
                <div className="chat-info">
                  <h4>{user.username}</h4>
                  <p>{user.email}</p>
                </div>
              </div>
            ))
          ) : (
            <p>No users found</p>
          )}
        </div>
      </div>

      {/* Chat Window */}
      <div className="chat-window">
        {selectedUser ? (
          <>
            <div className="chat-header">
              <h3>Chat with {selectedUser.username}</h3>
            </div>

            {/* Messages Display */}
            <div className="chat-messages">
              {messages.map((msg, index) => (
                <div
                  key={index}
                  className={`message ${msg.sender_id === currentUser.id ? "sent" : "received"}`}
                >
                  {msg.message}
                </div>
              ))}
            </div>

            {/* Message Input */}
            <div className="chat-input">
              <input
                type="text"
                placeholder="Type a message..."
                value={messageInput}
                onChange={(e) => setMessageInput(e.target.value)}
              />
              <button onClick={handleSendMessage}>
                <FaPaperPlane />
              </button>
            </div>
          </>
        ) : (
          <div className="no-chat-selected">
            <p>Select a user to start a conversation</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatPage;
