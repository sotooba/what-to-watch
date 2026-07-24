/**
 * Resets all advanced custom dashboard selection values.
 * Restores desktop pill defaults, mobile dropdown indices, and toggles off adult switches instantly.
 * @param {HTMLFormElement} formElement - The active filter form reference.
 */
function clearAllFilters(formElement) {
    if (!formElement) return;

    // 1. Reset standard textual selectors (Mobile View drop-downs)
    const selectElements = formElement.querySelectorAll('.filter-select');
    selectElements.forEach(select => {
        select.selectedIndex = 0; // Forces to "All/Any" option element index
    });

    // 2. Locate and check the default radio buttons (Desktop View Pills)
    // This matches both value="" and value="all"
    const defaultPills = formElement.querySelectorAll('input[type="radio"][value=""], input[type="radio"][value="all"]');
    defaultPills.forEach(radio => {
        radio.checked = true;
    });


    // 3. Turn off both Desktop and Mobile Adult Switch buttons explicitly
    const switches = formElement.querySelectorAll('input[type="checkbox"]');
    switches.forEach(checkbox => {
        checkbox.checked = false;
    });
}
