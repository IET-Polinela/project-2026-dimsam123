const routes = {
    '#login': `
        <div class="container d-flex justify-content-center align-items-center min-vh-100">
            <div class="col-12 col-md-6 col-lg-4 bg-white p-4 rounded shadow-sm">
                <h3 class="text-center mb-4"><i class="bi bi-box-arrow-in-right"></i> Login</h3>
                <form id="login-form">
                    <div class="mb-3">
                        <label class="form-label">Username</label>
                        <input type="text" id="username" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Password</label>
                        <input type="password" id="password" class="form-control" required>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Login</button>
                </form>
            </div>
        </div>
    `,
    '#dashboard': `
        <div class="container-fluid">
            <div class="row">
                <nav class="col-12 col-lg-3 bg-dark text-white p-3 min-vh-100">
                    <h4><i class="bi bi-building"></i> SmartCity</h4>
                    <hr>
                    <ul class="nav flex-column">
                        <li class="nav-item"><a class="nav-link text-white" href="#dashboard">Dashboard</a></li>
                        <li class="nav-item"><a class="nav-link text-danger" href="#" id="logout-btn">Logout</a></li>
                    </ul>
                </nav>
                <main class="col-12 col-lg-9 p-4">
                    <h2>Selamat Datang di Dashboard</h2>
                    <p>Anda berhasil login menggunakan JWT Token.</p>
                </main>
            </div>
        </div>
    `
};

function handleRouting() {
    const hash = window.location.hash || '#login'; // Default ke #login jika kosong
    const appDiv = document.getElementById('app');
    
    // Masukkan template HTML sesuai hash url
    appDiv.innerHTML = routes[hash] || '<h1>404 Not Found</h1>';

    // Jalankan setup form jika masuk halaman login
    if (hash === '#login') {
        setupLoginForm();
    }
}

// Deteksi perubahan hash url dan saat halaman pertama di-load
window.addEventListener('hashchange', handleRouting);
window.addEventListener('DOMContentLoaded', handleRouting);