/**
 * BookSage-AI Modern JavaScript
 * Handles search autocomplete, recommendation buttons, and UI interactions
 */

// DOM Elements
const bookSearch = document.getElementById('book-search');
const searchResults = document.getElementById('search-results');
const searchBtn = document.getElementById('search-btn');
const recommendButtons = document.getElementById('recommend-buttons');

// Debounce function to limit API calls
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Search API call
async function searchBooks(query) {
    if (query.length < 2) {
        hideResults();
        return;
    }

    try {
        const response = await fetch(`/search_books?query=${encodeURIComponent(query)}`);
        const data = await response.json();

        if (data.length > 0) {
            displayResults(data);
        } else {
            hideResults();
        }
    } catch (error) {
        console.error('Search error:', error);
        hideResults();
    }
}

// Display search results
function displayResults(books) {
    searchResults.innerHTML = '';

    books.forEach(book => {
        const item = document.createElement('a');
        item.href = '#';
        item.className = 'search-result-item';
        item.innerHTML = `
            <img src="${book.image_url}" class="search-result-image" alt="${book.title}" onerror="this.src='https://via.placeholder.com/50x70?text=Book'">
            <div class="search-result-info">
                <h6>${book.title}</h6>
                <small>${book.author}</small>
            </div>
        `;

        item.addEventListener('click', (e) => {
            e.preventDefault();
            selectBook(book.title);
        });

        searchResults.appendChild(item);
    });

    searchResults.classList.add('show');
}

// Hide search results
function hideResults() {
    searchResults.classList.remove('show');
}

// Select a book from search results
function selectBook(title) {
    bookSearch.value = title;
    hideResults();
    updateHiddenFields(title);
    showRecommendButtons();
}

// Update hidden form fields with book title
function updateHiddenFields(title) {
    const hybridField = document.getElementById('hybrid-book-title');
    const collabField = document.getElementById('collab-book-title');
    const contentField = document.getElementById('content-book-title');

    if (hybridField) hybridField.value = title;
    if (collabField) collabField.value = title;
    if (contentField) contentField.value = title;
}

// Show recommendation buttons with animation
function showRecommendButtons() {
    const searchTerm = bookSearch.value.trim();

    if (searchTerm.length > 0) {
        updateHiddenFields(searchTerm);
        recommendButtons.classList.add('show');
    } else {
        // Shake animation for empty search
        bookSearch.classList.add('shake');
        setTimeout(() => {
            bookSearch.classList.remove('shake');
        }, 500);
    }
}

// Debounced search handler
const debouncedSearch = debounce((query) => searchBooks(query), 300);

// Event Listeners
if (bookSearch) {
    // Input event for search
    bookSearch.addEventListener('input', (e) => {
        const query = e.target.value.trim();
        debouncedSearch(query);

        // Hide buttons if search is empty
        if (query.length === 0) {
            recommendButtons.classList.remove('show');
        }
    });

    // Focus event
    bookSearch.addEventListener('focus', () => {
        if (bookSearch.value.trim().length >= 2) {
            debouncedSearch(bookSearch.value.trim());
        }
    });

    // Enter key handler
    bookSearch.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            showRecommendButtons();
        }
    });
}

// Search button click
if (searchBtn) {
    searchBtn.addEventListener('click', () => {
        showRecommendButtons();
    });
}

// Click outside to close results
document.addEventListener('click', (e) => {
    if (!e.target.closest('.search-container')) {
        hideResults();
    }
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Check if there's a pre-filled search term
    const searchTerm = bookSearch ? bookSearch.value.trim() : '';

    if (searchTerm.length > 0) {
        updateHiddenFields(searchTerm);
        recommendButtons.classList.add('show');
    }

    // Add animation delays to book cards
    const bookCards = document.querySelectorAll('.book-card');
    bookCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.05}s`;
    });

    // Add animation delays to method cards
    const methodCards = document.querySelectorAll('.method-card');
    methodCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
});

// Smooth scroll for internal links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add loading state to buttons on form submit
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function () {
        const btn = this.querySelector('button[type="submit"]');
        if (btn) {
            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
        }
    });
});