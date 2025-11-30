// ============================================================================
// LOGS FUNCTIONALITY
// ============================================================================

let logsRefreshInterval = null;
let currentLogFilter = 'all';
let allLogs = [];

async function loadSystemLogs() {
    try {
        const lines = document.getElementById('logLinesSelect')?.value || 50;
        const response = await fetch('/api/logs/system?lines=' + lines);
        const data = await response.json();

        if (data.success) {
            allLogs = data.logs;
            displayLogs(allLogs);
            updateLogStats(allLogs.length);
        } else {
            console.error('Erro ao carregar logs:', data.error);
        }
    } catch (error) {
        console.error('Erro ao carregar logs:', error);
        const container = document.getElementById('logsContainer');
        if (container) {
            container.innerHTML = '<div class="log-entry log-error"><span class="log-message">Erro ao carregar logs: ' + error.message + '</span></div>';
        }
    }
}

function displayLogs(logs) {
    const container = document.getElementById('logsContainer');
    if (!container) return;

    // Filtra logs se necessário
    let filteredLogs = logs;
    if (currentLogFilter !== 'all') {
        filteredLogs = logs.filter(function(log) {
            return log.type === currentLogFilter;
        });
    }

    if (filteredLogs.length === 0) {
        container.innerHTML = '<div class="log-entry log-info"><span class="log-message">Nenhum log encontrado</span></div>';
        return;
    }

    let html = '';
    for (let i = 0; i < filteredLogs.length; i++) {
        const log = filteredLogs[i];
        const logType = log.type || 'info';
        const timestamp = log.timestamp ? '<span class="log-timestamp">' + log.timestamp + '</span>' : '';
        const message = escapeHtml(log.message);
        html += '<div class="log-entry log-' + logType + '">' + timestamp + '<span class="log-message">' + message + '</span></div>';
    }

    container.innerHTML = html;

    // Scroll para o final
    container.scrollTop = container.scrollHeight;
}

function filterLogs(filter) {
    currentLogFilter = filter;

    // Atualiza botões
    const buttons = document.querySelectorAll('.log-filter-btn');
    for (let i = 0; i < buttons.length; i++) {
        const btn = buttons[i];
        btn.classList.remove('active');
        if (btn.dataset.filter === filter) {
            btn.classList.add('active');
        }
    }

    displayLogs(allLogs);
}

function updateLogStats(count) {
    const statsEl = document.getElementById('logStats');
    const lastUpdateEl = document.getElementById('lastUpdate');

    if (statsEl) {
        statsEl.textContent = count + ' entradas';
    }

    if (lastUpdateEl) {
        const now = new Date();
        lastUpdateEl.textContent = 'Última atualização: ' + now.toLocaleTimeString();
    }
}

async function clearLogs() {
    try {
        const response = await fetch('/api/logs/clear', { method: 'POST' });
        const data = await response.json();

        if (data.success) {
            allLogs = [];
            displayLogs([]);
            updateLogStats(0);
        }
    } catch (error) {
        console.error('Erro ao limpar logs:', error);
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function startLogsAutoRefresh() {
    if (logsRefreshInterval) {
        clearInterval(logsRefreshInterval);
    }

    const autoRefresh = document.getElementById('autoRefreshLogs');
    if (autoRefresh && autoRefresh.checked) {
        logsRefreshInterval = setInterval(loadSystemLogs, 5000); // Atualiza a cada 5 segundos
    }
}

function stopLogsAutoRefresh() {
    if (logsRefreshInterval) {
        clearInterval(logsRefreshInterval);
        logsRefreshInterval = null;
    }
}

// Event listeners para logs
document.addEventListener('DOMContentLoaded', function() {
    const autoRefreshCheckbox = document.getElementById('autoRefreshLogs');
    if (autoRefreshCheckbox) {
        autoRefreshCheckbox.addEventListener('change', function(e) {
            if (e.target.checked) {
                startLogsAutoRefresh();
            } else {
                stopLogsAutoRefresh();
            }
        });
    }

    const logLinesSelect = document.getElementById('logLinesSelect');
    if (logLinesSelect) {
        logLinesSelect.addEventListener('change', loadSystemLogs);
    }

    // Carrega logs quando a aba é ativada
    const logsTabBtn = document.querySelector('[data-tab="logs"]');
    if (logsTabBtn) {
        logsTabBtn.addEventListener('click', function() {
            loadSystemLogs();
            startLogsAutoRefresh();
        });
    }

    // Para auto-refresh quando sair da aba de logs
    const tabBtns = document.querySelectorAll('.tab-btn');
    for (let i = 0; i < tabBtns.length; i++) {
        tabBtns[i].addEventListener('click', function() {
            if (this.dataset.tab !== 'logs') {
                stopLogsAutoRefresh();
            }
        });
    }
});

// Expor funções globalmente
window.loadSystemLogs = loadSystemLogs;
window.filterLogs = filterLogs;
window.clearLogs = clearLogs;
