// PASTIKAN BARIS PERTAMA INI MEMAKAI URL LENGKAP KE PORT 8000
const API_URL = 'http://103.151.63.85:8010/api/reports/';

let currentTab = 'feed';
let editingReportId = null;

// FUNGSI UTAMA UNTUK MENGIRIMKAN TOKEN SECARA PAKSA
function getAuthHeaders() {
    const token = localStorage.getItem('access_token');
    console.log("Token yang diambil dari LocalStorage:", token); // Pastikan ini muncul di Console!

    // Jika token tidak ada, kita tambahkan log agar Anda tahu
    if (!token) {
        console.warn("PERINGATAN: Token tidak ditemukan di LocalStorage!");
    }

    return {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : ''
    };
}