import React, { useEffect, useState } from "react";
import "../styles/home.css";
import { FaHome, FaUser, FaBell, FaEnvelope } from "react-icons/fa";
import { createPost, fetchPosts } from "../services/api";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const [user, setUser] = useState(null);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [posts, setPosts] = useState([]); // Store user posts
  const navigate = useNavigate(); // Hook for navigation

  useEffect(() => {
    // Retrieve user info from localStorage
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser)); // Parse JSON and update state
      } catch (error) {
        console.error("Error parsing user data:", error);
      }
    }

    // Fetch posts from the backend
    const token = localStorage.getItem("token");
    if (token) {
      fetchPosts(token)
        .then((data) => setPosts(data))
        .catch((error) => console.error("Error fetching posts:", error));
    }
  }, []);

  const handlePostSubmit = async () => {
    if (!title.trim() || !content.trim()) {
      alert("Title and content cannot be empty.");
      return;
    }

    try {
      const token = localStorage.getItem("token");
      if (!token) {
        throw new Error("You need to log in before creating a post.");
      }

      const newPost = await createPost(title, content, token);
      setPosts([newPost, ...posts]); // Add new post to the top of the list
      setTitle("");
      setContent("");
    } catch (error) {
      console.error("Post creation failed:", error.message);
      alert(error.message);
    }
  };

  return (
    <div className="home-container">
      {/* Sidebar */}
      <div className="sidebar">
        <h2 className="logo">MySocial</h2>
        <ul>
          <li><FaHome /> Home</li>
          <li><FaUser /> Profile</li>
          <li onClick={() => navigate("/chat")} style={{ cursor: "pointer" }}>
            <FaEnvelope /> Messages
          </li>          <li><FaBell /> Notifications</li>
        </ul>
      </div>

      {/* Main Content */}
      <div className="main-content">
        <div className="welcome-message">
          <h2>Welcome, {user ? user.username : "Guest"}! 👋</h2>
        </div>

        {/* Create Post Section */}
        <div className="post-box">
          <input
            type="text"
            placeholder="Enter post title..."
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="post-title-input"
          />
          <textarea
            placeholder="Write your post content..."
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="post-content-input"
          />
          <button onClick={handlePostSubmit}>Post</button>
        </div>

        {/* Display Posts */}
        <div className="feed">
          {posts.length > 0 ? (
            posts.map((post) => (
              <div className="post" key={post.id}>
                <h4>{post.title}</h4>
                <p>{post.content}</p>
                <small>Posted by {post.user_id}</small> {/* Update based on your post schema */}
              </div>
            ))
          ) : (
            <p>No posts yet. Be the first to post!</p>
          )}
        </div>
      </div>

      {/* Notifications Sidebar */}
      <div className="notifications-sidebar">
        <h3>Notifications</h3>
        <p>🔔 Jane Smith liked your post.</p>
      </div>
    </div>
  );
};

export default Home;
