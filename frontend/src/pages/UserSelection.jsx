import React, {useState, useEffect} from 'react';
import {fetchUsers, createUser} from '../services/api';

const UserSelectionPage = ({onUserSelect}) => {
    const [users, setUsers] = useState([]);
    const [newUserName, setNewUserName] = useState('');
    const [error, setError] = useState(null);
    const [showSpoilerModal, setShowSpoilerModal] = useState(false);
    const [userSelected, setUserSelected] = useState(null);

    // Fetch users when component mounts
    useEffect(() => {
        const loadUsers = async () => {
            try {
                const fetchedUsers = await fetchUsers();
                setUsers(fetchedUsers);
            } catch (error) {
                setError('Failed to load users. Please try again.');
            }
        };
        loadUsers();
    }, []);

    const confirmUserSelect = () => {
        onUserSelect(userSelected.user_id); // Pass selected user ID back to App.js
    };

    const handleNewUserSubmit = async (e) => {
        e.preventDefault();
        try {
            const newUser = await createUser(newUserName);
            setUsers([...users, newUser]); // Add new user to the list
            onUserSelect(newUser.user_id); // Pass new user ID back to App.js
        } catch (error) {
            setError('Failed to create user. Please try again.');
        }
    };

    const handleUserSelectClick = (user) => {
        setUserSelected(user)
        setShowSpoilerModal(true)
    }

    return (
        <div className="flex-grow-1 d-flex align-items-center justify-content-center">
            <div className="w-100 m-auto" style={{maxWidth: "330px", padding: "1rem"}}>
                <p className="h3">Select or create a user</p>
                <div>
                    <p className="h4">Existing users</p>
                    {users.length > 0 ? (
                        <div className="list-group pb-3">
                            {users.map((user) => (
                                <div className="clickable list-group-item list-group-item-action align-items-center d-flex py-2 gap-3"
                                     key={user.user_id} onClick={() => handleUserSelectClick(user)}>
                                    <div className="circle-initial text-white" style={{ background: user.colour }}>{user.name[0].toUpperCase()}</div>
                                    <p className="mb-0">{user.name}</p>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <p>No users available.</p>
                    )}
                </div>

                <div>
                    <p className="h4">Create new user</p>
                    <form onSubmit={handleNewUserSubmit}>
                        <div className="input-group mb-3">
                            <input
                                className="form-control"
                                type="text"
                                value={newUserName}
                                onChange={(e) => setNewUserName(e.target.value)}
                                placeholder="Enter new user name"
                                required
                            />
                            <button className="btn btn-outline-primary" type="submit">Create User</button>
                        </div>
                    </form>
                </div>
                {error && <p style={{color: 'red'}}>{error}</p>}
            </div>

            {/* Login Confirmation Modal */}
            {showSpoilerModal && (
                <div className="modal fade show d-block" style={{backgroundColor: "rgba(0, 0, 0, 0.5)"}}>
                    <div className="modal-dialog">
                        <div className="modal-content">
                            <div className="modal-header">
                                <h5 className="modal-title">Spoilers!</h5>
                                <button type="button" className="btn-close"
                                        onClick={() => setShowSpoilerModal(false)}></button>
                            </div>
                            <div className="modal-body">
                                Are you certain that you want to login as "{userSelected?.name}"? You'll be able to see what others have purchased for you if this isn't you!
                            </div>
                            <div className="modal-footer">
                                <button
                                    type="button"
                                    className="btn btn-secondary"
                                    onClick={() => setShowSpoilerModal(false)}
                                >
                                    Cancel
                                </button>
                                <button type="button" className="btn btn-primary" onClick={confirmUserSelect}>
                                    Login
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default UserSelectionPage;
