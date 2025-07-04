let priceChart = null;
let searchResults = [];
let selectedGadgets = JSON.parse(localStorage.getItem('selectedGadgets')) || [];

// Function to initialize or update the price chart
function initializePriceChart(data) {
    const ctx = document.getElementById('priceChart').getContext('2d');
    if (priceChart) {
        priceChart.destroy(); // Destroy the existing chart
    }
    priceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Price History',
                data: data.prices,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Function to fetch price data (replace with your actual API call)
async function fetchPriceData(searchTerm) {
    const response = await fetch(`/api/price-history/?search=${searchTerm}`);
    const data = await response.json();
    return data;
}

// Function to handle search
async function handleSearch(searchTerm) {
    const searchResults = await fetchSearchResults(searchTerm);
    const priceData = await fetchPriceData(searchTerm);
    initializePriceChart(priceData);
}

// Function to redirect to the comparison page
function redirectToComparison() {
    console.log("Selected Gadgets:", selectedGadgets);
    if (selectedGadgets.length >= 2) {
        const gadgetIds = selectedGadgets.map(g => g.id).join(',');
        console.log("Redirecting to:", `/compare?gadgets=${gadgetIds}`);
        window.location.href = `/compare?gadgets=${gadgetIds}`;
    } else {
        alert("Please select at least 2 gadgets to compare.");
    }
}

// Function to handle gadget selection
function selectGadget(gadget) {
    selectedGadgets.push(gadget);
    localStorage.setItem('selectedGadgets', JSON.stringify(selectedGadgets));
}

// Function to display search results
function displaySearchResults() {
    const resultsContainer = document.getElementById('search-results');
    resultsContainer.innerHTML = searchResults.map(product => `
        <div class="gadget-card" data-gadget-id="${product.id}">
            <img src="${product.imageUrl}" alt="${product.name}">
            <h3>${product.name}</h3>
            <button onclick="addToCompare(${product.id}, '${product.imageUrl}')">
                ${selectedGadgets.some(g => g.id === product.id) ? 'Remove from Compare' : 'Add to Compare'}
            </button>
        </div>
    `).join('');
}

// Function to add or remove a product from the comparison bar
function addToCompare(gadgetId, imageUrl) {
    if (selectedGadgets.some(g => g.id === gadgetId)) {
        selectedGadgets = selectedGadgets.filter(g => g.id !== gadgetId);
    } else if (selectedGadgets.length < 4) {
        selectedGadgets.push({ id: gadgetId, imageUrl: imageUrl });
    } else {
        alert("Maximum 4 products allowed");
        return;
    }
    localStorage.setItem('selectedGadgets', JSON.stringify(selectedGadgets));
    updateComparisonBar();
    displaySearchResults();
}

// Function to update the comparison bar
function updateComparisonBar() {
    const comparisonBar = document.getElementById('selected-gadgets');
    comparisonBar.innerHTML = selectedGadgets.map(gadget => `
        <div class="gadget-thumbnail" data-id="${gadget.id}">
            <button onclick="removeFromCompare(${gadget.id})" class="remove-gadget">×</button>
            <img src="${gadget.imageUrl}" alt="Gadget ${gadget.id}">
        </div>
    `).join('');
    document.getElementById('comparison-bar').style.display = selectedGadgets.length > 0 ? 'flex' : 'none';
}

// Function to remove a product from the comparison bar
function removeFromCompare(gadgetId) {
    selectedGadgets = selectedGadgets.filter(g => g.id !== gadgetId);
    localStorage.setItem('selectedGadgets', JSON.stringify(selectedGadgets));
    updateComparisonBar();
    displaySearchResults();
}

// Initialize comparison bar and chart on page load
document.addEventListener('DOMContentLoaded', () => {
    selectedGadgets = JSON.parse(localStorage.getItem('selectedGadgets')) || [];
    updateComparisonBar();
    const initialData = {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        prices: [65, 59, 80, 81, 56, 55, 40]
    };
    initializePriceChart(initialData);
});




