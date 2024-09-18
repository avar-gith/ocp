// Függvény a levelek megjelenítéséhez
function displayEmails(emails) {
    const emailListDiv = document.getElementById('email-list');
    emailListDiv.innerHTML = '';  // Előző tartalom törlése

    emails.forEach(email => {
        const emailCard = `
            <div class="email-card">
                <h4>${email.subject}</h4>
                <p><strong>Küldő:</strong> ${email.sender}</p>
                <p>${email.snippet}</p>
            </div>
        `;
        emailListDiv.innerHTML += emailCard;  // Új kártyák hozzáadása
    });
}

// Amikor az új e-mailek érkeznek, hívd meg ezt a függvényt
checkForNewEmails().then(newEmails => {
    if (newEmails.length > 0) {
        displayEmails(newEmails);  // E-mailek megjelenítése
    }
});
