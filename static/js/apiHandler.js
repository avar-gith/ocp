import { displayData } from './cardRenderer.js'; // Kártyák generálása
import { hideLoaders } from './uiHandler.js'; // Loaderek eltüntetése

// API-k meghívása és adatainak feldolgozása
export const fetchApiData = async () => {
    try {
        const [
            projectsResponse,
            storiesResponse,
            tasksResponse,
            employeesResponse,
            teamsResponse,
            emailsResponse,
            skillsResponse,
            positionsResponse,
            squadsResponse,
            companiesResponse,
            wikipagesResponse
        ] = await Promise.all([
            fetch("http://localhost:8000/api/jira/projects/"),
            fetch("http://localhost:8000/api/jira/stories/"),
            fetch("http://localhost:8000/api/jira/tasks/"),
            fetch("http://localhost:8000/api/organization/employees/"),
            fetch("http://localhost:8000/api/organization/teams/"),
            fetch("http://localhost:8000/api/office/emails/"),
            fetch("http://localhost:8000/api/organization/skills/"),
            fetch("http://localhost:8000/api/organization/positions/"),
            fetch("http://localhost:8000/api/organization/squads/"),
            fetch("http://localhost:8000/api/organization/companies/"),
            fetch("http://localhost:8000/api/office/wikipages/")
        ]);

        // Ellenőrizzük, hogy minden API válasz sikeres-e
        if (projectsResponse.ok && storiesResponse.ok && tasksResponse.ok && employeesResponse.ok) {
            const projects = await projectsResponse.json();
            const stories = await storiesResponse.json();
            const tasks = await tasksResponse.json();
            const employees = await employeesResponse.json();

            // Ellenőrizzük, hogy valóban van-e adat
            if (projects.length && stories.length && tasks.length && employees.length) {
                // Adatok megjelenítése
                displayData(projects, stories, tasks, employees);
                hideLoaders(); // Loaderek eltüntetése
            } else {
                console.warn("Az egyik vagy több adat üres: projects, stories, tasks, employees");
            }
        } else {
            console.error("Hiba történt az API hívások közben, nem érkezett megfelelő válasz.");
        }
    } catch (error) {
        console.error("Hiba történt az API hívások közben:", error);
    }
};

// Oldal betöltése után elindítjuk az API hívásokat
window.addEventListener('load', fetchApiData);
