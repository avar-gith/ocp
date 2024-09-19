import { fetchApiData } from './apiHandler.js'; // Helyes exportált függvény importálása
import { attachCardClickEvent } from './eventHandler.js'; // Események kezelése

// Kártyák megjelenítése és események hozzáadása
export const displayData = (projects, stories, tasks, employees) => {
    const projectContainer = document.querySelector('.project-cards');
    projectContainer.innerHTML = "";  // Tisztítjuk a tartalmat

    // Projektek megjelenítése
    projects.forEach(project => {
        const responsibleEmployee = employees.find(emp => emp.id === project.responsible);
        const responsibleName = responsibleEmployee ? responsibleEmployee.name : 'Ismeretlen';

        const projectCard = `
            <div class="card project-card" data-id="${project.id}">
                <div class="card-body">
                    <h5 class="card-title">${project.name}</h5>
                    <p>Felelős: <span style="color: #007bff;">${responsibleName}</span></p>
                    <p>Státusz: ${project.status_display}</p>
                    <p>Határidő: <strong>${project.deadline ? project.deadline : 'Nincs megadva'}</strong></p>
                    <p>Leírás: ${project.description}</p>
                </div>
            </div>
        `;
        projectContainer.insertAdjacentHTML('beforeend', projectCard);

        // Történetek és feladatok megjelenítése
        const projectStories = stories.filter(story => story.project === project.id);
        projectStories.forEach(story => {
            const storyResponsible = employees.find(emp => emp.id === story.responsible);
            const storyResponsibleName = storyResponsible ? storyResponsible.name : 'Ismeretlen';

            const storyCard = `
                <div class="card story-card" data-id="${story.id}">
                    <div class="card-body">
                        <h5 class="card-title">${story.name}</h5>
                        <p>Felelős: <span style="color: #007bff;">${storyResponsibleName}</span></p>
                        <p>Státusz: ${story.status_display}</p>
                        <p>Határidő: <strong>${story.deadline ? story.deadline : 'Nincs megadva'}</strong></p>
                        <p>Leírás: ${story.description}</p>
                    </div>
                </div>
            `;
            projectContainer.insertAdjacentHTML('beforeend', storyCard);

            // Feladatok megjelenítése a történeten belül
            const storyTasks = tasks.filter(task => task.story === story.id);
            storyTasks.forEach(task => {
                const taskResponsible = employees.find(emp => emp.id === task.responsible);
                const taskResponsibleName = taskResponsible ? taskResponsible.name : 'Ismeretlen';

                const taskCard = `
                    <div class="card task-card" data-id="${task.id}">
                        <div class="card-body">
                            <h5 class="card-title">${task.name}</h5>
                            <p>Felelős: <span style="color: #007bff;">${taskResponsibleName}</span></p>
                            <p>Státusz: ${task.status_display}</p>
                            <p>Határidő: <strong>${task.deadline ? task.deadline : 'Nincs megadva'}</strong></p>
                            <p>Leírás: ${task.description}</p>
                        </div>
                    </div>
                `;
                projectContainer.insertAdjacentHTML('beforeend', taskCard);
            });
        });
    });

    attachCardClickEvent(projects, stories, tasks, employees); // Események hozzáadása
};
