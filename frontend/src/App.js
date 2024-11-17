import './App.css';
import React, {useEffect, useState} from 'react';
import LandingPage from './pages/LandingPage';
import UserSelectionPage from './pages/UserSelection';
import UserListPage from './pages/MyList';
import OtherUsersListsPage from "./pages/OtherLists";
import {ReactComponent as Logo} from './img/christmas-tree.svg'


function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [userId, setUserId] = useState(null);
    const [showUserList, setShowUserList] = useState(true)

    const handleAuthentication = () => {
        setIsAuthenticated(true); // Update state to indicate user is authenticated
    };

    const handleUserSelect = (id) => {
        setUserId(id);
        sessionStorage.setItem('userId', id);
    };

    const logout = () => {
        setUserId(null)
        sessionStorage.clear()
    }

    useEffect(() => {
        const storedSessionToken = localStorage.getItem('authToken');
        if (storedSessionToken) {
            setIsAuthenticated(true); // Assuming authenticated users have a user_id
        }
    }, []);

    return (
        <div className="d-flex flex-column min-vh-100">
            {!isAuthenticated ? (
                <LandingPage onAuthenticate={handleAuthentication}/>
            ) : !userId ? (
                <UserSelectionPage onUserSelect={handleUserSelect}/>
            ) : (
                <div className="d-flex flex-column flex-grow-1">
                    <header className="navbar d-flex justify-content-between align-items-center mx-2">
                        <div className="d-flex align-items-center">
                            <div style={{ height: "32px", width: "32px"}}>
                                <Logo />
                            </div>
                            <h1 className="mb-0">Christmas lists</h1>
                        </div>

                        <div className="btn-group">
                            <button
                                className={`btn btn-lg ${showUserList ? "btn-primary" : "btn-outline-primary"}`}
                                onClick={() => setShowUserList(true)}
                            >
                                Your list
                            </button>
                            <button
                                className={`btn btn-lg ${!showUserList ? "btn-primary" : "btn-outline-primary"}`}
                                onClick={() => setShowUserList(false)}
                            >
                                Other's lists
                            </button>
                        </div>

                        <button
                            className="btn btn-danger"
                            onClick={logout}
                        >
                            Logout
                        </button>
                    </header>

                    <div className="bg-body-tertiary flex-grow-1">
                        <div className="fade-container">
                            {showUserList ? <UserListPage/> : <OtherUsersListsPage/>}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default App;
