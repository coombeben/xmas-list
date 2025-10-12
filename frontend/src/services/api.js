import fetchWrapper from "./fetchWrapper";

// Submit site password
export const authenticateUser = async (password) => {
    const response = await fetch(import.meta.env.VITE_API_URL + '/authenticate', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ password }),
    });
    if (!response.ok) throw new Error("Error authenticating")
    const data = await response.json()
    return data.token;
};

// Get list of all existing users
export const fetchUsers = async () => {
    const response = await fetchWrapper('/users');
    if (!response.ok) throw new Error('Error fetching users')
    return response.json()
};

// Create a new user
export const createUser = async (name) => {
    const response = await fetchWrapper('/users', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ name }),
    });
    if (!response.ok) throw new Error('Error creating user');
    return await response.json();
};

// Get user's existing list
export const fetchUserItems = async () => {
    const response = await fetchWrapper('/users/<user_id>/items');
    if (!response.ok) throw new Error('Error fetching user list');
    return await response.json()
};

// Update the properties of an item
export const updateItem = async (item) => {
    const response = await fetchWrapper(`/users/<user_id>/items/${item.item_id}`, {
        method: 'PUT',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(item),
    });
    if (!response.ok) throw new Error('Error saving item');
    return null
};

// Delete an item from list
export const deleteItem = async (itemId) => {
    const response = await fetchWrapper(`/users/<user_id>/items/${itemId}`, {
        method: 'DELETE',
    });
    if (!response.ok) throw new Error('Error deleting item');
}

// Add an item to the list
export const addItem = async (item) => {
    const response = await fetchWrapper(`/users/<user_id>/items`, {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(item),
    });
    if (!response.ok) throw new Error('Error adding item');
    return await response.json()
};

// Fetch all other users' lists
export const fetchOtherUsersLists = async () => {
    const response = await fetchWrapper("/users/<user_id>/lists");
    if (!response.ok) throw new Error("Failed to fetch other users' lists");
    return await response.json();
};

// Mark an item as purchased by the current user
export const purchaseItem = async (itemId) => {
    const response = await fetchWrapper(`/users/<user_id>/items/${itemId}/purchase`, {
        method: "POST",
    });
    if (!response.ok) throw new Error("Failed to mark item as purchased");
};

// Delete the purchase made by the current user
export const deletePurchase = async (itemId) => {
    const response = await fetchWrapper(`/users/<user_id>/items/${itemId}/purchase`, {
        method: "DELETE",
    });
    if (!response.ok) throw new Error("Failed to delete purchase");
};
