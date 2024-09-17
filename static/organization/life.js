// file: organization/static/organization/life.js

let isLifeServiceActive = false; // Szolgáltatás állapota
const lastEvent = new Date(); // Az aktuális dátum
lastEvent.setHours(22, 0, 0, 0); // Beállítjuk 22:00 órára
let interval; // Az időzítő referencia

function toggleButton() {
    const button = document.getElementById('toggle-button');
    isLifeServiceActive = !isLifeServiceActive; // Állapot megfordítása

    if (isLifeServiceActive) {
        button.classList.remove('btn-warning');
        button.classList.add('btn-success');
        updateSidebar('Az Élet szolgáltatás BE kapcsolva.'); // Üzenet a sidebarra
        startImitatingTime(); // Indítsd el az idő imitálását
    } else {
        button.classList.remove('btn-success');
        button.classList.add('btn-warning');
        updateSidebar('Az Élet szolgáltatás KI kapcsolva.'); // Üzenet a sidebarra
        stopImitatingTime(); // Állítsd le az idő imitálását
    }
}

function startImitatingTime() {
    updateSidebar(`Utolsó esemény időpontja: ${lastEvent.toLocaleString()}`); // Kiírjuk a kezdő időpontot

    interval = setInterval(() => {
        lastEvent.setHours(lastEvent.getHours() + 1); // Növeljük az órát
        updateSidebar(`Utolsó esemény időpontja: ${lastEvent.toLocaleString()}`); // Frissítjük a sidebaron
        createWorkEvent(); // Esemény generálása
    }, 1000); // Tick időzítő (1 másodperc)
}

function stopImitatingTime() {
    clearInterval(interval); // Időzítő leállítása
}

function updateSidebar(message) {
    const sidebar = document.getElementById('email-list'); // A sidebar elem
    const newMessage = document.createElement('div'); // Új üzenet létrehozása
    newMessage.textContent = message; // Üzenet beállítása
    sidebar.appendChild(newMessage); // Hozzáadjuk az üzenetet a sidebarhoz
}
