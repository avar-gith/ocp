// file: static/js/cardHandler.js

export const generateProjectCard = (project, employees) => {
    const responsibleEmployee = employees.find(emp => emp.id === project.responsible);
    return `
        <div class="card text-white bg-primary mb-3" style="max-width: 18rem;">
            <div class="card-header">Projekt</div>
            <div class="card-body">
                <h5 class="card-title">Projekt Név: ${project.name}</h5>
                <p class="card-text">
                    <strong>Felelős:</strong> ${responsibleEmployee ? responsibleEmployee.name : 'Ismeretlen'}<br>
                    <strong>Státusz:</strong> ${project.status}<br>
                    <strong>Határidő:</strong> ${project.deadline}<br>
                    <strong>Leírás:</strong> ${project.description}
                </p>
            </div>
        </div>
    `;
};

export const generateStoryCard = (story, employees) => {
    const storyResponsible = employees.find(emp => emp.id === story.responsible);
    return `
        <div class="card text-white bg-success mb-3" style="max-width: 18rem;">
            <div class="card-header">Történet</div>
            <div class="card-body">
                <h5 class="card-title">Történet Név: ${story.name}</h5>
                <p class="card-text">
                    <strong>Felelős:</strong> ${storyResponsible ? storyResponsible.name : 'Ismeretlen'}<br>
                    <strong>Státusz:</strong> ${story.status}<br>
                    <strong>Határidő:</strong> ${story.deadline}<br>
                    <strong>Leírás:</strong> ${story.description}
                </p>
            </div>
        </div>
    `;
};

export const generateTaskCard = (task, employees) => {
    const taskResponsible = employees.find(emp => emp.id === task.responsible);
    return `
        <div class="card text-white bg-danger mb-3" style="max-width: 18rem;">
            <div class="card-header">Feladat</div>
            <div class="card-body">
                <h5 class="card-title">Feladat Név: ${task.name}</h5>
                <p class="card-text">
                    <strong>Felelős:</strong> ${taskResponsible ? taskResponsible.name : 'Ismeretlen'}<br>
                    <strong>Státusz:</strong> ${task.status}<br>
                    <strong>Határidő:</strong> ${task.deadline}
                </p>
            </div>
        </div>
    `;
};
