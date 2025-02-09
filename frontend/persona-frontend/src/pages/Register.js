import { useState } from 'react';
import { registerUser } from '../services/api';
import { useNavigate } from 'react-router-dom';
import '../styles/auth.css';

const Register = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleRegister = async () => {
        if (password !== confirmPassword) {
            setError("Passwords do not match");
            return;
        }

        try {
            await registerUser(username, email, password, confirmPassword);
            navigate("/login"); // Redirect to Login after successful registration
        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-box">
                <h2 className="auth-title">Register</h2>
                {error && <p className="error-message">{error}</p>}
                <input 
                    type="text" 
                    placeholder="Username" 
                    className="auth-input"
                    onChange={(e) => setUsername(e.target.value)} 
                />
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
                <input 
                    type="password" 
                    placeholder="Confirm Password" 
                    className="auth-input"
                    onChange={(e) => setConfirmPassword(e.target.value)} 
                />
                <button onClick={handleRegister} className="auth-button">Register</button>
                <a href="/login" className="auth-link">Already have an account? Login</a>
            </div>
        </div>
    );
};

export default Register;
