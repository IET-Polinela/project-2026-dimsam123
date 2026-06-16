function setupLoginForm() {
    const loginForm = document.getElementById('login-form');
    if (!loginForm) return;

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // Mencegah reload halaman formal form
        
        const usernameInput = document.getElementById('username').value;
        const passwordInput = document.getElementById('password').value;

        try {
            const res = await requestAPI('/api/token/', {
                method: 'POST',
                body: JSON.stringify({ username: usernameInput, password: passwordInput })
            });

            if (res.status === 200) {
                const data = await res.json();
                // Simpan token ke localStorage browser
                localStorage.setItem('access_token', data.access);
                localStorage.setItem('refresh_token', data.refresh);
                
                // Alihkan ke halaman dashboard menggunakan hash routing
                window.location.hash = '#dashboard';
            } else {
                alert('Login Gagal! Periksa kembali username & password.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Tidak dapat terhubung ke server backend.');
        }
    });
}