import React, { useState } from 'react';
import { authenticateUser } from '../services/api';

const LandingPage = ({ onAuthenticate }) => {
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const token = await authenticateUser(password);
            if (token) {
                localStorage.setItem('authToken', token)
                onAuthenticate(); // Call the function passed from App.js to proceed to the next page
            } else {
                setError('Incorrect password. Please try again.');
            }
        } catch (error) {
            setError('An error occurred. Please try again.');
        }
    };

    return (
        <div className="flex-grow-1 d-flex align-items-center justify-content-center">
            <div className="w-100 m-auto" style={{maxWidth: "330px", padding: "1rem"}}>
                <p className="h4 mb-3 fw-normal">Please enter the password to access this app</p>
                <form onSubmit={handleSubmit}>
                    <div className="input-group mb-3">
                        <input
                            className="form-control"
                            type="password"
                            value={password}
                            onChange={handlePasswordChange}
                            placeholder="Enter password"
                            required
                        />
                        <button className="btn btn-outline-primary" type="submit">Enter</button>
                    </div>
                </form>
                {error && <p style={{color: 'red'}}>{error}</p>}
            </div>
        </div>
    );
};

export default LandingPage;
