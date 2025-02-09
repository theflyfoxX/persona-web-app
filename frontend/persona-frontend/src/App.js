import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Home from './pages/Home';
import ProtectedRoute from './components/ProtectedRoute';
import ChatPage from "./pages/ChatPage";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />

                {/* Protected Routes */}
                <Route 
                    path="/home" 
                    element={
                        <ProtectedRoute>
                            <Home />
                        </ProtectedRoute>
                    } 
                />
                <Route 
                    path="/chat" 
                    element={
                        <ProtectedRoute>
                            <ChatPage  />
                        </ProtectedRoute>
                    } 
                />
                {/* <Route 
                    path="/friends" 
                    element={
                        <ProtectedRoute>
                            <Friends />
                        </ProtectedRoute>
                    } 
                /> */}

                {/* Default Route */}
                <Route path="*" element={<Navigate to="/home" />} />
            </Routes>
        </Router>
    );
}

export default App;
