import React, {useState, useEffect} from "react";
import {fetchUserItems, updateItem, deleteItem, addItem} from "../services/api";

const UserListPage = () => {
    const [items, setItems] = useState([]);
    const [editingItemId, setEditingItemId] = useState(null); // Track which item is being edited
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [itemToDelete, setItemToDelete] = useState(null);
    const [newItem, setNewItem] = useState({name: "", description: ""});

    // Fetch the user's current list on component mount
    useEffect(() => {
        loadUserItems();
    }, []);

    const loadUserItems = async () => {
        try {
            const data = await fetchUserItems();
            setItems(data);
        } catch (error) {
            console.error("Error fetching items:", error);
        }
    };

    const handleEditItem = (itemId, field, value) => {
        setItems(items.map(item =>
            item.item_id === itemId ? {...item, [field]: value} : item
        ));
    };

    const handleEditClick = async (item) => {
        if (editingItemId !== null && editingItemId !== item.item_id) {
            await handleUpdateItem(items.find(i => i.item_id === editingItemId)); // Save currently edited item
        }
        setEditingItemId(item.item_id); // Set new item to edit
    };

    const handleSaveClick = async (item) => {
        await handleUpdateItem(item);
        setEditingItemId(null);
    };

    const handleDeleteClick = (item) => {
        setItemToDelete(item);
        setShowDeleteModal(true);
    };

    const confirmDelete = async () => {
        await handleDeleteItem(itemToDelete.item_id);
        setShowDeleteModal(false);
        setItemToDelete(null); // Clear itemToDelete
    };

    const handleUpdateItem = async (item) => {
        try {
            await updateItem(item);
            // Optionally re-fetch items or update local state after saving
        } catch (error) {
            console.error("Error saving item:", error);
        }
    };

    const handleDeleteItem = async (itemId) => {
        try {
            await deleteItem(itemId);
            setItems(items.filter(item => item.item_id !== itemId));
        } catch (error) {
            console.error("Error deleting item:", error);
        }
    };

    const handleAddItem = async () => {
        try {
            const addedItem = await addItem(newItem);
            setItems([...items, addedItem]);
            setNewItem({name: "", description: ""});
        } catch (error) {
            console.error("Error adding item:", error);
        }
    };

    return (
        <div className="d-flex align-items-center justify-content-center">
            <div className="w-100 m-auto" style={{maxWidth: "660px", padding: "1rem"}}>
                <p className="h3">Your christmas list</p>
                <div className="card shadow">
                    <div className="card-header">My list</div>
                    <ul className="list-group list-group-flush">
                        {items.map(item => (
                            <li
                                key={item.item_id}
                                className="list-group-item d-flex justify-content-between align-items-center"
                            >
                                <div className="d-flex flex-column me-2" style={{flex: 1}}>
                                    {editingItemId === item.item_id ? (
                                        <>
                                            <input
                                                type="text"
                                                className="form-control mb-2"
                                                value={item.name}
                                                onChange={(e) => handleEditItem(item.item_id, "name", e.target.value)}
                                                placeholder="Item name"
                                            />
                                            <input
                                                type="text"
                                                className="form-control"
                                                value={item.description}
                                                onChange={(e) => handleEditItem(item.item_id, "description", e.target.value)}
                                                placeholder="Description"
                                            />
                                        </>
                                    ) : (
                                        <>
                                            <strong>{item.name}</strong>
                                            <small className="text-muted">{item.description}</small>
                                        </>
                                    )}
                                </div>
                                <div className="d-flex align-items-center">
                                    {editingItemId === item.item_id ? (
                                        <button
                                            className="btn btn-success btn-sm me-2"
                                            onClick={() => handleSaveClick(item)}
                                        >
                                            Save
                                        </button>
                                    ) : (
                                        <button
                                            className="btn btn-primary btn-sm me-2"
                                            onClick={() => handleEditClick(item)}
                                        >
                                            Edit
                                        </button>
                                    )}
                                    <button
                                        className="btn btn-danger btn-sm"
                                        onClick={() => handleDeleteClick(item)}
                                    >
                                        Delete
                                    </button>
                                </div>
                            </li>
                        ))}
                        {/* Add new item*/}
                        <li
                            className="list-group-item d-flex justify-content-between align-items-center bg-body-secondary border-secondary"
                            style={{ border: "2px dashed", borderRadius: "4px", marginTop: "15px" }}
                        >
                            <div className="d-flex flex-column me-2" style={{flex: 1}}>
                                <input
                                    type="text"
                                    className="form-control mb-2"
                                    value={newItem.name}
                                    onChange={(e) => setNewItem({...newItem, name: e.target.value})}
                                    placeholder="Item name"
                                />
                                <input
                                    type="text"
                                    className="form-control form-control-sm"
                                    value={newItem.description}
                                    onChange={(e) => setNewItem({...newItem, description: e.target.value})}
                                    placeholder="Description (optional)"
                                />
                            </div>
                            <div className="d-flex align-items-center">
                                <button
                                    className="btn btn-success btn-small d-flex align-items-center"
                                    onClick={handleAddItem}
                                >
                                    <i className="bi bi-plus-lg me-1"></i>
                                    Add Item
                                </button>
                            </div>
                        </li>
                    </ul>
                </div>

                {/* Delete Confirmation Modal */}
                {showDeleteModal && (
                    <div className="modal fade show d-block" style={{backgroundColor: "rgba(0, 0, 0, 0.5)"}}>
                        <div className="modal-dialog">
                            <div className="modal-content">
                                <div className="modal-header">
                                    <h5 className="modal-title">Are you sure?</h5>
                                    <button type="button" className="btn-close"
                                            onClick={() => setShowDeleteModal(false)}></button>
                                </div>
                                <div className="modal-body">
                                    Do you really want to delete "{itemToDelete?.name}"? This action cannot be undone.
                                </div>
                                <div className="modal-footer">
                                    <button type="button" className="btn btn-secondary"
                                            onClick={() => setShowDeleteModal(false)}>
                                        Cancel
                                    </button>
                                    <button type="button" className="btn btn-danger" onClick={confirmDelete}>
                                        Delete
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default UserListPage;

