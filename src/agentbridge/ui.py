"""AgentBridge Operations Console and admin dashboard."""

from fastapi.responses import HTMLResponse

CONSOLE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>AgentBridge Operations Console</title>
  <style>
    :root {
      --bg: #f6f1eb;
      --panel: #ffffff;
      --muted: #706a63;
      --text: #1f1d1b;
      --border: #e0d8cd;
      --brand: #2d2b2a;
      --accent: #b46439;
      --accent-soft: #f5e8df;
      --ok: #2c6f48;
      --ok-soft: #eaf5ee;
      --warn: #ad6927;
      --warn-soft: #f9efe2;
      --danger: #b23a3a;
      --danger-soft: #fbe6e6;
      --shadow: 0 10px 24px rgba(24, 20, 15, 0.06);
    }

    * { box-sizing: border-box; }
    html, body { margin: 0; padding: 0; font-family: Arial, sans-serif; background: var(--bg); color: var(--text); }
    body { min-height: 100vh; }
    button, input, select { font: inherit; }
    .hidden { display: none !important; }

    .login-shell {
      min-height: 100vh; display: grid; place-items: center; background: linear-gradient(135deg, #f6f1eb 0%, #efe4d9 100%);
      padding: 24px;
    }
    .login-card {
      width: min(480px, 100%); background: rgba(255,255,255,0.9); backdrop-filter: blur(10px);
      border: 1px solid var(--border); border-radius: 16px; box-shadow: var(--shadow); padding: 28px;
    }
    .eyebrow { text-transform: uppercase; letter-spacing: 0.12em; font-size: 11px; color: var(--muted); font-weight: 700; }
    h1 { margin: 12px 0 8px; font-size: 32px; }
    .login-card p { margin: 0 0 20px; color: var(--muted); }
    .field { display: grid; gap: 8px; margin-bottom: 14px; }
    .field label { font-weight: 600; color: var(--text); }
    .field input, .field select { width: 100%; padding: 12px 14px; border: 1px solid var(--border); border-radius: 10px; background: #fff; }
    .field input:focus, .field select:focus { outline: 2px solid rgba(180,100,57,0.15); border-color: var(--accent); }
    .primary-btn, .secondary-btn, .danger-btn, .ghost-btn {
      border: none; border-radius: 10px; padding: 11px 16px; cursor: pointer; font-weight: 700;
    }
    .primary-btn { background: var(--brand); color: white; }
    .secondary-btn { background: var(--panel); color: var(--text); border: 1px solid var(--border); }
    .danger-btn { background: var(--danger); color: white; }
    .ghost-btn { background: rgba(180,100,57,0.08); color: var(--accent); border: 1px solid rgba(180,100,57,0.18); }
    .stack { display: flex; gap: 10px; flex-wrap: wrap; }
    .toolbar { display: flex; flex-wrap: wrap; gap: 12px; align-items: end; margin: 12px 0 16px; }
    .toolbar .field { margin-bottom: 0; min-width: 180px; }
    .table-action { background: transparent; border: 1px solid var(--border); border-radius: 8px; padding: 6px 10px; color: var(--text); cursor: pointer; }
    .table-action.danger { border-color: rgba(178,58,58,0.25); color: var(--danger); background: rgba(178,58,58,0.04); }
    .alert { border-radius: 10px; padding: 10px 12px; font-size: 14px; margin-bottom: 16px; }
    .alert.error { background: var(--danger-soft); color: var(--danger); border: 1px solid #f0b1b1; }
    .alert.success { background: var(--ok-soft); color: var(--ok); border: 1px solid #b7d9bf; }

    .app-shell { display: none; min-height: 100vh; }
    .app-shell.visible { display: block; }
    .topbar {
      display: flex; justify-content: space-between; align-items: center; padding: 18px 24px; background: var(--brand); color: white; border-bottom: 1px solid rgba(255,255,255,0.08);
    }
    .brand { font-size: 20px; font-weight: 700; }
    .topbar-actions { display: flex; align-items: center; gap: 12px; }
    .user-pill { background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); border-radius: 999px; padding: 7px 12px; font-size: 12px; }

    .content { padding: 24px; }
    .grid { display: grid; gap: 18px; }
    .grid.two { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .grid.three { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .panel {
      background: var(--panel); border: 1px solid var(--border); border-radius: 14px; box-shadow: var(--shadow);
      padding: 18px; min-width: 0;
    }
    .panel h2 { margin: 0 0 12px; font-size: 18px; }
    .kpis { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; }
    .kpi {
      background: white; border: 1px solid var(--border); border-radius: 12px; padding: 16px; min-height: 90px;
    }
    .kpi-label { color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; }
    .kpi-value { margin-top: 10px; font-size: 28px; font-weight: 700; }
    .badge { display: inline-block; border-radius: 999px; padding: 5px 8px; font-size: 11px; font-weight: 700; }
    .badge.ok { background: var(--ok-soft); color: var(--ok); }
    .badge.warn { background: var(--warn-soft); color: var(--warn); }
    .badge.err { background: var(--danger-soft); color: var(--danger); }

    table { width: 100%; border-collapse: collapse; margin-top: 10px; }
    th, td { text-align: left; border-bottom: 1px solid var(--border); padding: 10px 8px; font-size: 13px; }
    th { color: var(--muted); text-transform: uppercase; letter-spacing: 0.06em; font-size: 11px; }
    .mono { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
    form { display: grid; gap: 12px; }
    .row { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
    .muted { color: var(--muted); }
    .chart-wrap { width: 100%; min-height: 220px; background: linear-gradient(180deg, rgba(180,100,57,0.04), rgba(180,100,57,0.01)); border-radius: 12px; border: 1px solid var(--border); padding: 12px; }
    canvas { width: 100%; height: 220px; display: block; }
    .empty { color: var(--muted); font-style: italic; }

    @media (max-width: 900px) {
      .grid.two, .grid.three, .kpis { grid-template-columns: 1fr; }
      .row { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <div id="loginView" class="login-shell">
    <div class="login-card">
      <div class="eyebrow">AgentBridge control plane</div>
      <h1>Sign in</h1>
      <p>Use an owner/operator admin token to manage tenants, projects, keys and usage.</p>
      <div id="authError" class="alert error hidden"></div>
      <div class="field">
        <label for="tokenInput">Admin token</label>
        <input id="tokenInput" type="password" placeholder="ga_..." />
      </div>
      <div class="stack">
        <button id="loginBtn" class="primary-btn">Login</button>
      </div>
    </div>
  </div>

  <div id="appView" class="app-shell">
    <header class="topbar">
      <div class="brand">AgentBridge</div>
      <div class="topbar-actions">
        <div id="adminInfo" class="user-pill">admin</div>
        <button id="logoutBtn" class="secondary-btn">Logout</button>
      </div>
    </header>

    <main class="content">
      <div class="grid" style="gap: 18px;">
        <section class="kpis" id="kpiCards"></section>

        <div class="grid two">
          <div class="panel">
            <h2>Tenants</h2>
            <form id="tenantForm">
              <div class="field">
                <label>Tenant name</label>
                <input name="tenantName" placeholder="e.g. acme" required />
              </div>
              <div class="stack">
                <button class="primary-btn" type="submit">Create tenant</button>
              </div>
            </form>
            <table>
              <thead>
                <tr><th>Name</th><th>ID</th><th>Actions</th></tr>
              </thead>
              <tbody id="tenantTableBody"></tbody>
            </table>
          </div>

          <div class="panel">
            <h2>Projects</h2>
            <form id="projectForm">
              <div class="field">
                <label>Tenant</label>
                <select id="projectTenantSelect" required></select>
              </div>
              <div class="row">
                <div class="field">
                  <label>Project name</label>
                  <input name="projectName" placeholder="e.g. backend" required />
                </div>
                <div class="field">
                  <label>Budget mode</label>
                  <select name="budgetMode">
                    <option value="hard">hard</option>
                    <option value="soft">soft</option>
                  </select>
                </div>
              </div>
              <div class="row">
                <div class="field">
                  <label>Monthly token budget</label>
                  <input name="monthlyTokenBudget" type="number" min="0" step="1" placeholder="1000000" />
                </div>
                <div class="field">
                  <label>Monthly cost budget (USD)</label>
                  <input name="monthlyCostBudget" type="number" min="0" step="0.01" placeholder="250.00" />
                </div>
              </div>
              <div class="stack">
                <button class="primary-btn" type="submit">Create project</button>
              </div>
            </form>
            <table>
              <thead>
                <tr><th>Project</th><th>Tenant</th><th>Budget</th><th>Actions</th></tr>
              </thead>
              <tbody id="projectTableBody"></tbody>
            </table>
          </div>
        </div>

        <div class="grid two">
          <div class="panel">
            <h2>API keys</h2>
            <form id="keyForm">
              <div class="field">
                <label>Project</label>
                <select id="keyProjectSelect" required></select>
              </div>
              <div class="row">
                <div class="field">
                  <label>Key name</label>
                  <input name="keyName" placeholder="backend-prod" required />
                </div>
                <div class="field">
                  <label>Allowed aliases</label>
                  <input name="allowedAliases" placeholder="chat-default,embed-default" />
                </div>
              </div>
              <div class="row">
                <div class="field">
                  <label>RPM limit</label>
                  <input name="rpmLimit" type="number" min="1" value="60" required />
                </div>
                <div class="field">
                  <label>TPM limit</label>
                  <input name="tpmLimit" type="number" min="1" value="100000" required />
                </div>
              </div>
              <div class="stack">
                <button class="primary-btn" type="submit">Create key</button>
              </div>
            </form>
            <div id="newKeyBox" class="alert success hidden" style="margin-top: 14px;"></div>
            <table>
              <thead>
                <tr><th>Name</th><th>Prefix</th><th>RPM</th><th>TPM</th><th>Status</th><th>Actions</th></tr>
              </thead>
              <tbody id="keyTableBody"></tbody>
            </table>
          </div>

          <div class="panel">
            <h2>Provider health</h2>
            <div id="providerHealth"></div>
          </div>
        </div>

        <div class="panel">
          <h2>Usage overview</h2>
          <div class="toolbar">
            <div class="field" style="max-width: 240px; margin-top: 0;">
              <label for="usageProjectSelect">Project</label>
              <select id="usageProjectSelect"></select>
            </div>
            <div class="field" style="max-width: 180px; margin-top: 0;">
              <label for="usageFromInput">From</label>
              <input id="usageFromInput" type="date" />
            </div>
            <div class="field" style="max-width: 180px; margin-top: 0;">
              <label for="usageToInput">To</label>
              <input id="usageToInput" type="date" />
            </div>
            <button id="usageRefreshBtn" class="secondary-btn" type="button">Apply filters</button>
          </div>
          <div class="chart-wrap">
            <canvas id="usageChart" width="900" height="220"></canvas>
          </div>
          <table>
            <thead>
              <tr><th>Day</th><th>Requests</th><th>Prompt tokens</th><th>Completion tokens</th><th>Cost</th></tr>
            </thead>
            <tbody id="usageTableBody"></tbody>
          </table>
        </div>
      </div>
    </main>
  </div>

  <script>
    const TOKEN_KEY = 'agentbridge-admin-token';
    const state = {
      token: localStorage.getItem(TOKEN_KEY) || '',
      admin: null,
      tenants: [],
      projects: [],
      keys: [],
      providerHealth: {},
      usage: [],
      usageFilters: { from: '', to: '' },
      selectedProjectId: null
    };

    const ui = {
      loginView: document.getElementById('loginView'),
      appView: document.getElementById('appView'),
      authError: document.getElementById('authError'),
      tokenInput: document.getElementById('tokenInput'),
      adminInfo: document.getElementById('adminInfo'),
      tenantTableBody: document.getElementById('tenantTableBody'),
      projectTableBody: document.getElementById('projectTableBody'),
      keyTableBody: document.getElementById('keyTableBody'),
      projectTenantSelect: document.getElementById('projectTenantSelect'),
      keyProjectSelect: document.getElementById('keyProjectSelect'),
      usageProjectSelect: document.getElementById('usageProjectSelect'),
      usageFromInput: document.getElementById('usageFromInput'),
      usageToInput: document.getElementById('usageToInput'),
      usageRefreshBtn: document.getElementById('usageRefreshBtn'),
      providerHealth: document.getElementById('providerHealth'),
      usageTableBody: document.getElementById('usageTableBody'),
      kpiCards: document.getElementById('kpiCards'),
      newKeyBox: document.getElementById('newKeyBox'),
      usageChart: document.getElementById('usageChart')
    };

    function setAuthError(message) {
      if (!message) {
        ui.authError.classList.add('hidden');
        ui.authError.textContent = '';
        return;
      }
      ui.authError.textContent = message;
      ui.authError.classList.remove('hidden');
    }

    function showApp() {
      ui.loginView.classList.add('hidden');
      ui.appView.classList.add('visible');
    }

    function showLogin() {
      ui.appView.classList.remove('visible');
      ui.loginView.classList.remove('hidden');
    }

    async function api(path, options = {}) {
      const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };
      const token = state.token;
      if (token) {
        headers.Authorization = `Bearer ${token}`;
      }
      const response = await fetch(path, {
        ...options,
        headers,
      });
      const text = await response.text();
      let payload = null;
      try {
        payload = text ? JSON.parse(text) : null;
      } catch (e) {
        payload = text;
      }
      if (!response.ok) {
        const detail = payload && typeof payload === 'object' && payload.detail ? payload.detail : 'Request failed';
        throw new Error(typeof detail === 'string' ? detail : JSON.stringify(detail));
      }
      return payload;
    }

    async function login() {
      const token = ui.tokenInput.value.trim();
      if (!token) {
        setAuthError('Please enter an admin token.');
        return;
      }
      state.token = token;
      localStorage.setItem(TOKEN_KEY, token);
      try {
        state.admin = await api('/admin/v1/me');
        ui.adminInfo.textContent = `${state.admin.email} (${state.admin.role})`;
        setAuthError('');
        ui.tokenInput.value = '';
        await loadDashboard();
        showApp();
      } catch (error) {
        state.token = '';
        localStorage.removeItem(TOKEN_KEY);
        setAuthError(error.message || 'Login failed');
        showLogin();
      }
    }

    function logout() {
      state.token = '';
      state.admin = null;
      localStorage.removeItem(TOKEN_KEY);
      ui.adminInfo.textContent = 'admin';
      ui.newKeyBox.classList.add('hidden');
      showLogin();
    }

    async function loadDashboard() {
      ui.usageFromInput.value = state.usageFilters.from;
      ui.usageToInput.value = state.usageFilters.to;
      await Promise.all([loadTenants(), loadProjects(), loadProviderHealth()]);
      if (state.projects.length) {
        const selected = state.projects.find(p => p.id === state.selectedProjectId) || state.projects[0];
        state.selectedProjectId = selected ? selected.id : null;
      }
      await loadProjectKeys();
      await loadUsage();
      renderKPIs();
    }

    async function loadTenants() {
      const tenants = await api('/admin/v1/tenants');
      state.tenants = tenants;
      renderTenantOptions();
      renderTenantTable();
    }

    async function loadProjects() {
      const projects = await api('/admin/v1/projects');
      state.projects = projects;
      renderProjectSelectors();
      renderProjectTable();
    }

    async function loadProviderHealth() {
      const health = await api('/admin/v1/providers/health');
      state.providerHealth = health;
      renderProviderHealth();
    }

    async function loadProjectKeys() {
      const projectId = state.selectedProjectId || (state.projects[0] && state.projects[0].id) || null;
      if (!projectId) {
        state.keys = [];
        renderKeyTable();
        return;
      }
      const rows = await api(`/admin/v1/keys?project_id=${encodeURIComponent(projectId)}`);
      state.keys = rows;
      renderKeyTable();
    }

    async function loadUsage() {
      const projectId = state.selectedProjectId || (state.projects[0] && state.projects[0].id) || null;
      if (!projectId) {
        state.usage = [];
        renderUsage();
        return;
      }
      const params = new URLSearchParams({
        project_id: projectId,
        group_by: 'day'
      });
      if (state.usageFilters.from) params.set('from', state.usageFilters.from);
      if (state.usageFilters.to) params.set('to', state.usageFilters.to);
      const rows = await api(`/admin/v1/usage?${params.toString()}`);
      state.usage = rows;
      renderUsage();
      renderKPIs();
    }

    function renderTenantOptions() {
      const options = state.tenants.map(t => `<option value="${t.id}">${t.name}</option>`).join('');
      ui.projectTenantSelect.innerHTML = options || '<option value="">No tenant available</option>';
      ui.projectTenantSelect.disabled = !state.tenants.length;
    }

    function renderProjectSelectors() {
      const projectOptions = state.projects.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
      ui.keyProjectSelect.innerHTML = projectOptions || '<option value="">No project available</option>';
      ui.usageProjectSelect.innerHTML = projectOptions || '<option value="">No project available</option>';
      ui.keyProjectSelect.disabled = !state.projects.length;
      ui.usageProjectSelect.disabled = !state.projects.length;
      if (state.projects.length && !state.selectedProjectId) {
        state.selectedProjectId = state.projects[0].id;
      }
      if (state.selectedProjectId && state.projects.some(p => p.id === state.selectedProjectId)) {
        ui.keyProjectSelect.value = state.selectedProjectId;
        ui.usageProjectSelect.value = state.selectedProjectId;
      }
    }

    function renderTenantTable() {
      if (!state.tenants.length) {
        ui.tenantTableBody.innerHTML = '<tr><td colspan="3" class="empty">No tenants yet</td></tr>';
        return;
      }
      ui.tenantTableBody.innerHTML = state.tenants.map(t => `
        <tr>
          <td>${t.name}</td>
          <td class="mono">${t.id}</td>
          <td><button class="table-action danger" data-action="delete-tenant" data-id="${t.id}">Delete</button></td>
        </tr>
      `).join('');
    }

    function renderProjectTable() {
      if (!state.projects.length) {
        ui.projectTableBody.innerHTML = '<tr><td colspan="4" class="empty">No projects yet</td></tr>';
        return;
      }
      ui.projectTableBody.innerHTML = state.projects.map(p => {
        const tenantName = state.tenants.find(t => t.id === p.tenant_id)?.name || p.tenant_id;
        const budget = p.monthly_token_budget ? `${Number(p.monthly_token_budget).toLocaleString()} tokens` : 'No cap';
        return `
          <tr>
            <td>${p.name}</td>
            <td>${tenantName}</td>
            <td class="mono">${budget}</td>
            <td><button class="table-action danger" data-action="delete-project" data-id="${p.id}">Delete</button></td>
          </tr>
        `;
      }).join('');
    }

    function renderKeyTable() {
      if (!state.keys.length) {
        ui.keyTableBody.innerHTML = '<tr><td colspan="6" class="empty">No keys for this project</td></tr>';
        return;
      }
      ui.keyTableBody.innerHTML = state.keys.map(k => `
        <tr>
          <td>${k.name}</td>
          <td class="mono">${k.prefix}</td>
          <td>${k.rpm_limit}</td>
          <td>${k.tpm_limit}</td>
          <td><span class="badge ${k.revoked ? 'warn' : 'ok'}">${k.revoked ? 'revoked' : 'active'}</span></td>
          <td><button class="table-action danger" data-action="delete-key" data-id="${k.id}">Revoke</button></td>
        </tr>
      `).join('');
    }

    function renderProviderHealth() {
      const entries = Object.entries(state.providerHealth || {});
      if (!entries.length) {
        ui.providerHealth.innerHTML = '<div class="empty">No provider health data yet.</div>';
        return;
      }
      ui.providerHealth.innerHTML = entries.map(([name, data]) => {
        const circuit = data.circuit || 'unknown';
        const badgeClass = circuit === 'closed' ? 'ok' : circuit === 'half_open' ? 'warn' : 'err';
        const latencyText = data.ewma_latency_s && Object.keys(data.ewma_latency_s).length
          ? Object.entries(data.ewma_latency_s).map(([k, v]) => `${k.split(':').pop()}: ${Number(v).toFixed(3)}s`).join(', ')
          : 'n/a';
        return `
          <div class="panel" style="padding: 14px; margin-bottom: 12px; border-color: var(--border);">
            <div style="display:flex;justify-content:space-between;align-items:center; margin-bottom: 8px; gap: 8px;">
              <strong>${name}</strong>
              <span class="badge ${badgeClass}">${circuit}</span>
            </div>
            <div class="muted mono">EWMA latency: ${latencyText}</div>
          </div>
        `;
      }).join('');
    }

    function renderKPIs() {
      const totalProjects = state.projects.length;
      const activeKeys = state.keys.filter(k => !k.revoked).length;
      const providerCount = Object.keys(state.providerHealth || {}).length;
      const totalUsage = state.usage.reduce((sum, row) => sum + (Number(row.requests) || 0), 0);
      const totalCost = state.usage.reduce((sum, row) => sum + (Number(row.est_cost_usd) || 0), 0);
      const cards = [
        { label: 'Projects', value: String(totalProjects) },
        { label: 'Active keys', value: String(activeKeys) },
        { label: 'Providers', value: String(providerCount) },
        { label: 'Requests', value: Number(totalUsage).toLocaleString() },
        { label: 'Cost', value: `$${totalCost.toFixed(4)}` }
      ];
      ui.kpiCards.innerHTML = cards.map(card => `
        <div class="kpi">
          <div class="kpi-label">${card.label}</div>
          <div class="kpi-value">${card.value}</div>
        </div>
      `).join('');
    }

    function renderUsage() {
      const rows = state.usage || [];
      ui.usageTableBody.innerHTML = !rows.length ? '<tr><td colspan="5" class="empty">No usage data yet for this window.</td></tr>' : rows.map(row => `
        <tr>
          <td>${row.day || 'n/a'}</td>
          <td>${Number(row.requests || 0).toLocaleString()}</td>
          <td>${Number(row.prompt_tokens || 0).toLocaleString()}</td>
          <td>${Number(row.completion_tokens || 0).toLocaleString()}</td>
          <td>$${Number(row.est_cost_usd || 0).toFixed(4)}</td>
        </tr>
      `).join('');
      drawUsageChart(rows);
    }

    function drawUsageChart(rows) {
      const canvas = ui.usageChart;
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
      gradient.addColorStop(0, 'rgba(180,100,57,0.28)');
      gradient.addColorStop(1, 'rgba(180,100,57,0.04)');

      const margin = { top: 18, right: 30, bottom: 32, left: 40 };
      const maxValue = Math.max(...rows.map(r => Number(r.requests || 0)), 1);
      const width = canvas.width - margin.left - margin.right;
      const height = canvas.height - margin.top - margin.bottom;

      ctx.fillStyle = gradient;
      ctx.fillRect(margin.left, margin.top, width, height);

      ctx.strokeStyle = '#d8d0c3';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(margin.left, margin.top);
      ctx.lineTo(margin.left, height + margin.top);
      ctx.lineTo(margin.left + width, height + margin.top);
      ctx.stroke();

      for (let step = 0; step <= 4; step += 1) {
        const y = margin.top + (height / 4) * step;
        ctx.strokeStyle = 'rgba(112,106,99,0.18)';
        ctx.beginPath();
        ctx.moveTo(margin.left, y);
        ctx.lineTo(margin.left + width, y);
        ctx.stroke();
        const valueLabel = Math.round(maxValue - ((maxValue / 4) * step));
        ctx.fillStyle = '#706a63';
        ctx.font = '11px sans-serif';
        ctx.fillText(String(valueLabel), 8, y + 4);
      }

      const barWidth = Math.max(18, width / Math.max(rows.length, 1) - 12);
      rows.forEach((row, index) => {
        const x = margin.left + index * (width / Math.max(rows.length, 1)) + 8;
        const value = Number(row.requests || 0);
        const barHeight = (value / maxValue) * height;
        const y = margin.top + height - barHeight;
        ctx.fillStyle = '#b46439';
        ctx.fillRect(x, y, barWidth, barHeight);
      });

      ctx.fillStyle = '#5a534d';
      ctx.font = '12px sans-serif';
      rows.forEach((row, index) => {
        const x = margin.left + index * (width / Math.max(rows.length, 1)) + 8;
        ctx.fillText(row.day ? String(row.day).slice(5) : 'n/a', x, canvas.height - 8);
      });
    }

    document.getElementById('loginBtn').addEventListener('click', login);
    document.getElementById('logoutBtn').addEventListener('click', logout);
    ui.tokenInput.addEventListener('keydown', (event) => {
      if (event.key === 'Enter') login();
    });

    document.getElementById('tenantForm').addEventListener('submit', async (event) => {
      event.preventDefault();
      const form = new FormData(event.currentTarget);
      const name = form.get('tenantName');
      await api('/admin/v1/tenants', { method: 'POST', body: JSON.stringify({ name }) });
      event.currentTarget.reset();
      await loadTenants();
      await loadProjects();
    });

    document.getElementById('projectForm').addEventListener('submit', async (event) => {
      event.preventDefault();
      const form = new FormData(event.currentTarget);
      const tenantId = ui.projectTenantSelect.value;
      const payload = {
        tenant_id: tenantId,
        name: form.get('projectName'),
        monthly_token_budget: form.get('monthlyTokenBudget') ? Number(form.get('monthlyTokenBudget')) : null,
        monthly_cost_budget_usd: form.get('monthlyCostBudget') ? Number(form.get('monthlyCostBudget')) : null,
        budget_mode: form.get('budgetMode')
      };
      await api('/admin/v1/projects', { method: 'POST', body: JSON.stringify(payload) });
      event.currentTarget.reset();
      await loadProjects();
      await loadUsage();
    });

    document.getElementById('keyForm').addEventListener('submit', async (event) => {
      event.preventDefault();
      const form = new FormData(event.currentTarget);
      const projectId = ui.keyProjectSelect.value;
      const allowedAliases = String(form.get('allowedAliases') || '').split(',').map(v => v.trim()).filter(Boolean);
      const payload = {
        project_id: projectId,
        name: form.get('keyName'),
        allowed_aliases: allowedAliases.length ? allowedAliases : null,
        rpm_limit: Number(form.get('rpmLimit')),
        tpm_limit: Number(form.get('tpmLimit'))
      };
      const result = await api('/admin/v1/keys', { method: 'POST', body: JSON.stringify(payload) });
      ui.newKeyBox.textContent = `Key created successfully: ${result.key}`;
      ui.newKeyBox.classList.remove('hidden');
      event.currentTarget.reset();
      await loadProjectKeys();
    });

    ui.keyProjectSelect.addEventListener('change', async (event) => {
      state.selectedProjectId = event.target.value || null;
      await loadProjectKeys();
      await loadUsage();
    });

    ui.usageProjectSelect.addEventListener('change', async (event) => {
      state.selectedProjectId = event.target.value || null;
      await loadProjectKeys();
      await loadUsage();
    });

    ui.usageRefreshBtn.addEventListener('click', async () => {
      state.usageFilters.from = ui.usageFromInput.value;
      state.usageFilters.to = ui.usageToInput.value;
      await loadUsage();
    });

    document.addEventListener('click', async (event) => {
      const target = event.target.closest('[data-action]');
      if (!target) return;
      const { action, id } = target.dataset;
      if (!id) return;
      if (action === 'delete-key') {
        if (!window.confirm('Revoke this API key?')) return;
        await api(`/admin/v1/keys/${encodeURIComponent(id)}`, { method: 'DELETE' });
        await loadProjectKeys();
        await loadUsage();
      }
      if (action === 'delete-project') {
        if (!window.confirm('Delete this project and all of its API keys?')) return;
        await api(`/admin/v1/projects/${encodeURIComponent(id)}`, { method: 'DELETE' });
        await loadProjects();
        await loadProjectKeys();
        await loadUsage();
      }
      if (action === 'delete-tenant') {
        if (!window.confirm('Delete this tenant and all child projects/keys?')) return;
        await api(`/admin/v1/tenants/${encodeURIComponent(id)}`, { method: 'DELETE' });
        await loadTenants();
        await loadProjects();
        await loadProjectKeys();
        await loadUsage();
      }
    });

    if (state.token) {
      api('/admin/v1/me').then(async (admin) => {
        state.admin = admin;
        ui.adminInfo.textContent = `${admin.email} (${admin.role})`;
        await loadDashboard();
        showApp();
      }).catch(() => {
        logout();
      });
    } else {
      showLogin();
    }
  </script>
</body>
</html>
"""


def render_console(*, providers: list[str] | None = None, aliases: list[str] | None = None) -> HTMLResponse:
    """Return the live operations console with a browser-based admin dashboard."""
    return HTMLResponse(content=CONSOLE_HTML, status_code=200)
