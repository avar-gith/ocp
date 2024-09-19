// file: static/js/uiHandler.js

// Funkció a loader elrejtéséhez
const hideElement = (element) => {
    if (element) {
        element.style.display = 'none';
    }
};

// Funkció a tartalom megjelenítéséhez és a gördítősáv visszaállításához
const showContentAndEnableScroll = (contentElement, containerElement) => {
    if (contentElement) {
        contentElement.style.display = 'block';
    }
    if (containerElement) {
        containerElement.style.overflowY = 'scroll'; // Gördítősáv visszaadása
    }
};

// Loaderek elrejtése és a gördítősáv visszaadása a betöltés után
export const hideLoaders = () => {
    const leftLoader = document.querySelector('.jira_box_left .oloader-container');
    const rightLoader = document.querySelector('.jira_box_right .oloader-container');
    
    // Loaderek elrejtése
    hideElement(leftLoader);
    hideElement(rightLoader);

    // Tartalom megjelenítése és gördítősáv visszaadása
    const leftContent = document.querySelector('.jira_box_left .details-content');
    const rightContent = document.querySelector('.jira_box_right .projects-content');
    const leftBox = document.querySelector('.jira_box_left');
    const rightBox = document.querySelector('.jira_box_right');

    showContentAndEnableScroll(leftContent, leftBox);
    showContentAndEnableScroll(rightContent, rightBox);
};

