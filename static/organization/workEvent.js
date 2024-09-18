const eventTypes = [
    { type: 'Projekt', chance: 0.1 },  // 20% esély
    { type: 'Sprint', chance: 0.15 },   // 10% esély
    { type: 'Story', chance: 0.18 },   // 5% esély
    { type: 'Task', chance: 0.45 },     // 10% esély
];

// Hibakeresési mód manuális bekapcsolása (true, ha logolni szeretnéd)
const debugMode = true;

/**
 * WorkEvent generálása valószínűség alapján.
 */
function createWorkEvent() {
    const eventsToGenerate = [];

    // Minden eseménytípusra dobunk egy véletlenszámot, és az esély alapján döntünk
    eventTypes.forEach(event => {
        const randomChance = Math.random(); // 0 és 1 közötti véletlenszám
        
        // Ha hibakeresési mód bekapcsolva, logoljuk a véletlenszámokat
        if (debugMode) {
            console.log(`Véletlen szám a ${event.type} esetén: ${randomChance}, esély: ${event.chance}`);
        }

        if (randomChance <= event.chance) {
            const eventMessage = `${event.type} keletkezett: ${new Date().toLocaleString()}`;
            console.log(eventMessage);  // Kiírjuk a konzolra
            eventsToGenerate.push(event.type); // Hozzáadjuk az eseményt a generálandó listához
        }
    });

    // Ha van legalább egy esemény, amit generálni kell, akkor küldjük el az API-nak
    if (eventsToGenerate.length > 0) {
        const csrfToken = document.getElementById('csrf_token').value; // CSRF token

        fetch('/office/generate-events/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken // CSRF token hozzáadása a kéréshez
            },
            body: JSON.stringify({ events: eventsToGenerate }) // Generált események küldése
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Hálózati hiba történt, nem sikerült a kérés.');
            }
            return response.json();
        })
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
    } else {
        console.log('Nem generálódott új esemény.');
    }
}
