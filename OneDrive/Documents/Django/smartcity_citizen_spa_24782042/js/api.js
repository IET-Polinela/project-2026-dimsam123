const BACKEND_URL = 'http://127.0.0.1:8000';

async function requestAPI(endpoint, options = {}) {
    // Ambil token dari localStorage
    const accessToken = localStorage.getItem('access_token');
    
    // Siapkan headers dasar
    options.headers = options.headers || {};
    options.headers['Content-Type'] = 'application/json';

    // Jika token ada, sisipkan ke Header Authorization
    if (accessToken) {
        options.headers['Authorization'] = `Bearer ${accessToken}`;
    }

    const response = await fetch(`${BACKEND_URL}${endpoint}`, options);
    return response;
}