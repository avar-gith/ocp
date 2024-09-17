// file: organization/static/organization/workEvent.js

const eventTypes = [
    'Projekt',
    'Sprint',
    'Történet',
    'Feladat',
    'Levél'
];

/**
 * WorkEvent generálása.
 */
// file: organization/static/organization/workEvent.js

function createWorkEvent() {
    const randomIndex = Math.floor(Math.random() * eventTypes.length); // Véletlenszerű index
    const eventType = eventTypes[randomIndex];
    const eventMessage = `${eventType} keletkezett: ${new Date().toLocaleString()}`;
    
    updateSidebar(eventMessage); // Kiírja a sidebarra az eseményt

    // Események generálása a backend API-n keresztül
    const csrfToken = document.getElementById('csrf_token').value; // CSRF token

    fetch('/office/generate-events/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken // CSRF token hozzáadása a kéréshez
        },
        body: JSON.stringify({}) // További adatok küldése, ha szükséges
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('Események sikeresen generálva.');
        } else {
            console.error('Hiba történt az események generálásakor:', data.message);
        }
    })
    .catch((error) => {
        console.error('Hiba:', error);
    });
}


/**
 * Frissíti a sidebar tartalmát.
 * @param {string} message - Az üzenet, amit a sidebar-ba kell írni.
 */
function updateSidebar(message) {
    const sidebar = document.getElementById('email-list'); // A sidebar elem
    const newMessage = document.createElement('div'); // Új üzenet létrehozása
    newMessage.textContent = message; // Üzenet beállítása
    sidebar.appendChild(newMessage); // Hozzáadjuk az üzenetet a sidebarhoz
}
