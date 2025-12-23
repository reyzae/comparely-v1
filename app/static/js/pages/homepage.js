// ==========================================
// HOMEPAGE - Quick Compare Functionality
// File: homepage.js
// Deskripsi: JavaScript untuk halaman homepage
// ==========================================

// Tunggu sampai halaman selesai load
document.addEventListener('DOMContentLoaded', function () {

    // ==========================================
    // INISIALISASI ELEMEN
    // ==========================================

    // Ambil elemen-elemen yang diperlukan
    const device1Input = document.getElementById('device1Input');
    const device1Suggestions = document.getElementById('device1Suggestions');
    const device2Input = document.getElementById('device2Input');
    const device2Suggestions = document.getElementById('device2Suggestions');
    const compareBtn = document.getElementById('compareBtn');

    // Buat instance autocomplete untuk device 1
    const autocomplete1 = new AutocompleteSearch(device1Input, device1Suggestions);

    // Buat instance autocomplete untuk device 2
    const autocomplete2 = new AutocompleteSearch(device2Input, device2Suggestions);

    // ==========================================
    // VARIABEL GLOBAL
    // ==========================================

    // Variabel untuk menyimpan selected devices
    let selectedDevice1 = null;
    let selectedDevice2 = null;

    // ==========================================
    // EVENT LISTENERS
    // ==========================================

    // Event listener saat device 1 dipilih
    device1Input.addEventListener('deviceSelected', (e) => {
        selectedDevice1 = e.detail;
        console.log('Device 1 dipilih:', selectedDevice1);
        checkCompareReady();
    });

    // Event listener saat device 2 dipilih
    device2Input.addEventListener('deviceSelected', (e) => {
        selectedDevice2 = e.detail;
        console.log('Device 2 dipilih:', selectedDevice2);
        checkCompareReady();
    });

    // Event listener untuk tombol compare
    compareBtn.addEventListener('click', () => {
        if (selectedDevice1 && selectedDevice2) {
            // Redirect ke halaman compare
            window.location.href = `/compare-page?id1=${selectedDevice1.id}&id2=${selectedDevice2.id}`;
        }
    });

    // ==========================================
    // FUNCTIONS
    // ==========================================

    /**
     * Function untuk cek apakah kedua device sudah dipilih
     * Kalau sudah, enable tombol compare
     * Kalau belum, disable tombol compare
     */
    function checkCompareReady() {
        const helpText = document.getElementById('compareHelp');

        if (selectedDevice1 && selectedDevice2) {
            // Enable tombol compare
            compareBtn.disabled = false;

            // Hide helper text karena user sudah tahu apa yang harus dilakukan
            if (helpText) {
                helpText.style.display = 'none';
            }
        } else {
            // Disable tombol compare
            compareBtn.disabled = true;

            // Show helper text untuk guidance
            if (helpText) {
                helpText.style.display = 'block';
            }
        }
    }

});
