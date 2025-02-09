import axios from 'axios';

const API_URL = "http://localhost:9000"; // Adjust this if your backend URL is different


export const loginUser = async (email, password) => {
    try {
        const response = await axios.post(
            `${API_URL}/auth/login`,
            new URLSearchParams({
                username: email,
                password: password
            }),
            { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
        );

        console.log("Login API Response:", response.data); 

        const { access_token, user } = response.data;

        if (!access_token || !user) {
            console.error("No access token received");
            throw new Error("Invalid login response");
        }

        // ✅ Store the token and ensure it is correctly set before using it
        localStorage.setItem("token", access_token);
        localStorage.setItem("user", JSON.stringify(user));

        console.log("Token stored (After Setting):", localStorage.getItem("token"));

        return { access_token, user };  // ✅ Return token explicitly instead of relying on localStorage
    } catch (error) {
        console.error("Login Error:", error.response?.data || error.message);
        throw new Error(error.response?.data?.detail || "Login failed");
    }
};


// User Registration
export const registerUser = async (username, email, password, confirmPassword) => {
    try {
        const response = await axios.post(`${API_URL}/users/`, {
            username,
            email,
            password,
            confirm_password: confirmPassword
        });
        return response.data;
    } catch (error) {
        throw new Error(error.response?.data?.detail || "Registration failed");
    }
};

// Get Current User// Get Current User
export const getCurrentUser = async (token = null) => {
    try {
        token = token || localStorage.getItem("token");  // Use passed token if available

        console.log("Retrieved Token:", token);  // ✅ Debugging step

        if (!token) {
            throw new Error("User is not authenticated");
        }

        const response = await axios.get(`${API_URL}/auth/users/me`, {
            headers: { Authorization: `Bearer ${token}` }
        });

        localStorage.setItem("user", JSON.stringify(response.data));
        return response.data;
    } catch (error) {
        console.error("Unauthorized:", error.response?.data || error.message);
        throw new Error("Unauthorized");
    }
};
export const createPost = async (title, content, token = null) => {
    try {
        token = token || localStorage.getItem("token");  // Use the passed token

        console.log("Retrieved Token:", token);  // ✅ Debugging step

        if (!token) throw new Error("User is not authenticated");

        const response = await axios.post(
            `${API_URL}/posts/`, 
            { title, content }, 
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            }
        );

        console.log("Post created:", response.data);
        return response.data;

    } catch (error) {
        console.error("Error creating post:", error.response?.data || error.message);
        throw new Error(error.response?.data?.detail || "Failed to create post");
    }
};
export const fetchPosts = async (token) => {
    try {
        const response = await axios.get(`${API_URL}/posts/`, {
            headers: { Authorization: `Bearer ${token}` }
        });
        return response.data; // This returns the list of posts
    } catch (error) {
        console.error("Failed to fetch posts:", error.response?.data || error.message);
        throw new Error("Failed to fetch posts");
    }
};



export const fetchUsers = async (token) => {
    try {
        const response = await axios.get(`${API_URL}/users`, {
            headers: { Authorization: `Bearer ${token}` },
        });
        return response.data;
    } catch (error) {
        console.error("Failed to fetch users:", error.response?.data || error.message);
        throw new Error("Failed to retrieve users");
    }
};

export const startConversation = async (user1_id, user2_id, token) => {
    // Ensure user IDs are sorted
    const sortedIds = [user1_id, user2_id].sort();
    const sortedUser1 = sortedIds[0];
    const sortedUser2 = sortedIds[1];

    try {
        const response = await axios.post(
            `http://localhost:9000/conversations/start?user1_id=${sortedUser1}&user2_id=${sortedUser2}`,
            {},
            { headers: { Authorization: `Bearer ${token}` } }
        );
        return response.data; // Returns conversation ID
    } catch (error) {
        console.error("Failed to start conversation:", error.response?.data || error.message);
        throw new Error("Failed to start conversation");
    }
};


export const fetchMessages = async (conversationId, token) => {
    try {
        console.log(`📨 Fetching messages for Conversation ID: ${conversationId}`);
        const response = await axios.get(
            `http://localhost:9000/messages/${conversationId}`,
            { headers: { Authorization: `Bearer ${token}` } }
        );
        console.log("✅ Messages Retrieved:", response.data);
        return response.data; // Returns list of messages
    } catch (error) {
        console.error("Failed to fetch messages:", error.response?.data || error.message);
        return [];
    }
};

// Send a message
export const sendMessage = async (conversationId, senderId, receiverId, message, token) => {
    try {
        const response = await axios.post(
            "http://localhost:9000/messages/",
            {
                conversation_id: conversationId,
                sender_id: senderId,
                receiver_id: receiverId,
                message: message,
                media: null,  // Media support can be added later
            },
            { headers: { Authorization: `Bearer ${token}` } }
        );
        return response.data;
    } catch (error) {
        console.error("Failed to send message:", error.response?.data || error.message);
        throw new Error("Failed to send message");
    }
};
