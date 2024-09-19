document.addEventListener("DOMContentLoaded", function () {
    const mainContentDiv = document.querySelector(".grid-main");
    const emailListDiv = document.getElementById('email-list');
    const apiUrl = "/adan/service-call/";  // Az AI hívás URL-je
    const emailApiUrl = "/api/office/emails/";  // Levelek lekérésének URL-je
    let previousEmails = [];  // Korábban lekért levelek tárolása
    let isFirstFetch = true;  // Változó az első lekérés követésére

    // Függvény az AI hívásához
    async function fetchContent(promptData, extraData) {
        try {
            console.log("AI hívás indítása...");
            console.log("Prompt:", promptData);
            console.log("További adatok:", extraData);

            // Loader azonnali megjelenítése
            mainContentDiv.innerHTML = `<div class="loader-container"><div class="loader"></div></div>`;  // Egyszerű loader megjelenítése

            // Timeout hozzáadása, hogy biztos legyen, hogy a loader megjelenik
            await new Promise(resolve => setTimeout(resolve, 100)); // Kis szünetet tart, hogy a loader renderelődjön

            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')  // A CSRF token lekérdezése
                },
                body: JSON.stringify({
                    prompt: promptData,
                    data: extraData
                })
            });

            if (!response.ok) {
                throw new Error("Hiba történt az AI API hívás során.");
            }

            const data = await response.json();
            console.log("AI válasz érkezett:", data);

            const responseText = formatResponseText(data.response);  // Formázott AI válasz
            mainContentDiv.innerHTML = `<p>${responseText}</p>`;  // Megjelenítés a felhasználónak
        } catch (error) {
            console.error("Hiba történt az AI hívás során:", error);
            mainContentDiv.innerHTML = "<p>Hiba történt a válasz lekérése során.</p>";
        }
    }



    // Formázza a választ a linebreak-ek és ** jelölések alapján
    function formatResponseText(text) {
        // Replace line breaks with <br> tags
        const withLineBreaks = text.replace(/\n/g, '<br>');
        
        // Regex to find words between ** and wrap them in a span with a class
        const formattedText = withLineBreaks.replace(/\*\*(.*?)\*\*/g, '<span class="text-primary">$1</span>');
        
        return formattedText;
    }


    // Függvény a levelek megjelenítéséhez
    function displayEmails(emails) {
        // console.log("Levelek megjelenítése:", emails);
        // emailListDiv.innerHTML = '';  // Előző tartalom törlése

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
            emailListDiv.innerHTML += emailCard;  // Új kártyák hozzáadása
        });
    }

    // Függvény a levelek lekérdezéséhez
    async function fetchEmails() {
        try {
            // console.log("Levelek lekérdezése...");
            const response = await fetch(emailApiUrl);
            if (!response.ok) {
                throw new Error("Nem sikerült lekérdezni a leveleket.");
            }

            const emails = await response.json();
            // console.log("Lekérdezett levelek:", emails);
            return emails;
        } catch (error) {
            console.error("Hiba történt a levelek lekérése során:", error);
            return [];
        }
    }

    // Ellenőrzi az új leveleket, és ha talál, elküldi az AI-nek
    async function checkForNewEmails() {
        // console.log("Új levelek ellenőrzése...");
        const emails = await fetchEmails();
        
        // Log az összes korábban lekérdezett levélről
        // console.log("Előző levelek:", previousEmails);

        // Ellenőrzés új levelekre a korábban lekérdezett emailek alapján
        const newEmails = emails.filter(email => !previousEmails.some(prev => prev.id === email.id));
        
        // Logoljuk az új levelek halmazát
        // console.log("Új levelek (új azonosítók):", newEmails);

        if (!isFirstFetch && newEmails.length > 0) {
            // console.log("Új levelek találhatók:", newEmails);

            const emailSummaries = newEmails.map(email => ({
                subject: email.subject,
                sender: email.sender.name,
                snippet: email.snippet
            }));

            const prompt = "Kérlek röviden foglald össze a történteket a levelek alapján.";
            console.log("AI-nek elküldött adatok:", emailSummaries);
            fetchContent(prompt, emailSummaries);  // Az új levelek továbbküldése az AI-nek
        } else if (isFirstFetch) {
            console.log("Első lekérés, nincs AI hívás.");
        }

        previousEmails = emails;  // Frissítjük az előző leveleket
        isFirstFetch = false;  // Az első lekérés után átállítjuk
        return newEmails;
    }

    // Kiegészítő függvény a CSRF token lekérdezéséhez
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Az oldal betöltésekor azonnal lekérdezzük a leveleket, és megjelenítjük
    checkForNewEmails().then(newEmails => {
        if (newEmails.length > 0) {
            displayEmails(newEmails);  // E-mailek megjelenítése
        }
    });

    // 10 másodpercenként ellenőrizzük az új leveleket, és megjelenítjük azokat
    setInterval(() => {
        checkForNewEmails().then(newEmails => {
            if (newEmails.length > 0) {
                displayEmails(newEmails);  // Új e-mailek megjelenítése
            }
        });
    }, 10000);  // 10 másodperc
});
