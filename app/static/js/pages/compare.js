// ==========================================
// COMPARE PAGE - Fetch AI Analysis
// File: compare.js
// Deskripsi: JavaScript untuk halaman compare dengan AI
// ==========================================

// Tunggu sampai halaman selesai load
document.addEventListener('DOMContentLoaded', function () {

    // ==========================================
    // FADE-IN ANIMATION untuk cards
    // ==========================================
    addFadeInAnimation('.device-compare-card');
    addFadeInAnimation('.highlight-card');

    // ==========================================
    // FETCH AI ANALYSIS OTOMATIS
    // ==========================================

    // Ambil device IDs dari URL
    // Contoh URL: /compare-page?id1=1&id2=2
    const urlParams = new URLSearchParams(window.location.search);
    const deviceId1 = urlParams.get('id1');
    const deviceId2 = urlParams.get('id2');

    // Kalau ada kedua ID, fetch AI analysis
    if (deviceId1 && deviceId2) {
        fetchAIAnalysis(deviceId1, deviceId2);
    }

    // ==========================================
    // EVENT LISTENER untuk tombol retry
    // ==========================================
    const retryBtn = document.getElementById('retryBtn');
    if (retryBtn) {
        retryBtn.addEventListener('click', function () {
            // Retry fetch AI analysis
            fetchAIAnalysis(deviceId1, deviceId2);
        });
    }

});

// ==========================================
// FUNCTION: Fetch AI Analysis dari API
// ==========================================
function fetchAIAnalysis(id1, id2) {
    // Ambil elemen-elemen yang diperlukan
    const loadingDiv = document.getElementById('aiLoading');
    const resultDiv = document.getElementById('aiResult');
    const errorDiv = document.getElementById('aiError');

    // Reset state: tampilkan loading, sembunyikan result dan error
    loadingDiv.style.display = 'block';
    resultDiv.style.display = 'none';
    errorDiv.style.display = 'none';

    // Fetch ke endpoint /compare/ai
    // Pakai fetch API (built-in JavaScript, gak perlu library)
    fetch(`/compare/ai?id1=${id1}&id2=${id2}`)
        .then(response => {
            // Cek apakah response OK (status 200-299)
            if (!response.ok) {
                throw new Error('API error: ' + response.status);
            }
            // Parse response jadi JSON
            return response.json();
        })
        .then(data => {
            // Kalau berhasil, tampilkan hasil AI
            displayAIResult(data.ai_analysis);
        })
        .catch(error => {
            // Kalau gagal, tampilkan error
            console.error('Error fetching AI analysis:', error);
            showError();
        });
}

// ==========================================
// FUNCTION: Tampilkan hasil AI
// ==========================================
function displayAIResult(aiAnalysis) {
    const loadingDiv = document.getElementById('aiLoading');
    const resultDiv = document.getElementById('aiResult');
    const errorDiv = document.getElementById('aiError');

    // Sembunyikan loading
    loadingDiv.style.display = 'none';

    // Tampilkan result
    resultDiv.style.display = 'block';

    // Format AI analysis dengan line breaks
    // AI analysis dari backend sudah dalam format markdown-like
    // Kita convert ** jadi <strong> untuk bold
    let formattedText = aiAnalysis
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>') // Bold text
        .replace(/\n/g, '<br>'); // Line breaks

    // Masukkan ke dalam result div
    resultDiv.innerHTML = formattedText;

    // Sembunyikan error
    errorDiv.style.display = 'none';
}

// ==========================================
// FUNCTION: Tampilkan error state
// ==========================================
function showError() {
    const loadingDiv = document.getElementById('aiLoading');
    const resultDiv = document.getElementById('aiResult');
    const errorDiv = document.getElementById('aiError');

    // Sembunyikan loading dan result
    loadingDiv.style.display = 'none';
    resultDiv.style.display = 'none';

    // Tampilkan error
    errorDiv.style.display = 'block';
}
