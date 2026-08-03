/**
 * AFter typing in the search box
 * When enter key is pressed on the mobile devices
 * Hide the keyboard
 */
function handleMobileSearch(inputId = 'navSearchInput') {
    // Finds the relevant search input field element
    const searchInput = document.getElementById(inputId);
    if (searchInput) {
        // Strips focus away from the field, which tells the mobile OS to hide the keyboard
        searchInput.blur();
    }
}

/**
 * Mobile navbar overlays: search and navigation occupy the same visual layer
 * without expanding the header or moving the page content.
 */
document.addEventListener('DOMContentLoaded', () => {
    const searchToggle = document.getElementById('mobileSearchToggle');
    const searchPanel = document.getElementById('mobileSearchPanel');
    const searchInput = document.getElementById('mobileSearchInput');
    const navCollapse = document.getElementById('whatToWatchNav');

    if (!searchToggle || !searchPanel || !searchInput || !navCollapse) return;

    const closeSearch = () => {
        searchPanel.hidden = true;
        searchToggle.setAttribute('aria-expanded', 'false');
    };

    searchToggle.addEventListener('click', () => {
        const opening = searchPanel.hidden;

        if (opening && window.bootstrap) {
            window.bootstrap.Collapse.getOrCreateInstance(navCollapse, { toggle: false }).hide();
        }

        searchPanel.hidden = !opening;
        searchToggle.setAttribute('aria-expanded', String(opening));

        if (opening) {
            requestAnimationFrame(() => searchInput.focus());
        }
    });

    navCollapse.addEventListener('show.bs.collapse', closeSearch);
});

/**
 * Keep a responsive skeleton visible while a request that needs TMDB data is
 * being rendered by Flask. It is intentionally triggered before navigation,
 * so slow API responses never leave the visitor with a blank page.
 */
document.addEventListener('DOMContentLoaded', () => {
    const loadingOverlay = document.getElementById('pageLoadingOverlay');
    let navigationPending = false;

    if (!loadingOverlay) return;

    const showLoading = () => {
        loadingOverlay.hidden = false;
        document.body.setAttribute('aria-busy', 'true');
    };

    const beginLoadingNavigation = (navigate) => {
        if (navigationPending) return;

        navigationPending = true;
        showLoading();

        // Show the loading state briefly, but avoid keeping the user waiting longer than necessary.
        requestAnimationFrame(() => window.setTimeout(navigate, 50));
    };

    /**
     * Custom Filter Form
     */
    document.querySelectorAll('form[action="/recommendations"]').forEach((form) => {

        form.addEventListener('submit', (event) => {
            event.preventDefault();

            beginLoadingNavigation(() => form.submit());
        });

    });

    /**
     * Mood Pods
     */
    document.querySelectorAll('.mood-pod').forEach((moodPod) => {

        moodPod.addEventListener('click', (event) => {

            // Allow Ctrl+Click / Cmd+Click / Middle Click to behave normally.
            const modifiedClick =
                event.button !== 0 ||
                event.metaKey ||
                event.ctrlKey ||
                event.shiftKey ||
                event.altKey;

            if (modifiedClick) return;

            event.preventDefault();

            beginLoadingNavigation(() => {
                window.location.assign(moodPod.href);
            });

        });

    });

    /**
     * "Something Else" button
     */
    document.querySelectorAll('[data-loading-reload]').forEach((button) => {

        button.addEventListener('click', () => {

            beginLoadingNavigation(() => {
                window.location.reload();
            });

        });

    });

    /**
     * Browsers often restore pages from the Back/Forward Cache (bfcache)
     * instead of reloading them.
     *
     * Reset the loading overlay and internal navigation flag so the user
     * can immediately submit another search without refreshing the page.
     */
    window.addEventListener('pageshow', () => {

        navigationPending = false;

        loadingOverlay.hidden = true;

        document.body.removeAttribute('aria-busy');

    });

});


/**
 * Resets all advanced custom dashboard selection values.
 * Restores desktop pill defaults, mobile dropdown indices, and toggles off adult switches instantly.
 * @param {HTMLFormElement} formElement - The active filter form reference.
 */
function clearAllFilters(formElement) {
    if (!formElement) return;

    // Reset standard textual selectors (Mobile View drop-downs)
    const selectElements = formElement.querySelectorAll('.filter-select');
    selectElements.forEach(select => {
        select.selectedIndex = 0; // Forces to      "All/Any" option element index
    });

    // Locate and check the default radio buttons (Desktop View Pills)
    // This matches both value="" and value="all"
    const defaultPills = formElement.querySelectorAll('input[type="radio"][value=""], input[type="radio"][value="all"]');
    defaultPills.forEach(radio => {
        radio.checked = true;
    });

    // Turn off both Desktop and Mobile Adult Switch buttons explicitly
    const switches = formElement.querySelectorAll('input[type="checkbox"]');
    switches.forEach(checkbox => {
        checkbox.checked = false;
    });
}


/**
 * Keeps the form data clean by turning off hidden filter inputs.
 * 
 * Since the form has two sets of filters (one for desktop screens and one for mobile), 
 * the hidden set can still send empty values and break search results. 
 * This function checks the screen size and disables the hidden inputs so only 
 * the visible, active filters send data to the server.
 */

function updateResponsiveFilters() {
    // Find the desktop and mobile filter wrappers on the page
    const desktopContainer = document.getElementById("desktop-filters");
    const mobileContainer = document.getElementById("mobile-filters");

    if (!desktopContainer || !mobileContainer) return;

    // Grab all the interactive inputs (radios, dropdowns, etc.) inside both containers
    const desktopControls = desktopContainer.querySelectorAll("input, select, textarea");
    const mobileControls = mobileContainer.querySelectorAll("input, select, textarea");

    // Check if the current screen width is desktop-sized (992 pixels or wider)
    // Returns true if on desktop, or false if on a mobile/tablet screen
    const desktopView = window.matchMedia("(min-width: 992px)").matches;

    // If we are NOT on a desktop view, turn off (disable) the desktop elements
    desktopControls.forEach(control => control.disabled = !desktopView);

    // If we ARE on a desktop view, turn off (disable) the mobile elements
    mobileControls.forEach(control => control.disabled = desktopView);
}


// Calling the function
document.addEventListener("DOMContentLoaded", updateResponsiveFilters);
window.addEventListener("resize", updateResponsiveFilters);


// Dynamically load the genres based on the watch type selected
document.addEventListener("DOMContentLoaded", () => {

    const movieGenres = window.movieGenres;
    const tvGenres = window.tvGenres;

    const desktopContainer = document.getElementById("desktopGenreContainer");
    const mobileSelect = document.getElementById("mobileGenreSelect");

    // Watch type controls: desktop radios and mobile select
    const watchTypeRadios = document.querySelectorAll('input[name="type"]');
    const mobileTypeSelect = document.querySelector('#mobile-filters select[name="type"]');

    if (!Array.isArray(movieGenres) || !Array.isArray(tvGenres) || !desktopContainer || !mobileSelect) return;

    // -----------------------------
    // Desktop Genre Pills
    // -----------------------------
    function renderDesktopGenres(genres) {

        let html = `
            <label class="pill-checkbox-item">
                <input
                    type="radio"
                    name="genre"
                    value=""
                    checked>
                <span>All</span>
            </label>
        `;

        genres.forEach(genre => {

            html += `
                <label class="pill-checkbox-item">
                    <input
                        type="radio"
                        name="genre"
                        value="${genre.id}">
                    <span>${genre.name}</span>
                </label>
            `;

        });

        desktopContainer.innerHTML = html;
    }


    // -----------------------------
    // Mobile Dropdown
    // -----------------------------
    function renderMobileGenres(genres) {

        let html = `
            <option value="" selected>
                All
            </option>
        `;

        genres.forEach(genre => {

            html += `
                <option value="${genre.id}">
                    ${genre.name}
                </option>
            `;

        });

        mobileSelect.innerHTML = html;
    }


    // Initial Render: choose based on current selection (desktop checked radio or mobile select)
    const currentRadio = document.querySelector('input[name="type"]:checked');
    const currentMobileType = mobileTypeSelect ? mobileTypeSelect.value : null;
    const initialType = (currentRadio && currentRadio.value) || currentMobileType || 'movie';

    if (initialType === 'tv') {
        renderDesktopGenres(tvGenres);
        renderMobileGenres(tvGenres);
    } else {
        renderDesktopGenres(movieGenres);
        renderMobileGenres(movieGenres);
    }


    // -----------------------------
    // Change Watch Type
    // -----------------------------
    // Desktop radios
    watchTypeRadios.forEach(radio => {
        radio.addEventListener("change", function () {
            if (this.value === "movie") {
                renderDesktopGenres(movieGenres);
                renderMobileGenres(movieGenres);
            }
            else if (this.value === "tv") {
                renderDesktopGenres(tvGenres);
                renderMobileGenres(tvGenres);
            }
        });
    });

    // Mobile select (for small screens) — keep genres in sync when user changes type
    if (mobileTypeSelect) {
        mobileTypeSelect.addEventListener('change', function () {
            const val = this.value;
            if (val === 'tv') {
                renderDesktopGenres(tvGenres);
                renderMobileGenres(tvGenres);
            } else {
                renderDesktopGenres(movieGenres);
                renderMobileGenres(movieGenres);
            }

            // Also update the desktop radio selection so internal state matches
            const correspondingRadio = document.querySelector('input[name="type"][value="' + val + '"]');
            if (correspondingRadio) correspondingRadio.checked = true;
        });
    }

});

/**
 * Dynamic My Picks filter chips.
 */
document.addEventListener('DOMContentLoaded', () => {
    const clearButton = document.querySelector('.filter-clear');
    const toggleButton = document.querySelector('.filter-toggle');
    const tagButtons = Array.from(document.querySelectorAll('.filter-chip[data-tag]'));
    const cards = Array.from(document.querySelectorAll('.pick-card'));
    if (!tagButtons.length || !cards.length) return;

    const activeTags = new Set();
    const maxVisible = 4;
    const hiddenTags = tagButtons.slice(maxVisible);

    const setHiddenTags = (hidden) => {
        hiddenTags.forEach(button => {
            button.classList.toggle('filter-hidden', hidden);
            button.hidden = hidden;
        });
    };

    const resetToggle = () => {
        if (!toggleButton) return;
        setHiddenTags(true);
        toggleButton.dataset.expanded = 'false';
        toggleButton.textContent = 'See more';
    };

    const updateCards = () => {
        const shouldShowAll = activeTags.size === 0;
        cards.forEach(card => {
            const tags = card.dataset.tags ? card.dataset.tags.split('||') : [];
            const matches = shouldShowAll || tags.some(tag => activeTags.has(tag));
            card.closest('.col-12').style.display = matches ? 'block' : 'none';
        });
    };

    if (hiddenTags.length && toggleButton) {
        setHiddenTags(true);
        toggleButton.addEventListener('click', () => {
            const expanded = toggleButton.dataset.expanded === 'true';
            setHiddenTags(expanded);
            toggleButton.dataset.expanded = String(!expanded);
            toggleButton.textContent = expanded ? 'See more' : 'See less';
        });
    }

    if (clearButton) {
        clearButton.addEventListener('click', () => {
            activeTags.clear();
            tagButtons.forEach(button => {
                button.classList.remove('active');
                button.setAttribute('aria-pressed', 'false');
            });
            updateCards();
            resetToggle();
        });
    }

    tagButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tag = button.dataset.tag;
            if (!tag) return;

            if (activeTags.has(tag)) {
                activeTags.delete(tag);
                button.classList.remove('active');
                button.setAttribute('aria-pressed', 'false');
            } else {
                activeTags.add(tag);
                button.classList.add('active');
                button.setAttribute('aria-pressed', 'true');
            }

            updateCards();
        });
    });
});
