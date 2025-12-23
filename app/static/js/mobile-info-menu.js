// Mobile Info Menu Toggle
document.addEventListener('DOMContentLoaded', function () {
    const mobileInfoBtn = document.getElementById('mobileInfoBtn');
    const mobileInfoDropdown = document.getElementById('mobileInfoDropdown');

    if (mobileInfoBtn && mobileInfoDropdown) {
        // Toggle dropdown on button click
        mobileInfoBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            mobileInfoDropdown.classList.toggle('active');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function (e) {
            if (!mobileInfoBtn.contains(e.target) && !mobileInfoDropdown.contains(e.target)) {
                mobileInfoDropdown.classList.remove('active');
            }
        });

        // Close dropdown when clicking on a link
        const dropdownLinks = mobileInfoDropdown.querySelectorAll('a');
        dropdownLinks.forEach(link => {
            link.addEventListener('click', function () {
                mobileInfoDropdown.classList.remove('active');
            });
        });
    }
});
