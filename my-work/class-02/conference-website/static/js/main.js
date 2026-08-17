/**
 * Google Cloud Tech Summit 2026 - Client-side Interactive Search & Filter Logic
 */

document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search-input');
    const categorySelect = document.getElementById('category-select');
    const clearSearchBtn = document.getElementById('clear-search-btn');
    const resetFiltersBtn = document.getElementById('reset-filters-btn');
    const talksContainer = document.getElementById('talks-container');
    const visibleCountSpan = document.getElementById('visible-count');
    const noResultsDiv = document.getElementById('no-results');

    // Get all talk card elements (excluding lunch break card)
    const talkCards = Array.from(document.querySelectorAll('.talk-card'));

    /**
     * Filter talks based on current search query and selected category
     */
    function filterSchedule() {
        const query = searchInput.value.trim().toLowerCase();
        const selectedCategory = categorySelect.value;

        // Toggle clear search button visibility
        if (query.length > 0) {
            clearSearchBtn.hidden = false;
        } else {
            clearSearchBtn.hidden = true;
        }

        let visibleTalksCount = 0;

        talkCards.forEach(card => {
            const categoryId = card.getAttribute('data-category-id');
            const titleText = card.getAttribute('data-title') || '';
            const speakersText = card.getAttribute('data-speakers') || '';
            const cardContentText = card.innerText.toLowerCase();

            // 1. Category Matching
            const matchesCategory = (selectedCategory === 'all') || (categoryId === selectedCategory);

            // 2. Query Matching (Search in title, speaker names, description, etc.)
            const matchesQuery = query === '' || 
                titleText.includes(query) || 
                speakersText.includes(query) || 
                cardContentText.includes(query);

            if (matchesCategory && matchesQuery) {
                card.style.display = 'flex';
                visibleTalksCount++;
            } else {
                card.style.display = 'none';
            }
        });

        // Update count indicator
        visibleCountSpan.textContent = visibleTalksCount;

        // Handle empty state display
        if (visibleTalksCount === 0) {
            noResultsDiv.hidden = false;
            talksContainer.style.display = 'none';
        } else {
            noResultsDiv.hidden = true;
            talksContainer.style.display = 'flex';
        }
    }

    // Event Listeners
    if (searchInput) {
        searchInput.addEventListener('input', filterSchedule);
    }

    if (categorySelect) {
        categorySelect.addEventListener('change', filterSchedule);
    }

    if (clearSearchBtn) {
        clearSearchBtn.addEventListener('click', () => {
            searchInput.value = '';
            filterSchedule();
            searchInput.focus();
        });
    }

    if (resetFiltersBtn) {
        resetFiltersBtn.addEventListener('click', () => {
            searchInput.value = '';
            categorySelect.value = 'all';
            filterSchedule();
            searchInput.focus();
        });
    }
});
