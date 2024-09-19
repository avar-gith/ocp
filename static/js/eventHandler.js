// A részletek megjelenítése univerzálisan bármely típushoz (projektek, történetek, feladatok)
export const showDetails = (data, type, employees) => {
    const detailsContainer = document.getElementById('details-content');
    detailsContainer.innerHTML = ""; // Tisztítjuk a tartalmat

    // Ellenőrizd, hogy az employees tömb nem undefined, mielőtt a find-et meghívod
    const responsibleEmployee = employees && employees.find(emp => emp.id === data.responsible);
    const responsibleName = responsibleEmployee ? responsibleEmployee.name : 'Ismeretlen';

    const creatorEmployee = employees && employees.find(emp => emp.id === data.creator);
    const creatorName = creatorEmployee ? creatorEmployee.name : 'Ismeretlen';

    let detailsHTML = `
        <h3>${type === 'project' ? 'Projekt Név' : type === 'story' ? 'Történet Név' : 'Feladat Név'}: ${data.name}</h3>
        <p><strong>Leírás:</strong> ${data.description}</p>
        <p><strong>Státusz:</strong> ${data.status_display}</p> <!-- Frissítve a magyar státusz -->
        <p><strong>Határidő:</strong> ${data.deadline ? data.deadline : 'Nincs megadva'}</p>
    `;

    if (type === 'project') {
        detailsHTML += `<p><strong>Felelős:</strong> <span style="color: #007bff;">${responsibleName}</span></p>`;
    }

    if (type === 'story' || type === 'task') {
        detailsHTML += `<p><strong>Igénylő:</strong> <span class="text-muted">${creatorName}</span></p>`;
    }

    detailsContainer.innerHTML = detailsHTML;
};

// Kattintás esemény kezelése kártyákra (projektek, történetek, feladatok)
export const attachCardClickEvent = (projects, stories, tasks, employees) => {
    const projectCards = document.querySelectorAll('.project-card');
    const storyCards = document.querySelectorAll('.story-card');
    const taskCards = document.querySelectorAll('.task-card');

    // Ellenőrzés: biztosítsuk, hogy a projektek, történetek és feladatok adatai megfelelően lettek betöltve.
    if (!projects || !stories || !tasks) {
        console.warn("Az adatok nincsenek megfelelően betöltve.");
        return;
    }

    projectCards.forEach(card => {
        card.addEventListener('click', function() {
            const projectId = this.getAttribute('data-id');
            if (projectId) {
                const projectData = projects.find(project => project.id === parseInt(projectId));
                if (projectData) {
                    showDetails(projectData, 'project', employees);
                } else {
                    console.warn(`Nem található projekt az ID-vel: ${projectId}`);
                }
            }
        });
    });

    storyCards.forEach(card => {
        card.addEventListener('click', function() {
            const storyId = this.getAttribute('data-id');
            if (storyId) {
                const storyData = stories.find(story => story.id === parseInt(storyId));
                if (storyData) {
                    showDetails(storyData, 'story', employees);
                } else {
                    console.warn(`Nem található történet az ID-vel: ${storyId}`);
                }
            }
        });
    });

    taskCards.forEach(card => {
        card.addEventListener('click', function() {
            const taskId = this.getAttribute('data-id');
            if (taskId) {
                const taskData = tasks.find(task => task.id === parseInt(taskId));
                if (taskData) {
                    showDetails(taskData, 'task', employees);
                } else {
                    console.warn(`Nem található feladat az ID-vel: ${taskId}`);
                }
            }
        });
    });
};
