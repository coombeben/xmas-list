import React, {useState, useEffect} from "react";
import {fetchOtherUsersLists, purchaseItem, deletePurchase} from "../services/api";

const OtherUsersListsPage = () => {
    const [otherUsersLists, setOtherUsersLists] = useState([]);

    useEffect(() => {
        loadOtherUsersLists();
    }, []);

    const loadOtherUsersLists = async () => {
        try {
            const data = await fetchOtherUsersLists();
            setOtherUsersLists(data);
        } catch (error) {
            console.error("Error fetching other users' lists:", error);
        }
    };

    const handlePurchaseItem = async (itemId) => {
        try {
            await purchaseItem(itemId);
            loadOtherUsersLists(); // Refresh the lists to update purchase status
        } catch (error) {
            console.error("Error marking item as purchased:", error);
        }
    };

    const handleDeletePurchase = async (itemId) => {
        try {
            await deletePurchase(itemId);
            loadOtherUsersLists(); // Refresh the lists to update purchase status
        } catch (error) {
            console.error("Error deleting purchase:", error);
        }
    };

    return (
        <div className="row pt-3 px-3">
            {otherUsersLists.map(user => (
                <div
                    key={user.user_id}
                    className="col-12 col-md-6 col-lg-4 mb-4"
                >
                    <div className="card shadow">
                        <div className="card-header">{user.username}'s list</div>
                        <ul className="list-group list-group-flush">
                            {user.items.map(item => (
                                <li
                                    key={item.item_id}
                                    className="list-group-item d-flex justify-content-between align-items-center"
                                >
                                    <div className="d-flex flex-column me-2" style={{ maxWidth: '70%' }}>
                                        <strong>{item.name}</strong>
                                        <small className="text-muted">{item.description}</small>
                                        {item.purchased_by && (
                                            <div>
                                                <span>Purchased by: </span>
                                                <strong>{item.purchased_by}</strong>
                                            </div>
                                        )}
                                    </div>
                                    <div className="d-flex flex-column ms-2">
                                        {item.purchased_by_user_id !== null && item.purchased_by_user_id.toString() === sessionStorage.getItem('userId') ? (
                                            <button
                                                className="btn btn-danger btn-sm"
                                                onClick={() => handleDeletePurchase(item.item_id)}
                                            >
                                                Cancel purchase
                                            </button>
                                        ) : item.purchased_by_user_id === null ? (
                                            <button
                                                className="btn btn-primary btn-sm"
                                                onClick={() => handlePurchaseItem(item.item_id)}
                                            >
                                                Mark as purchased
                                            </button>
                                        ) : (
                                            <></>
                                        )}
                                    </div>
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default OtherUsersListsPage;

