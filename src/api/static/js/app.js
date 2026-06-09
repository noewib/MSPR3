/* ============================================================
   EDF/RTE Predictor Dashboard — Application Logic
   ============================================================ */

(() => {
  'use strict';

  /* --------------------------------------------------------
     CONFIG
     -------------------------------------------------------- */
  const CONFIG = {
    healthInterval:  5000,   // 5s
    metricsInterval: 3000,   // 3s
    maxDataPoints:   30,
    chartAnimation:  400,
    tabs: ['api','monitoring','load-tests','ml-results','rgpd','cgv','opendata'],
    defaultTab: 'api',
    endpoints: [
      { method: 'GET',  path: '/health',              desc: 'Vérification de l\'état du serveur' },
      { method: 'POST', path: '/predict',              desc: 'Prédiction de consommation électrique' },
      { method: 'GET',  path: '/api/metrics-json',     desc: 'Métriques temps réel (JSON)' },
      { method: 'GET',  path: '/api/model-stats',      desc: 'Statistiques des modèles ML' },
      { method: 'POST', path: '/api/load-test',        desc: 'Lancer un test de charge' },
      { method: 'GET',  path: '/api/predictions-history', desc: 'Historique des prédictions' },
      { method: 'GET',  path: '/docs',                 desc: 'Documentation Swagger UI' },
    ]
  };

  /* --------------------------------------------------------
     STATE
     -------------------------------------------------------- */
  const state = {
    currentTab: null,
    healthTimer: null,
    metricsTimer: null,
    metricsHistory: { timestamps: [], requests: [], latency: [] },
    charts: {},
    loadTestRunning: false,
    loadTestHistory: [],
    serverOnline: false,
  };

  /* --------------------------------------------------------
     UTILS
     -------------------------------------------------------- */
  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

  async function apiFetch(path, opts = {}) {
    try {
      const res = await fetch(path, opts);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (e) {
      console.warn(`API error [${path}]:`, e);
      return null;
    }
  }

  function formatNumber(n, decimals = 0) {
    if (n == null || isNaN(n)) return '—';
    return Number(n).toLocaleString('fr-FR', {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    });
  }

  function formatMs(ms) {
    if (ms == null) return '—';
    if (ms < 1) return `${(ms * 1000).toFixed(0)} µs`;
    if (ms < 1000) return `${ms.toFixed(1)} ms`;
    return `${(ms / 1000).toFixed(2)} s`;
  }

  function timeLabel() {
    return new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  }

  /* --------------------------------------------------------
     NAVIGATION
     -------------------------------------------------------- */
  function initNavigation() {
    $$('.nav-item[data-tab]').forEach(item => {
      item.addEventListener('click', (e) => {
        e.preventDefault();
        switchTab(item.dataset.tab);
      });
    });

    // Handle back/forward
    window.addEventListener('hashchange', () => {
      const hash = window.location.hash.replace('#','') || CONFIG.defaultTab;
      if (CONFIG.tabs.includes(hash)) switchTab(hash, false);
    });

    // Initial tab
    const initial = window.location.hash.replace('#','');
    switchTab(CONFIG.tabs.includes(initial) ? initial : CONFIG.defaultTab, false);
  }

  function switchTab(tabName, pushState = true) {
    if (state.currentTab === tabName) return;
    state.currentTab = tabName;

    // Update URL
    if (pushState) window.location.hash = tabName;

    // Update nav items
    $$('.nav-item[data-tab]').forEach(item => {
      item.classList.toggle('active', item.dataset.tab === tabName);
    });

    // Show/hide content
    $$('.tab-content').forEach(section => {
      section.classList.toggle('active', section.id === `tab-content-${tabName}`);
    });

    // Update breadcrumb
    const names = {
      api: '🔌 API', monitoring: '📊 Monitoring', 'load-tests': '🚀 Tests de Charge',
      'ml-results': '🤖 Résultats ML', rgpd: '🔒 RGPD', cgv: '📋 CGV', opendata: '🌐 Open Data'
    };
    const bc = $('#breadcrumb-active');
    if (bc) bc.textContent = names[tabName] || tabName;

    // Tab-specific init
    onTabEnter(tabName);
  }

  function onTabEnter(tab) {
    switch (tab) {
      case 'api':        initAPITab();      break;
      case 'monitoring': initMonitoring();  break;
      case 'load-tests': initLoadTests();   break;
      case 'ml-results': initMLResults();   break;
      case 'rgpd':       loadLegalPage('rgpd');   break;
      case 'cgv':        loadLegalPage('cgv');     break;
      case 'opendata':   loadLegalPage('opendata');break;
    }
  }

  /* --------------------------------------------------------
     SIDEBAR MOBILE
     -------------------------------------------------------- */
  function initSidebar() {
    const toggle = $('#sidebar-toggle');
    const sidebar = $('#sidebar');
    const overlay = $('#sidebar-overlay');

    if (toggle) {
      toggle.addEventListener('click', () => {
        sidebar.classList.toggle('open');
        overlay.classList.toggle('active');
      });
    }
    if (overlay) {
      overlay.addEventListener('click', () => {
        sidebar.classList.remove('open');
        overlay.classList.remove('active');
      });
    }
  }

  /* --------------------------------------------------------
     HEALTH CHECK
     -------------------------------------------------------- */
  function startHealthCheck() {
    checkHealth();
    state.healthTimer = setInterval(checkHealth, CONFIG.healthInterval);
  }

  async function checkHealth() {
    const indicator = $('#server-status-indicator');
    const statusText = $('#server-status-text');
    const apiLabel = $('#api-status-label');
    if (!indicator) return;

    indicator.className = 'status-indicator loading';
    if (apiLabel) apiLabel.textContent = 'Vérification…';
    const data = await apiFetch('/health');

    if (data) {
      state.serverOnline = true;
      indicator.className = 'status-indicator';
      if (statusText) statusText.textContent = 'En ligne';
      if (apiLabel) {
        apiLabel.textContent = 'En ligne';
        apiLabel.className = 'stat-value text-success';
      }
    } else {
      state.serverOnline = false;
      indicator.className = 'status-indicator offline';
      if (statusText) statusText.textContent = 'Hors ligne';
      if (apiLabel) {
        apiLabel.textContent = 'Hors ligne';
        apiLabel.className = 'stat-value text-danger';
      }
    }
  }

  /* --------------------------------------------------------
     API TAB
     -------------------------------------------------------- */
  function initAPITab() {
    renderEndpoints();
    initPredictForm();
  }

  function renderEndpoints() {
    const container = $('#endpoints-list');
    if (!container || container.children.length > 0) return;

    CONFIG.endpoints.forEach(ep => {
      const el = document.createElement('div');
      el.className = 'endpoint-item';
      el.innerHTML = `
        <span class="method-badge method-${ep.method.toLowerCase()}">${ep.method}</span>
        <span class="endpoint-path">${ep.path}</span>
        <span class="endpoint-desc">${ep.desc}</span>
      `;
      container.appendChild(el);
    });
  }

  function initPredictForm() {
    const form = $('#predict-form');
    if (!form || form.dataset.init) return;
    form.dataset.init = 'true';

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const dateInput = $('#predict-date');
      const modelSelect = $('#predict-model');
      const btn = $('#predict-btn');
      const output = $('#predict-response');
      const date = dateInput?.value;
      const modelName = modelSelect?.value;
      if (!date) return;

      btn.classList.add('loading');
      btn.innerHTML = '<span class="spinner spinner-sm"></span> Envoi…';
      output.textContent = 'Chargement…';
      
      const payload = { date: date };
      if (modelName) payload.model_name = modelName;

      const data = await apiFetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      btn.classList.remove('loading');
      btn.innerHTML = '⚡ Prédire';
      output.textContent = data
        ? JSON.stringify(data, null, 2)
        : '❌ Erreur — Le serveur n\'a pas répondu.';
    });
  }

  /* --------------------------------------------------------
     MONITORING TAB
     -------------------------------------------------------- */
  function initMonitoring() {
    createMonitoringCharts();
    fetchMetrics();
    clearInterval(state.metricsTimer);
    state.metricsTimer = setInterval(fetchMetrics, CONFIG.metricsInterval);
  }

  function createMonitoringCharts() {
    // Requests over time
    if (!state.charts.requests) {
      const ctx = $('#metrics-chart-requests');
      if (ctx) {
        state.charts.requests = new Chart(ctx, {
          type: 'line',
          data: {
            labels: [],
            datasets: [{
              label: 'Requêtes totales',
              data: [],
              borderColor: '#6366f1',
              backgroundColor: 'rgba(99,102,241,0.10)',
              fill: true,
              tension: 0.4,
              borderWidth: 2,
              pointRadius: 0,
              pointHoverRadius: 5,
              pointHoverBackgroundColor: '#6366f1',
            }]
          },
          options: chartDefaults('Requêtes')
        });
      }
    }

    // Latency over time
    if (!state.charts.latency) {
      const ctx = $('#metrics-chart-latency');
      if (ctx) {
        state.charts.latency = new Chart(ctx, {
          type: 'line',
          data: {
            labels: [],
            datasets: [{
              label: 'Latence (ms)',
              data: [],
              borderColor: '#22d3ee',
              backgroundColor: 'rgba(34,211,238,0.10)',
              fill: true,
              tension: 0.4,
              borderWidth: 2,
              pointRadius: 0,
              pointHoverRadius: 5,
              pointHoverBackgroundColor: '#22d3ee',
            }]
          },
          options: chartDefaults('Latence (ms)')
        });
      }
    }

    // Consumption gauge
    if (!state.charts.gauge) {
      const ctx = $('#metrics-chart-gauge');
      if (ctx) {
        state.charts.gauge = new Chart(ctx, {
          type: 'doughnut',
          data: {
            labels: ['Consommation', 'Restant'],
            datasets: [{
              data: [0, 100],
              backgroundColor: [
                createGradientDoughnut(ctx, '#6366f1', '#22d3ee'),
                'rgba(30,30,60,0.5)'
              ],
              borderWidth: 0,
              circumference: 270,
              rotation: 225,
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: true,
            cutout: '78%',
            plugins: {
              legend: { display: false },
              tooltip: { enabled: false }
            },
            animation: { animateRotate: true, duration: CONFIG.chartAnimation }
          }
        });
      }
    }
  }

  function createGradientDoughnut(canvas, color1, color2) {
    try {
      const ctx = canvas.getContext('2d');
      const g = ctx.createLinearGradient(0, 0, canvas.width || 300, 0);
      g.addColorStop(0, color1);
      g.addColorStop(1, color2);
      return g;
    } catch {
      return color1;
    }
  }

  function chartDefaults(yTitle) {
    return {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: CONFIG.chartAnimation },
      interaction: { intersect: false, mode: 'index' },
      scales: {
        x: {
          grid: { color: 'rgba(99,102,241,0.06)', drawBorder: false },
          ticks: { color: '#64748b', font: { size: 10 }, maxRotation: 0, maxTicksLimit: 8 }
        },
        y: {
          grid: { color: 'rgba(99,102,241,0.06)', drawBorder: false },
          ticks: { color: '#64748b', font: { size: 10 } },
          title: { display: true, text: yTitle, color: '#94a3b8', font: { size: 11 } }
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(15,15,35,0.95)',
          titleColor: '#f1f5f9',
          bodyColor: '#94a3b8',
          borderColor: 'rgba(99,102,241,0.3)',
          borderWidth: 1,
          cornerRadius: 8,
          padding: 12,
          titleFont: { weight: '600' }
        }
      }
    };
  }

  async function fetchMetrics() {
    const data = await apiFetch('/api/metrics-json');
    if (!data) return;

    const now = timeLabel();
    const h = state.metricsHistory;
    h.timestamps.push(now);
    h.requests.push(data.summary?.total_requests ?? data.request_count ?? 0);
    h.latency.push(data.summary?.avg_latency_ms ?? data.inference_latency ?? 0);

    // Trim to maxDataPoints
    if (h.timestamps.length > CONFIG.maxDataPoints) {
      h.timestamps.shift();
      h.requests.shift();
      h.latency.shift();
    }

    // Update charts
    if (state.charts.requests) {
      state.charts.requests.data.labels = [...h.timestamps];
      state.charts.requests.data.datasets[0].data = [...h.requests];
      state.charts.requests.update('none');
    }

    if (state.charts.latency) {
      state.charts.latency.data.labels = [...h.timestamps];
      state.charts.latency.data.datasets[0].data = [...h.latency];
      state.charts.latency.update('none');
    }

    // Gauge
    const consumption = data.summary?.last_prediction ?? data.consumption ?? 0;
    if (state.charts.gauge) {
      const maxVal = 80000; // reasonable max MW for France
      const pct = Math.min((consumption / maxVal) * 100, 100);
      state.charts.gauge.data.datasets[0].data = [pct, 100 - pct];
      state.charts.gauge.update('none');
    }
    const gaugeVal = $('#gauge-value');
    if (gaugeVal) gaugeVal.textContent = formatNumber(consumption, 0) + ' MW';

    // Stat cards
    setText('#stat-total-requests', formatNumber(data.summary?.total_requests ?? data.request_count ?? 0));
    setText('#stat-avg-latency', formatMs(data.summary?.avg_latency_ms ?? data.inference_latency ?? 0));
    setText('#stat-last-prediction', formatNumber(consumption, 0) + ' MW');
    
    // Format uptime correctly (uptime_seconds returns a number of seconds)
    const uptimeStr = data.uptime_seconds 
      ? (data.uptime_seconds > 3600 
          ? (data.uptime_seconds/3600).toFixed(1) + ' h' 
          : (data.uptime_seconds > 60 ? (data.uptime_seconds/60).toFixed(1) + ' m' : data.uptime_seconds + ' s'))
      : '—';
    setText('#stat-uptime', uptimeStr);
  }

  function setText(sel, val) {
    const el = $(sel);
    if (el) el.textContent = val;
  }

  /* --------------------------------------------------------
     LOAD TESTS TAB
     -------------------------------------------------------- */
  function initLoadTests() {
    const form = $('#load-test-form');
    if (!form || form.dataset.init) return;
    form.dataset.init = 'true';

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (state.loadTestRunning) return;
      await runLoadTest();
    });
  }

  async function runLoadTest() {
    state.loadTestRunning = true;
    const btn = $('#load-test-btn');
    const progress = $('#load-test-progress');
    const progressFill = $('#load-test-progress-fill');
    const progressText = $('#load-test-progress-text');
    const resultsArea = $('#load-test-results');

    const users    = parseInt($('#lt-users')?.value) || 100;
    const duration = parseInt($('#lt-duration')?.value) || 30;
    const rampUp   = parseInt($('#lt-rampup')?.value) || 5;

    btn.classList.add('loading');
    btn.innerHTML = '<span class="spinner spinner-sm"></span> Test en cours…';
    progress?.classList.remove('hidden');
    if (resultsArea) resultsArea.classList.add('hidden');

    // Simulate progress
    let pct = 0;
    const progressInterval = setInterval(() => {
      pct = Math.min(pct + (100 / (duration * 2)), 95);
      if (progressFill) progressFill.style.width = pct + '%';
      if (progressText) progressText.textContent = Math.round(pct) + '%';
    }, 500);

    const data = await apiFetch('/api/load-test', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ concurrent_users: users, duration_seconds: duration, ramp_up: rampUp })
    });

    clearInterval(progressInterval);
    if (progressFill) progressFill.style.width = '100%';
    if (progressText) progressText.textContent = '100%';

    setTimeout(() => {
      btn.classList.remove('loading');
      btn.innerHTML = '🚀 Lancer le test';
      state.loadTestRunning = false;

      if (data) {
        displayLoadTestResults(data);
        state.loadTestHistory.unshift({ date: new Date().toLocaleString('fr-FR'), ...data });
        renderTestHistory();
      } else {
        if (resultsArea) {
          resultsArea.classList.remove('hidden');
          resultsArea.innerHTML = '<div class="loading-state"><p class="text-danger">❌ Le test a échoué</p></div>';
        }
      }
    }, 600);
  }

  function displayLoadTestResults(data) {
    const area = $('#load-test-results');
    if (!area) return;
    area.classList.remove('hidden');

    // Summary stats
    setText('#lt-stat-total',    formatNumber(data.total_requests ?? 0));
    setText('#lt-stat-avg-rt',   formatMs(data.avg_response_time ?? 0));
    setText('#lt-stat-p95',      formatMs(data.p95 ?? 0));
    setText('#lt-stat-p99',      formatMs(data.p99 ?? 0));
    setText('#lt-stat-error',    (data.error_rate ?? 0).toFixed(1) + '%');
    setText('#lt-stat-throughput', formatNumber(data.throughput ?? data.requests_per_second ?? 0, 1) + ' req/s');

    // Response time distribution chart
    createOrUpdateChart('lt-chart-distribution', {
      type: 'bar',
      data: {
        labels: data.response_distribution?.labels || ['<100ms','100-200ms','200-500ms','500ms-1s','>1s'],
        datasets: [{
          label: 'Nombre de requêtes',
          data: data.response_distribution?.values || generateSampleDistribution(data.total_requests ?? 500),
          backgroundColor: [
            'rgba(16,185,129,0.6)',
            'rgba(99,102,241,0.6)',
            'rgba(34,211,238,0.6)',
            'rgba(245,158,11,0.6)',
            'rgba(239,68,68,0.6)'
          ],
          borderRadius: 6,
          borderSkipped: false,
        }]
      },
      options: { ...chartDefaults('Requêtes'), plugins: { legend: { display: false } } }
    });

    // RPS over time chart
    createOrUpdateChart('lt-chart-rps', {
      type: 'line',
      data: {
        labels: data.rps_over_time?.labels || generateTimeLabels(10),
        datasets: [{
          label: 'Req/s',
          data: data.rps_over_time?.values || generateSampleRPS(10, data.throughput ?? 50),
          borderColor: '#6366f1',
          backgroundColor: 'rgba(99,102,241,0.10)',
          fill: true,
          tension: 0.4,
          borderWidth: 2,
          pointRadius: 3,
          pointBackgroundColor: '#6366f1',
        }]
      },
      options: chartDefaults('Requêtes/s')
    });

    // Error rate over time
    createOrUpdateChart('lt-chart-errors', {
      type: 'line',
      data: {
        labels: data.errors_over_time?.labels || generateTimeLabels(10),
        datasets: [{
          label: 'Taux d\'erreur (%)',
          data: data.errors_over_time?.values || generateSampleErrors(10, data.error_rate ?? 1),
          borderColor: '#ef4444',
          backgroundColor: 'rgba(239,68,68,0.10)',
          fill: true,
          tension: 0.3,
          borderWidth: 2,
          pointRadius: 3,
          pointBackgroundColor: '#ef4444',
        }]
      },
      options: chartDefaults('Erreurs (%)')
    });
  }

  function generateSampleDistribution(total) {
    const t = total || 500;
    return [
      Math.round(t * 0.45),
      Math.round(t * 0.28),
      Math.round(t * 0.15),
      Math.round(t * 0.08),
      Math.round(t * 0.04)
    ];
  }

  function generateTimeLabels(n) {
    return Array.from({ length: n }, (_, i) => `${i * 3}s`);
  }

  function generateSampleRPS(n, avg) {
    return Array.from({ length: n }, () =>
      Math.max(0, avg + (Math.random() - 0.5) * avg * 0.4)
    );
  }

  function generateSampleErrors(n, rate) {
    return Array.from({ length: n }, () =>
      Math.max(0, rate + (Math.random() - 0.5) * rate * 0.6)
    );
  }

  function createOrUpdateChart(canvasId, config) {
    const canvas = $(`#${canvasId}`);
    if (!canvas) return;

    if (state.charts[canvasId]) {
      state.charts[canvasId].destroy();
    }

    config.options = {
      ...config.options,
      responsive: true,
      maintainAspectRatio: false
    };

    state.charts[canvasId] = new Chart(canvas, config);
  }

  function renderTestHistory() {
    const container = $('#load-test-history');
    if (!container) return;

    if (state.loadTestHistory.length === 0) {
      container.innerHTML = '<p class="text-muted" style="padding:12px;">Aucun test précédent</p>';
      return;
    }

    let html = `
      <div class="table-container">
        <table class="data-table">
          <thead><tr>
            <th>Date</th><th>Requêtes</th><th>Moy. RT</th><th>P95</th><th>Erreurs</th><th>Débit</th>
          </tr></thead>
          <tbody>
    `;

    state.loadTestHistory.forEach(r => {
      html += `<tr>
        <td>${r.date}</td>
        <td>${formatNumber(r.total_requests ?? 0)}</td>
        <td>${formatMs(r.avg_response_time ?? 0)}</td>
        <td>${formatMs(r.p95 ?? 0)}</td>
        <td>${(r.error_rate ?? 0).toFixed(1)}%</td>
        <td>${formatNumber(r.throughput ?? r.requests_per_second ?? 0, 1)} req/s</td>
      </tr>`;
    });

    html += '</tbody></table></div>';
    container.innerHTML = html;
  }

  /* --------------------------------------------------------
     ML RESULTS TAB
     -------------------------------------------------------- */
  async function initMLResults() {
    const container = $('#ml-results-content');
    if (!container) return;

    // Show loading
    const loadingEl = $('#ml-loading');
    if (loadingEl) loadingEl.classList.remove('hidden');

    const [stats, history] = await Promise.all([
      apiFetch('/api/model-stats'),
      apiFetch('/api/predictions-history')
    ]);

    if (loadingEl) loadingEl.classList.add('hidden');

    if (stats) renderModelStats(stats);
    if (history) renderPredictionsChart(history);
  }

  function renderModelStats(stats) {
    const models = stats.models || stats;
    if (!Array.isArray(models) || models.length === 0) return;

    // Find champion
    const champion = models.reduce((best, m) =>
      (m.mape != null && (best == null || m.mape < best.mape)) ? m : best, null);

    // Model comparison table
    const tableContainer = $('#ml-model-table');
    if (tableContainer) {
      let html = `
        <div class="table-container">
          <table class="data-table">
            <thead><tr>
              <th>Modèle</th><th>R²</th><th>RMSE</th><th>MAPE</th><th>Précision ±5%</th><th>Temps d'entraînement</th><th>Statut</th>
            </tr></thead>
            <tbody>
      `;

      models.forEach(m => {
        const isChampion = champion && m.name === champion.name;
        html += `<tr class="${isChampion ? 'champion' : ''}">
          <td><strong>${m.name || '—'}</strong></td>
          <td>${m.r2 != null ? m.r2.toFixed(4) : '—'}</td>
          <td>${m.rmse != null ? formatNumber(m.rmse, 2) : '—'}</td>
          <td>${m.mape != null ? m.mape.toFixed(2) + '%' : '—'}</td>
          <td>${m.accuracy_5pct != null ? m.accuracy_5pct.toFixed(1) + '%' : '—'}</td>
          <td>${m.training_time ?? '—'}</td>
          <td>${isChampion ? '<span class="badge badge-champion">🏆 Champion</span>' : '<span class="badge badge-primary">Candidat</span>'}</td>
        </tr>`;
      });

      html += '</tbody></table></div>';
      tableContainer.innerHTML = html;
    }

    // MAPE comparison bar chart
    createOrUpdateChart('ml-chart-mape', {
      type: 'bar',
      data: {
        labels: models.map(m => m.name || 'Modèle'),
        datasets: [{
          label: 'MAPE (%)',
          data: models.map(m => m.mape ?? 0),
          backgroundColor: models.map(m =>
            (champion && m.name === champion.name)
              ? 'rgba(245,158,11,0.6)'
              : 'rgba(99,102,241,0.5)'
          ),
          borderRadius: 8,
          borderSkipped: false,
        }]
      },
      options: {
        ...chartDefaults('MAPE (%)'),
        indexAxis: 'y',
        plugins: { legend: { display: false } }
      }
    });

    // Training metadata
    const metaContainer = $('#ml-training-meta');
    if (metaContainer && stats.metadata) {
      const md = stats.metadata;
      metaContainer.innerHTML = `
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-label">Source des données</div>
            <div class="stat-value" style="font-size:16px;">${md.data_source ?? 'RTE / Open Data'}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Période</div>
            <div class="stat-value" style="font-size:16px;">${md.period ?? '—'}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Features utilisées</div>
            <div class="stat-value" style="font-size:16px;">${md.features_count ?? '—'}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Dernière MAJ</div>
            <div class="stat-value" style="font-size:16px;">${md.last_updated ?? '—'}</div>
          </div>
        </div>
      `;
    }
  }

  function renderPredictionsChart(history) {
    const records = history.predictions || history.data || history;
    if (!Array.isArray(records) || records.length === 0) return;

    createOrUpdateChart('ml-chart-predictions', {
      type: 'line',
      data: {
        labels: records.map(r => r.date || r.timestamp || ''),
        datasets: [
          {
            label: 'Valeur réelle',
            data: records.map(r => r.actual ?? r.real ?? null),
            borderColor: '#22d3ee',
            backgroundColor: 'rgba(34,211,238,0.08)',
            fill: false,
            tension: 0.3,
            borderWidth: 2,
            pointRadius: 2,
          },
          {
            label: 'Prédiction',
            data: records.map(r => r.predicted ?? r.prediction ?? null),
            borderColor: '#6366f1',
            backgroundColor: 'rgba(99,102,241,0.08)',
            fill: false,
            tension: 0.3,
            borderWidth: 2,
            borderDash: [5, 3],
            pointRadius: 2,
          }
        ]
      },
      options: {
        ...chartDefaults('MW'),
        plugins: {
          legend: {
            display: true,
            position: 'top',
            labels: { color: '#94a3b8', font: { size: 12 }, usePointStyle: true, pointStyle: 'line' }
          },
          tooltip: {
            backgroundColor: 'rgba(15,15,35,0.95)',
            titleColor: '#f1f5f9',
            bodyColor: '#94a3b8',
            borderColor: 'rgba(99,102,241,0.3)',
            borderWidth: 1,
            cornerRadius: 8,
            padding: 12,
          }
        }
      }
    });
  }

  /* --------------------------------------------------------
     LEGAL PAGES (RGPD / CGV / OPENDATA)
     -------------------------------------------------------- */
  async function loadLegalPage(page) {
    const container = $(`#${page}-content`);
    if (!container) return;

    // Don't reload if already loaded
    if (container.dataset.loaded === 'true') return;

    container.innerHTML = '<div class="loading-state"><div class="spinner"></div><p>Chargement…</p></div>';

    try {
      const res = await fetch(`/static/pages/${page}.html`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const html = await res.text();
      container.innerHTML = `<div class="legal-content">${html}</div>`;
      container.dataset.loaded = 'true';
    } catch {
      container.innerHTML = `
        <div class="loading-state">
          <p class="text-muted">📄 Contenu non disponible.</p>
          <p class="text-muted" style="font-size:12px;">Le fichier /static/pages/${page}.html est introuvable.</p>
        </div>
      `;
    }
  }

  /* --------------------------------------------------------
     BOOT
     -------------------------------------------------------- */
  function init() {
    initSidebar();
    initNavigation();
    startHealthCheck();
  }

  // Wait for DOM
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
