// file: static/js/jira.js

import { fetchApiData } from './apiHandler.js';
import { hideLoaders } from './uiHandler.js';

// Oldal betöltése után elindítjuk az API hívásokat
window.addEventListener('load', fetchApiData);
