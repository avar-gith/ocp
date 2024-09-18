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
        console.log('Az Élet szolgáltatás BE kapcsolva.'); // Üzenet a konzolra
        startImitatingTime(); // Indítsd el az idő imitálását
    } else {
        button.classList.remove('btn-success');
        button.classList.add('btn-warning');
        console.log('Az Élet szolgáltatás KI kapcsolva.'); // Üzenet a konzolra
        stopImitatingTime(); // Állítsd le az idő imitálását
    }
}

function startImitatingTime() {
    // console.log(`Utolsó esemény időpontja: ${lastEvent.toLocaleString()}`); // Kiírjuk a kezdő időpontot a konzolra

    interval = setInterval(() => {
        lastEvent.setHours(lastEvent.getHours() + 1); // Növeljük az órát
        // console.log(`Frissített időpont: ${lastEvent.toLocaleString()}`); // Frissítjük a konzolon az időt
        createWorkEvent(); // Esemény generálása
    }, 2000); // Tick időzítő (1 másodperc)
}

function stopImitatingTime() {
    clearInterval(interval); // Időzítő leállítása
}
