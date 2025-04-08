// getYear.js
function getCurrentYear() {
    const currentYear = new Date().getFullYear();
    return currentYear;
}

document.addEventListener("DOMContentLoaded", function() {
    // Set the year in the footer when the document is loaded
    document.getElementById('year').textContent = getCurrentYear();
});