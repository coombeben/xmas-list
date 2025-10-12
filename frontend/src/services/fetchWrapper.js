const BASE_URL = import.meta.env.VITE_API_URL || 'https://christmas.coombe.xyz/api';

const fetchWrapper = async (url, options = {}) => {
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    const token = localStorage.getItem('authToken')
    if (token && !url.includes('/authenticate')) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    url = url.replace('<user_id>', sessionStorage.getItem('userId'));

    const newOptions = {
        ...options,
        headers,
    };

    try {
        const response = await fetch(`${BASE_URL}${url}`, newOptions);

        // Handle 401 Unauthorized responses globally
        if (response.status === 401) {
            localStorage.clear()
            sessionStorage.clear()
            window.location.reload();
            return null;
        }

        return await response;
    } catch (error) {
        console.error(`Error fetching ${url}:`, error);
        throw error;
    }
}

export default fetchWrapper;
