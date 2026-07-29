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
 * Resets all advanced custom dashboard selection values.
 * Restores desktop pill defaults, mobile dropdown indices, and toggles off adult switches instantly.
 * @param {HTMLFormElement} formElement - The active filter form reference.
 */
function clearAllFilters(formElement) {
    if (!formElement) return;

    // Reset standard textual selectors (Mobile View drop-downs)
    const selectElements = formElement.querySelectorAll('.filter-select');
    selectElements.forEach(select => {
        select.selectedIndex = 0; // Forces to "All/Any" option element index
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

    const watchTypeRadios = document.querySelectorAll(
        'input[name="type"]'
    );


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


    // Initial Render
    renderDesktopGenres(movieGenres);
    renderMobileGenres(movieGenres);


    // -----------------------------
    // Change Watch Type
    // -----------------------------
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

});
