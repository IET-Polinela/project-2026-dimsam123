// Memastikan routing berjalan pertama kali aplikasi dijalankan
(function initApp() {
    const token = localStorage.getItem('access_token');
    // Jika sudah ada token, langsung arahkan ke dashboard
    if (token && window.location.hash === '#login') {
        window.location.hash = '#dashboard';
    }
})();