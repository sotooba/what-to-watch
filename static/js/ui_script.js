/**
 * Resets all advanced custom dashboard selection values.
 * Restores desktop pill defaults and mobile dropdown indices instantly.
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
    const defaultPills = formElement.querySelectorAll('input[type="radio"][value=""]');
    defaultPills.forEach(radio => {
        radio.checked = true;
    });
}
