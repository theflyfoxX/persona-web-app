import { useState } from 'react';
import { loginUser } from '../services/api';
import { useNavigate } from 'react-router-dom';
import '../styles/auth.css';
import { getCurrentUser } from '../services/api';
const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = async () => {
        try {
            if (!email.trim() || !password.trim()) {
                alert("Please enter both email and password.");
                return;
            }
    
            const { access_token, user } = await loginUser(email, password);
            console.log("User logged in:", user);
    
            if (!access_token) {
                throw new Error("Login successful, but no token received.");
            }
    
            // Fetch user data using the token
            await getCurrentUser(access_token);
    
            // ✅ Ensure user data is correctly stored before navigating
            localStorage.setItem("user", JSON.stringify(user));
    
            setTimeout(() => { // ✅ Delay navigation to ensure state updates
                navigate("/dashboard"); // Change "/dashboard" to the correct route
            }, 100);  
    
        } catch (error) {
            console.error("Login failed:", error.message);
            alert(error.message);
        }
    };
    
    
    return (
        <div className="auth-container">
            <div className="auth-box">
                <h2 className="auth-title">Login</h2>
                {error && <p className="error-message">{error}</p>}
                <input 
                    type="email" 
                    placeholder="Email" 
                    className="auth-input"
                    onChange={(e) => setEmail(e.target.value)} 
                />
                <input 
                    type="password" 
                    placeholder="Password" 
                    className="auth-input"
                    onChange={(e) => setPassword(e.target.value)} 
                />
                <button onClick={handleLogin} className="auth-button">Login</button>
                <a href="/register" className="auth-link">Don't have an account? Sign up</a>
            </div>
        </div>
    );
};

export default Login;
