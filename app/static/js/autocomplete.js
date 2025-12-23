// Autocomplete Search Component
// File ini handle autocomplete functionality untuk search bars

class AutocompleteSearch {
    constructor(inputElement, suggestionsElement) {
        this.input = inputElement;
        this.suggestions = suggestionsElement;
        this.selectedDevice = null;
        this.debounceTimer = null;

        // Bind event listeners
        this.init();
    }

    init() {
        // Event listener saat user ketik
        this.input.addEventListener('input', () => {
            const query = this.input.value.trim();

            // Kalau kurang dari 2 karakter, hide suggestions
            if (query.length < 2) {
                this.hideSuggestions();
                return;
            }

            // Debounce: tunggu 300ms sebelum fetch
            // Biar tidak terlalu banyak request ke server
            clearTimeout(this.debounceTimer);
            this.debounceTimer = setTimeout(() => {
                this.fetchSuggestions(query);
            }, 300);
        });

        // Event listener saat user klik di luar
        document.addEventListener('click', (e) => {
            if (!this.input.contains(e.target) && !this.suggestions.contains(e.target)) {
                this.hideSuggestions();
            }
        });
    }

    async fetchSuggestions(query) {
        try {
            // Fetch data dari API autocomplete
            const response = await fetch(`/devices/autocomplete?query=${encodeURIComponent(query)}`);
            const devices = await response.json();

            // Tampilkan suggestions
            this.showSuggestions(devices);
        } catch (error) {
            console.error('Error fetching suggestions:', error);
        }
    }

    showSuggestions(devices) {
        // Kalau tidak ada hasil, hide suggestions
        if (devices.length === 0) {
            this.hideSuggestions();
            return;
        }

        // Get query untuk highlighting
        const query = this.input.value.trim();

        // Buat HTML untuk suggestions dengan highlighted text
        this.suggestions.innerHTML = devices.map(device => {
            // Highlight matched text di nama dan brand
            const highlightedName = this.highlightMatch(device.name, query);
            const highlightedBrand = this.highlightMatch(device.brand, query);

            return `
                <div class="suggestion-item" data-id="${device.id}" data-name="${device.name}">
                    <strong>${highlightedName}</strong>
                    <span class="suggestion-brand">${highlightedBrand}</span>
                </div>
            `;
        }).join('');

        // Show suggestions dropdown
        this.suggestions.style.display = 'block';

        // IMPROVED: Use event delegation
        // Hanya 1 event listener di parent container, bukan di setiap item
        // Ini lebih efficient dan prevent memory leak
        this.suggestions.onclick = (e) => {
            // Cari parent element yang punya class suggestion-item
            const item = e.target.closest('.suggestion-item');
            if (!item) return;

            const deviceId = item.getAttribute('data-id');
            const deviceName = item.getAttribute('data-name');

            // Set input value ke device name
            this.input.value = deviceName;

            // Simpan selected device
            this.selectedDevice = { id: deviceId, name: deviceName };

            // Hide suggestions
            this.hideSuggestions();

            // Trigger custom event (biar bisa di-listen dari luar)
            this.input.dispatchEvent(new CustomEvent('deviceSelected', {
                detail: this.selectedDevice
            }));
        };
    }

    // Function untuk highlight matched text
    highlightMatch(text, query) {
        if (!query || !text) return text;

        // Escape special regex characters
        const escapedQuery = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

        // Create regex untuk case-insensitive match
        const regex = new RegExp(`(${escapedQuery})`, 'gi');

        // Replace matched text dengan <mark> tag
        return text.replace(regex, '<mark>$1</mark>');
    }

    hideSuggestions() {
        this.suggestions.style.display = 'none';
        this.suggestions.innerHTML = '';
    }

    getSelectedDevice() {
        return this.selectedDevice;
    }

    reset() {
        this.input.value = '';
        this.selectedDevice = null;
        this.hideSuggestions();
    }
}

// Export untuk dipakai di halaman lain
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AutocompleteSearch;
}
