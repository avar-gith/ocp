document.addEventListener("DOMContentLoaded", function () {
    const emailListDiv = document.getElementById('email-list');
    const emailApiUrl = "/api/office/emails/";  // Levelek lekérésének URL-je
    let previousEmails = [];  // Az előző letöltéskor tárolt levelek

    // Függvény a levelek lekérdezéséhez
    async function fetchEmails() {
        try {
            const response = await fetch(emailApiUrl);
            if (!response.ok) {
                throw new Error("Nem sikerült lekérdezni a leveleket.");
            }

            const emails = await response.json();
            return emails;
        } catch (error) {
            console.error("Hiba történt a levelek lekérése során:", error);
            return [];
        }
    }

    // Függvény a levelek megjelenítéséhez ID sorrendben
    function displayEmails(emails) {
        // E-maileket ID alapján sorbarendezzük csökkenő sorrendben
        emails.sort((a, b) => b.id - a.id);

        // Megjelenítjük az e-maileket
        emails.forEach(email => {
            const emailCard = `
                <div class="mail-card">
                    <div class="mail-header">
                        <span class="mail-sender">${email.sender.name}</span>
                        <span class="mail-date">${new Date(email.sent_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span> <!-- Csak az óra:perc -->
                    </div>
                    <div class="mail-subject">
                        <span class="subject-text">${email.subject}</span>
                    </div>
                    <div class="mail-content">
                        <p>${email.content}</p>
                    </div>
                </div>
            `;
            // Az új leveleket a lista tetejére illesztjük
            emailListDiv.insertAdjacentHTML('afterbegin', emailCard);
        });
    }

    // Első lekérés és megjelenítés
    fetchEmails().then(emails => {
        previousEmails = emails;  // Eltároljuk az előző leveleket
        displayEmails(emails);    // Megjelenítjük az első lekérés leveleit
    });

    // 2 másodpercenként új levelek ellenőrzése és hozzáadása a listához
    setInterval(async () => {
        const newEmails = await fetchEmails();  // Lekérjük az új leveleket

        // Új levelek szűrése (csak azok, amelyek nincsenek az előző listában)
        const freshEmails = newEmails.filter(email => 
            !previousEmails.some(prevEmail => prevEmail.id === email.id)
        );

        if (freshEmails.length > 0) {
            console.log("Új levelek érkeztek:", freshEmails);
            displayEmails(freshEmails);  // Megjelenítjük az új leveleket
            previousEmails = newEmails;  // Frissítjük az előző levelek listáját
        }
    }, 2000);  // 2 másodperc
});
