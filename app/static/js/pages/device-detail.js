// ==========================================
// DEVICE DETAIL PAGE - Tab Switching & Share
// File: device-detail.js
// Deskripsi: JavaScript untuk halaman device detail
// ==========================================

// Tunggu sampai halaman selesai load
document.addEventListener('DOMContentLoaded', function () {

    // ==========================================
    // TAB SWITCHING FUNCTIONALITY
    // ==========================================

    /**
     * Function untuk switch tabs
     * @param {string} tabName - Nama tab yang mau ditampilkan
     */
    window.switchTab = function (tabName) {
        // Hide semua tab content
        const allTabs = document.querySelectorAll('.tab-content');
        allTabs.forEach(tab => {
            tab.classList.remove('active');
        });

        // Remove active dari semua buttons
        const allButtons = document.querySelectorAll('.tab-button');
        allButtons.forEach(btn => {
            btn.classList.remove('active');
        });

        // Show tab yang dipilih
        const selectedTab = document.getElementById(tabName + '-tab');
        if (selectedTab) {
            selectedTab.classList.add('active');
        }

        // Set button active
        event.target.classList.add('active');
    };

    // ==========================================
    // SHARE FUNCTIONALITY
    // ==========================================

    /**
     * Function untuk share device
     * Menggunakan Web Share API kalau tersedia
     * Kalau tidak, copy link ke clipboard
     */
    window.shareDevice = function () {
        // Ambil info device dari halaman
        const deviceName = document.querySelector('.device-header-enhanced h1').textContent;
        const deviceUrl = window.location.href;

        // Cek apakah browser support Web Share API
        if (navigator.share) {
            // Pakai Web Share API (modern browsers, mobile)
            navigator.share({
                title: deviceName + ' - COMPARELY',
                text: 'Lihat spesifikasi ' + deviceName,
                url: deviceUrl
            }).then(() => {
                showToast('Berhasil share device!', 'success');
            }).catch((error) => {
                console.log('Error sharing:', error);
            });
        } else {
            // Fallback: copy link ke clipboard
            navigator.clipboard.writeText(deviceUrl).then(() => {
                showToast('Link berhasil dicopy ke clipboard!', 'success');
            }).catch(() => {
                showToast('Gagal copy link', 'error');
            });
        }
    };

    // ==========================================
    // FADE-IN ANIMATION
    // ==========================================

    // Add fade-in animation saat page load
    addFadeInAnimation('.device-detail-grid');

});
