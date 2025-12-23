// ==========================================
// DEVICES PAGE - Compare Bar Functionality
// File: devices.js
// Deskripsi: JavaScript untuk halaman devices list
// ==========================================

// Tunggu sampai halaman selesai load
document.addEventListener('DOMContentLoaded', function () {

    // ==========================================
    // INISIALISASI ELEMEN
    // ==========================================

    // Ambil elemen-elemen yang diperlukan
    const compareBar = document.getElementById('compareBar');
    const selectedDevicesContainer = document.getElementById('selectedDevices');
    const compareButton = document.getElementById('compareButton');
    const clearButton = document.getElementById('clearButton');

    // View toggle elements
    const gridViewBtn = document.getElementById('gridViewBtn');
    const listViewBtn = document.getElementById('listViewBtn');
    const devicesGrid = document.getElementById('devicesGrid');
    const devicesList = document.getElementById('devicesList');

    // ==========================================
    // VARIABEL GLOBAL
    // ==========================================

    // Array untuk menyimpan device yang dipilih (maksimal 2)
    let selectedDevices = [];

    // ==========================================
    // VIEW TOGGLE FUNCTIONALITY
    // ==========================================

    // Load saved view preference from localStorage
    const savedView = localStorage.getItem('devices_view_preference') || 'grid';
    setView(savedView);

    // Event listener untuk grid view button
    if (gridViewBtn) {
        gridViewBtn.addEventListener('click', function () {
            setView('grid');
            localStorage.setItem('devices_view_preference', 'grid');
        });
    }

    // Event listener untuk list view button
    if (listViewBtn) {
        listViewBtn.addEventListener('click', function () {
            setView('list');
            localStorage.setItem('devices_view_preference', 'list');
        });
    }

    /**
     * Function untuk set view (grid atau list)
     */
    function setView(view) {
        if (view === 'grid') {
            // Show grid, hide list
            if (devicesGrid) devicesGrid.style.display = 'grid';
            if (devicesList) devicesList.style.display = 'none';

            // Update button states
            if (gridViewBtn) gridViewBtn.classList.add('active');
            if (listViewBtn) listViewBtn.classList.remove('active');
        } else {
            // Show list, hide grid
            if (devicesGrid) devicesGrid.style.display = 'none';
            if (devicesList) devicesList.style.display = 'flex';

            // Update button states
            if (gridViewBtn) gridViewBtn.classList.remove('active');
            if (listViewBtn) listViewBtn.classList.add('active');
        }
    }

    // ==========================================
    // DUAL-RANGE PRICE SLIDER - ENHANCED
    // ==========================================

    const minPriceSlider = document.getElementById('minPriceSlider');
    const maxPriceSlider = document.getElementById('maxPriceSlider');
    const minPriceLabel = document.getElementById('minPriceLabel');
    const maxPriceLabel = document.getElementById('maxPriceLabel');
    const sliderTrack = document.getElementById('sliderTrack');
    const presetButtons = document.querySelectorAll('.preset-btn');

    if (minPriceSlider && maxPriceSlider) {

        // Format number to Rupiah with proper formatting
        function formatRupiah(number) {
            const millions = number / 1000000;
            if (millions >= 1) {
                const formatted = millions % 1 === 0 ? millions.toFixed(0) : millions.toFixed(1);
                return `Rp ${formatted} Jt`;
            } else if (number === 0) {
                return 'Rp 0';
            } else {
                return 'Rp ' + (number / 1000).toFixed(0) + 'rb';
            }
        }

        // Update price display and slider track
        function updatePriceDisplay() {
            const minValue = parseInt(minPriceSlider.value);
            const maxValue = parseInt(maxPriceSlider.value);

            // Ensure min doesn't exceed max
            if (minValue > maxValue) {
                minPriceSlider.value = maxValue;
                return;
            }

            // Update inline labels
            if (minPriceLabel) {
                minPriceLabel.textContent = formatRupiah(minValue);
            }
            if (maxPriceLabel) {
                maxPriceLabel.textContent = formatRupiah(maxValue);
            }

            // Update visual track
            updateSliderTrack();
        }

        // Update slider track visual
        function updateSliderTrack() {
            const minValue = parseInt(minPriceSlider.value);
            const maxValue = parseInt(maxPriceSlider.value);
            const min = parseInt(minPriceSlider.min);
            const max = parseInt(minPriceSlider.max);

            const percentMin = ((minValue - min) / (max - min)) * 100;
            const percentMax = ((maxValue - min) / (max - min)) * 100;

            sliderTrack.style.left = percentMin + '%';
            sliderTrack.style.width = (percentMax - percentMin) + '%';
        }

        // Event listeners for sliders
        minPriceSlider.addEventListener('input', updatePriceDisplay);
        maxPriceSlider.addEventListener('input', updatePriceDisplay);

        // Enable pointer events for thumbs only
        minPriceSlider.style.pointerEvents = 'auto';
        maxPriceSlider.style.pointerEvents = 'auto';

        // Initialize
        updatePriceDisplay();

        // Touch feedback for mobile
        [minPriceSlider, maxPriceSlider].forEach(slider => {
            slider.addEventListener('mousedown', () => {
                slider.style.cursor = 'grabbing';
            });
            slider.addEventListener('mouseup', () => {
                slider.style.cursor = 'grab';
            });
        });
    }

    // ==========================================
    // PRICE PRESET BUTTONS
    // ==========================================

    if (presetButtons.length > 0) {
        presetButtons.forEach(btn => {
            btn.addEventListener('click', function () {
                const minPrice = this.getAttribute('data-min');
                const maxPrice = this.getAttribute('data-max');

                // Update sliders
                if (minPriceSlider) minPriceSlider.value = minPrice;
                if (maxPriceSlider) maxPriceSlider.value = maxPrice;

                updatePriceDisplay();

                // Visual feedback
                presetButtons.forEach(b => b.classList.remove('active'));
                this.classList.add('active');
            });
        });
    }


    // ==========================================
    // ACTIVE FILTERS BADGES (COMPACT)
    // ==========================================

    const activeFiltersBadges = document.getElementById('activeFiltersBadges');
    const badgesContainer = document.getElementById('badgesContainer');

    // Function to update filter pills
    function updateFilterPills() {
        const pills = [];

        // Get current filter values from URL or form
        const urlParams = new URLSearchParams(window.location.search);

        // Category filter
        const category = urlParams.get('category');
        if (category) {
            const categoryName = document.querySelector(`#category option[value="${category}"]`)?.text || category;
            pills.push({ type: 'category', label: categoryName, value: category });
        }

        // Brand filter
        const brand = urlParams.get('brand');
        if (brand) {
            pills.push({ type: 'brand', label: brand, value: brand });
        }

        // RAM filter
        const ram = urlParams.get('ram');
        if (ram) {
            pills.push({ type: 'ram', label: `RAM: ${ram}`, value: ram });
        }

        // Storage filter
        const storage = urlParams.get('storage');
        if (storage) {
            pills.push({ type: 'storage', label: `Storage: ${storage}`, value: storage });
        }

        // Min/Max price filter
        const minPrice = urlParams.get('min_price');
        const maxPrice = urlParams.get('max_price');

        if (minPrice && parseInt(minPrice) > 0) {
            const priceLabel = formatRupiah(parseInt(minPrice));
            pills.push({ type: 'min_price', label: `Min: ${priceLabel}`, value: minPrice });
        }

        if (maxPrice && parseInt(maxPrice) < 50000000) {
            const priceLabel = formatRupiah(parseInt(maxPrice));
            pills.push({ type: 'max_price', label: `Max: ${priceLabel}`, value: maxPrice });
        }

        // Show/hide badges
        if (pills.length > 0 && activeFiltersBadges && badgesContainer) {
            activeFiltersBadges.style.display = 'flex';

            // Render compact badges
            badgesContainer.innerHTML = pills.map(pill => `
                <span class="filter-badge">
                    ${pill.label}
                    <button type="button" class="filter-badge-remove" onclick="removeFilter('${pill.type}')">&times;</button>
                </span>
            `).join('');
        } else if (activeFiltersBadges) {
            activeFiltersBadges.style.display = 'none';
        }
    }

    // Function to remove individual filter
    window.removeFilter = function (filterType) {
        const url = new URL(window.location);
        url.searchParams.delete(filterType);
        window.location.href = url.toString();
    };

    // Clear all filters (if needed later)
    // Remove clearAllButton section as it's not used anymore

    // Initialize filter pills on page load
    updateFilterPills();

    // Helper function for formatting rupiah (already exists above but making it global)
    function formatRupiah(number) {
        const millions = number / 1000000;
        if (millions >= 1) {
            const formatted = millions % 1 === 0 ? millions.toFixed(0) : millions.toFixed(1);
            return `Rp ${formatted} Jt`;
        } else {
            return 'Rp ' + number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
        }
    }


    // ==========================================
    // EVENT LISTENERS
    // ==========================================

    // Event listener untuk semua checkbox device (both grid and list)
    document.querySelectorAll('.device-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            const deviceId = this.getAttribute('data-id');
            const deviceName = this.getAttribute('data-name');
            const card = this.closest('.device-item-card, .device-item-list');

            if (this.checked) {
                // Tambah device ke selection
                addDevice(deviceId, deviceName, card);
            } else {
                // Remove device dari selection
                removeDevice(deviceId, card);
            }

            // Update compare bar
            updateCompareBar();

            // Sync checkboxes between grid and list view
            syncCheckboxes(deviceId, this.checked);
        });
    });

    // Event listener untuk tombol compare
    if (compareButton) {
        compareButton.addEventListener('click', function () {
            if (selectedDevices.length === 2) {
                // Redirect ke halaman compare
                window.location.href = `/compare-page?id1=${selectedDevices[0].id}&id2=${selectedDevices[1].id}`;
            }
        });
    }

    // Event listener untuk tombol clear
    if (clearButton) {
        clearButton.addEventListener('click', function () {
            // Clear semua selection
            clearSelection();
        });
    }

    // ==========================================
    // AUTO-SUBMIT SAAT KATEGORI BERUBAH
    // ==========================================

    // Ambil elemen kategori dropdown
    const categorySelect = document.getElementById('category');

    // Kalau ada kategori dropdown
    if (categorySelect) {
        // Event listener saat kategori berubah
        categorySelect.addEventListener('change', function () {
            // Ambil form
            const form = this.closest('form');

            // Submit form otomatis
            if (form) {
                form.submit();
            }
        });
    }

    // ==========================================
    // FUNCTIONS
    // ==========================================

    /**
     * Function untuk sync checkboxes antara grid dan list view
     */
    function syncCheckboxes(deviceId, checked) {
        document.querySelectorAll(`.device-checkbox[data-id="${deviceId}"]`).forEach(cb => {
            cb.checked = checked;
        });
    }

    /**
     * Function untuk tambah device ke selection
     */
    function addDevice(id, name, card) {
        // Cek apakah sudah ada 2 device
        if (selectedDevices.length >= 2) {
            // Uncheck checkbox yang baru diklik
            const checkboxes = document.querySelectorAll(`.device-checkbox[data-id="${id}"]`);
            checkboxes.forEach(cb => cb.checked = false);

            // Tampilkan pesan ke user
            alert('Maksimal 2 device untuk dibandingkan!');
            return;
        }

        // Tambah device ke array
        selectedDevices.push({ id, name });

        // Tambah class 'selected' ke semua card dengan ID yang sama
        document.querySelectorAll(`.device-checkbox[data-id="${id}"]`).forEach(cb => {
            const parentCard = cb.closest('.device-item-card, .device-item-list');
            if (parentCard) {
                parentCard.classList.add('selected');
            }
        });

        console.log('Device ditambahkan:', name);
    }

    /**
     * Function untuk remove device dari selection
     */
    function removeDevice(id, card) {
        // Filter out device yang di-remove
        selectedDevices = selectedDevices.filter(device => device.id !== id);

        // Remove class 'selected' dari semua card dengan ID yang sama
        document.querySelectorAll(`.device-checkbox[data-id="${id}"]`).forEach(cb => {
            const parentCard = cb.closest('.device-item-card, .device-item-list');
            if (parentCard) {
                parentCard.classList.remove('selected');
            }
        });

        console.log('Device dihapus, sisa:', selectedDevices.length);
    }

    /**
     * Function untuk update tampilan compare bar
     */
    function updateCompareBar() {
        // Kalau ada device yang dipilih, show compare bar
        if (selectedDevices.length > 0) {
            compareBar.classList.add('active');

            // Update list device yang dipilih
            selectedDevicesContainer.innerHTML = selectedDevices.map(device => `
                <span class="selected-device-tag">✓ ${device.name}</span>
            `).join('');

            // Enable/disable tombol compare
            if (selectedDevices.length === 2) {
                compareButton.disabled = false;
            } else {
                compareButton.disabled = true;
            }
        } else {
            // Hide compare bar kalau tidak ada device yang dipilih
            compareBar.classList.remove('active');
        }
    }

    /**
     * Function untuk clear semua selection
     */
    function clearSelection() {
        // Uncheck semua checkbox
        document.querySelectorAll('.device-checkbox').forEach(checkbox => {
            checkbox.checked = false;

            // Remove selected class dari card
            const card = checkbox.closest('.device-item-card, .device-item-list');
            if (card) {
                card.classList.remove('selected');
            }
        });

        // Clear array
        selectedDevices = [];

        // Update compare bar
        updateCompareBar();

        console.log('Selection cleared');
    }

    // ==========================================
    // FADE-IN ANIMATION
    // ==========================================

    // Add fade-in animation ke device cards saat page load
    addFadeInAnimation('.device-item-card');
    addFadeInAnimation('.device-item-list');

});
