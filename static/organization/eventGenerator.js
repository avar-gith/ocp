// file: organization/static/organization/eventGenerator.js

(function() {
    const eventTypes = [
        'Projekt',
        'Sprint',
        'Történet',
        'Feladat',
        'Levél'
    ];

    /**
     * Véletlenszerű esemény generálása.
     * @returns {string} Az esemény típusa.
     */
    function generateRandomEvent() {
        const randomIndex = Math.floor(Math.random() * eventTypes.length); // Véletlenszerű index
        const eventMessage = `${eventTypes[randomIndex]} keletkezett: ${new Date().toLocaleString()}`;
        
        updateSidebar(eventMessage); // Kiírja a sidebarra az eseményt
        return eventMessage; // Visszatér az esemény üzenetével
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

    // Exponáljuk a generateRandomEvent függvényt
    window.generateRandomEvent = generateRandomEvent;

})();
