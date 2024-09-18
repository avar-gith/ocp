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

document.addEventListener("DOMContentLoaded", function () {
    const mainContentDiv = document.querySelector(".grid-main");
    const apiUrl = "/adan/service-call/";  // Az AI hívás URL-je
    const emailApiUrl = "/api/office/emails/";  // Levelek lekérésének URL-je
    let previousEmails = [];  // Korábban lekért levelek tárolása
    let isFirstFetch = true;  // Nyomon követi, hogy az első lekérés megtörtént-e

    // Függvény az AI hívásához
    async function fetchContent(promptData, extraData) {
        try {
            console.log("AI hívás indítása...");
            console.log("Prompt:", promptData);
            console.log("További adatok:", extraData);

            // Loader azonnali megjelenítése
            mainContentDiv.innerHTML = `
                <div class="oloader-container">
                    <div class="oloader"></div>
                </div>
            `;  // Egyszerű loader megjelenítése a mező közepén
            
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
        const withLineBreaks = text.replace(/\n/g, '<br>');
        const formattedText = withLineBreaks.replace(/\*\*(.*?)\*\*/g, '<span class="text-primary">$1</span>');
        return formattedText;
    }

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

    // AI elemzést végző függvény (aiHandler)
    async function aiHandler() {
        const emails = await fetchEmails();
        const newEmails = emails.filter(email => !previousEmails.some(prev => prev.id === email.id));

        if (!isFirstFetch && newEmails.length > 0) {
            const emailSummaries = newEmails.map(email => ({
                subject: email.subject,
                sender: email.sender.name,
                content: email.content
            }));

            // Szövegmező értékének lekérése
            const customTextarea = document.getElementById("custom-textarea");
            const customPrompt = customTextarea.value.trim();  // Beírt szöveg

            // Ellenőrizzük, hogy a szövegmező üres-e, ha igen, használjuk a placeholdert
            let prompt = "";
            if (customPrompt) {
                prompt = customPrompt;  // Ha van érték a szövegmezőben, azt használjuk
            } else {
                prompt = customTextarea.placeholder;  // Ha üres, akkor a placeholder értéket küldjük
            }

            // További logika az API-híváshoz (prompt használatával)
            fetchContent(prompt, emailSummaries);
        }

        previousEmails = emails;  // Frissítjük az előző leveleket
        isFirstFetch = false;  // Az első lekérés után átállítjuk
    }

    // 20 másodpercenként ellenőrzi a leveleket és elemzi az új leveleket
    setInterval(() => {
        console.log("...");
        aiHandler();
    }, 10000);  // 20 másodperc
});
