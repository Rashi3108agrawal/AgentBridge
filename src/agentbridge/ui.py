"""
AgentBridge Operations Console.
Enterprise engineering console for inspecting routing topology, provider health,
circuit breakers, admission quotas, and live telemetry.
"""

from fastapi.responses import HTMLResponse

CONSOLE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AgentBridge Operations Console</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-canvas: #F5F1EA;
      --bg-panel: #FFFFFF;
      --bg-subtle: #F0ECE4;
      --bg-hover: #E9E4DC;
      --text-main: #232323;
      --text-muted: #6E7881;
      --text-dim: #8E979F;
      --border-color: #D8D1C8;
      --border-subtle: #E5DFD6;
      --slate-warm: #262220;
      --burnt-orange: #B46A3C;
      --burnt-orange-subtle: #F6EDE6;
      --muted-olive: #596157;
      --muted-olive-subtle: #EEF1EE;
      --steel: #6E7881;
      --charcoal: #1D1F22;
      --status-ok: #3F6E4D;
      --status-ok-bg: #EAF2EC;
      --status-warn: #A6682B;
      --status-warn-bg: #FAF2EA;
      --status-err: #A23B3B;
      --status-err-bg: #FBEFEF;
      --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-mono: 'JetBrains Mono', SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      --radius-sm: 4px;
      --radius-md: 6px;
      --shadow-sm: 0 1px 2px rgba(38, 34, 32, 0.04);
      --shadow-md: 0 4px 8px -2px rgba(38, 34, 32, 0.06);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg-canvas);
      color: var(--text-main);
      font-family: var(--font-sans);
      font-size: 13px;
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
    }

    /* Top Navigation Bar */
    header.top-nav {
      height: 48px;
      background: var(--slate-warm);
      color: #F7F4EF;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px;
      border-bottom: 1px solid #1a1715;
    }
    .brand-section {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .brand-logo {
      font-weight: 700;
      font-size: 15px;
      letter-spacing: -0.02em;
      color: #F7F4EF;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .brand-logo .dot {
      width: 8px;
      height: 8px;
      background: var(--burnt-orange);
      border-radius: 2px;
    }
    .version-tag {
      font-family: var(--font-mono);
      font-size: 10px;
      background: #393431;
      color: #C7C2BA;
      padding: 1px 6px;
      border-radius: var(--radius-sm);
      border: 1px solid #4a4440;
    }
    .cluster-pill {
      display: flex;
      align-items: center;
      gap: 6px;
      background: #332E2C;
      padding: 3px 10px;
      border-radius: var(--radius-sm);
      font-size: 11px;
      color: #E2DDD5;
      border: 1px solid #453F3B;
    }
    .indicator-green {
      width: 7px;
      height: 7px;
      background: #56B370;
      border-radius: 50%;
    }
    .top-actions {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 11px;
    }
    .shortcut-hint {
      font-family: var(--font-mono);
      background: #383330;
      color: #C0BAB1;
      padding: 2px 6px;
      border-radius: 3px;
      font-size: 10px;
    }
    .user-badge {
      display: flex;
      align-items: center;
      gap: 6px;
      color: #D3CDC4;
      font-family: var(--font-mono);
    }
    .role-tag {
      background: var(--burnt-orange);
      color: #FFF;
      font-size: 9px;
      padding: 1px 5px;
      border-radius: 2px;
      font-weight: 600;
    }

    /* Layout Shell */
    .app-shell {
      display: flex;
      height: calc(100vh - 48px);
      overflow: hidden;
    }

    /* Sidebar */
    aside.sidebar {
      width: 220px;
      background: #EFEAE1;
      border-right: 1px solid var(--border-color);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
    }
    .nav-group-title {
      font-size: 10px;
      text-transform: uppercase;
      font-weight: 600;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      padding: 16px 14px 6px;
    }
    .nav-list {
      list-style: none;
      padding: 0 8px;
    }
    .nav-item {
      display: flex;
      align-items: center;
      gap: 9px;
      padding: 7px 10px;
      border-radius: var(--radius-sm);
      font-size: 12px;
      font-weight: 500;
      color: #383431;
      cursor: pointer;
      text-decoration: none;
      margin-bottom: 2px;
      transition: background 0.12s ease;
    }
    .nav-item:hover {
      background: var(--bg-hover);
      color: var(--charcoal);
    }
    .nav-item.active {
      background: var(--slate-warm);
      color: #F7F4EF;
      font-weight: 600;
    }
    .nav-count {
      margin-left: auto;
      font-family: var(--font-mono);
      font-size: 10px;
      opacity: 0.7;
    }

    /* Sidebar Footer Telemetry */
    .sidebar-footer {
      margin-top: auto;
      padding: 12px;
      border-top: 1px solid var(--border-color);
      background: #E8E2D7;
      font-size: 11px;
    }
    .mini-stat {
      display: flex;
      justify-content: space-between;
      margin-bottom: 4px;
      color: var(--text-muted);
    }
    .mini-stat span.val {
      font-family: var(--font-mono);
      color: var(--text-main);
      font-weight: 600;
    }

    /* Main Workspace */
    main.workspace {
      flex: 1;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
    }

    /* Cluster Status Ribbon */
    .ribbon {
      background: #FAF7F2;
      border-bottom: 1px solid var(--border-color);
      padding: 12px 20px;
      display: flex;
      align-items: center;
      gap: 24px;
      flex-wrap: wrap;
    }
    .ribbon-cell {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }
    .ribbon-cell .label {
      font-size: 10px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--text-muted);
    }
    .ribbon-cell .metric {
      font-family: var(--font-mono);
      font-size: 14px;
      font-weight: 600;
      color: var(--slate-warm);
    }
    .ribbon-cell .metric.good { color: var(--status-ok); }
    .ribbon-cell .sub {
      font-size: 10px;
      color: var(--text-dim);
    }

    /* View Content Panels */
    .view-content {
      padding: 20px;
      flex: 1;
      display: none;
    }
    .view-content.active {
      display: block;
    }

    .section-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      margin-bottom: 14px;
    }
    .section-title {
      font-size: 16px;
      font-weight: 700;
      letter-spacing: -0.01em;
      color: var(--slate-warm);
    }
    .section-desc {
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 2px;
    }
    .toolbar-actions {
      display: flex;
      gap: 8px;
    }

    /* Engineering Buttons */
    .btn {
      font-family: var(--font-sans);
      font-size: 12px;
      font-weight: 500;
      padding: 5px 12px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      border: 1px solid var(--border-color);
      background: var(--bg-panel);
      color: var(--text-main);
      transition: all 0.12s ease;
    }
    .btn:hover {
      background: var(--bg-subtle);
      border-color: #BDB5AA;
    }
    .btn-primary {
      background: var(--slate-warm);
      color: #F7F4EF;
      border-color: var(--slate-warm);
    }
    .btn-primary:hover {
      background: #393431;
    }
    .btn-burnt {
      background: var(--burnt-orange);
      color: #FFF;
      border-color: var(--burnt-orange);
    }
    .btn-burnt:hover {
      background: #9B5A32;
    }

    /* Dense Data Table */
    .table-container {
      background: var(--bg-panel);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      box-shadow: var(--shadow-sm);
      overflow-x: auto;
    }
    table.dense-table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 12px;
    }
    table.dense-table th {
      background: #FAF7F2;
      border-bottom: 1px solid var(--border-color);
      padding: 8px 12px;
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--text-muted);
      white-space: nowrap;
    }
    table.dense-table td {
      padding: 8px 12px;
      border-bottom: 1px solid var(--border-subtle);
      color: var(--text-main);
      vertical-align: middle;
      white-space: nowrap;
    }
    table.dense-table tr:last-child td {
      border-bottom: none;
    }
    table.dense-table tr:hover td {
      background: #FDFBF8;
    }

    /* Monospace elements */
    .mono {
      font-family: var(--font-mono);
      font-size: 11px;
    }

    /* Pills & Badges */
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 1px 7px;
      border-radius: 3px;
      font-size: 11px;
      font-weight: 500;
      border: 1px solid transparent;
    }
    .badge-ok {
      background: var(--status-ok-bg);
      color: var(--status-ok);
      border-color: #CBE0D1;
    }
    .badge-warn {
      background: var(--status-warn-bg);
      color: var(--status-warn);
      border-color: #EFDBC9;
    }
    .badge-err {
      background: var(--status-err-bg);
      color: var(--status-err);
      border-color: #EAC9C9;
    }
    .badge-neutral {
      background: #EFEAE2;
      color: var(--slate-warm);
      border-color: #DFD8CC;
    }
    .badge-olive {
      background: var(--muted-olive-subtle);
      color: var(--muted-olive);
      border-color: #D3DAD3;
    }
    .badge-burnt {
      background: var(--burnt-orange-subtle);
      color: var(--burnt-orange);
      border-color: #EBD6C7;
    }

    /* Cards Grid */
    .grid-2 {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
      margin-bottom: 16px;
    }
    .grid-3 {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      margin-bottom: 16px;
    }
    .card {
      background: var(--bg-panel);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 16px;
      box-shadow: var(--shadow-sm);
    }
    .card-title {
      font-size: 13px;
      font-weight: 600;
      color: var(--slate-warm);
      margin-bottom: 6px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .card-desc {
      font-size: 11px;
      color: var(--text-muted);
      margin-bottom: 12px;
    }

    /* Code Block / Topology Inspector */
    pre.code-view {
      background: #201D1B;
      color: #E8E3DA;
      font-family: var(--font-mono);
      font-size: 11px;
      line-height: 1.5;
      padding: 12px;
      border-radius: var(--radius-sm);
      overflow-x: auto;
      border: 1px solid #36312E;
    }

    /* Right Inspection Drawer */
    .drawer {
      border-left: 1px solid var(--border-color);
      background: #FAF7F2;
      padding: 16px;
      width: 320px;
      flex-shrink: 0;
      overflow-y: auto;
    }
    .drawer-title {
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--slate-warm);
      margin-bottom: 12px;
    }
    .drawer-kv {
      display: flex;
      justify-content: space-between;
      padding: 6px 0;
      border-bottom: 1px solid var(--border-subtle);
      font-size: 11px;
    }
    .drawer-kv .key {
      color: var(--text-muted);
    }
    .drawer-kv .val {
      font-family: var(--font-mono);
      font-weight: 600;
      color: var(--charcoal);
    }

    /* Filter Bar */
    .filter-bar {
      display: flex;
      gap: 10px;
      margin-bottom: 12px;
      align-items: center;
    }
    .search-input {
      background: var(--bg-panel);
      border: 1px solid var(--border-color);
      padding: 5px 10px;
      border-radius: var(--radius-sm);
      font-size: 12px;
      font-family: var(--font-sans);
      color: var(--text-main);
      width: 240px;
    }
    .search-input:focus {
      outline: none;
      border-color: var(--burnt-orange);
    }
  </style>
</head>
<body>

  <!-- Top Header Navigation -->
  <header class="top-nav">
    <div class="brand-section">
      <div class="brand-logo">
        <div class="dot"></div>
        AgentBridge
      </div>
      <span class="version-tag">v1.0.0</span>
      <div class="cluster-pill">
        <div class="indicator-green"></div>
        <span>Production Cluster: us-east-1</span>
      </div>
    </div>
    <div class="top-actions">
      <div>Search <span class="shortcut-hint">Ctrl+K</span></div>
      <div class="user-badge">
        <span>admin@agentbridge.io</span>
        <span class="role-tag">OWNER</span>
      </div>
    </div>
  </header>

  <div class="app-shell">
    <!-- Left Navigation Sidebar -->
    <aside class="sidebar">
      <div class="nav-group-title">Platform Plane</div>
      <ul class="nav-list">
        <li><a class="nav-item active" data-view="routing">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 3 21 3 21 8"/><line x1="4" y1="20" x2="21" y2="3"/><polyline points="21 16 21 21 16 21"/><line x1="15" y1="15" x2="21" y2="21"/><line x1="4" y1="4" x2="9" y2="9"/></svg>
          Intelligence Routing
          <span class="nav-count">4</span>
        </a></li>
        <li><a class="nav-item" data-view="providers">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="8" rx="2" ry="2"/><rect x="2" y="14" width="20" height="8" rx="2" ry="2"/><line x1="6" y1="6" x2="6.01" y2="6"/><line x1="6" y1="18" x2="6.01" y2="18"/></svg>
          Provider Registry
          <span class="nav-count">5</span>
        </a></li>
        <li><a class="nav-item" data-view="governance">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
          Governance & Quotas
          <span class="nav-count">12</span>
        </a></li>
        <li><a class="nav-item" data-view="telemetry">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
          Execution Telemetry
          <span class="nav-count">LIVE</span>
        </a></li>
      </ul>

      <div class="nav-group-title">Engine Configuration</div>
      <ul class="nav-list">
        <li><a class="nav-item" data-view="caching">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>
          Cache Layer
        </a></li>
        <li><a class="nav-item" data-view="system">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
          System Topology
        </a></li>
      </ul>

      <div class="sidebar-footer">
        <div class="mini-stat"><span>Configured Providers</span><span class="val">{{PROVIDER_COUNT}}</span></div>
        <div class="mini-stat"><span>Aliases</span><span class="val">{{ALIAS_COUNT}}</span></div>
        <div class="mini-stat"><span>Provider Set</span><span class="val mono">{{PROVIDER_NAMES}}</span></div>
        <div class="mini-stat"><span>Alias Set</span><span class="val mono">{{ALIAS_NAMES}}</span></div>
      </div>
    </aside>

    <!-- Main Workspace Content -->
    <main class="workspace">

      <!-- Status Summary Ribbon -->
      <section class="ribbon">
        <div class="ribbon-cell">
          <span class="label">Platform Status</span>
          <span class="metric good">ONLINE</span>
          <span class="sub">All 5 providers reachable</span>
        </div>
        <div class="ribbon-cell">
          <span class="label">Gateway Overhead (P95)</span>
          <span class="metric">12.8 ms</span>
          <span class="sub">Target budget &lt; 20 ms</span>
        </div>
        <div class="ribbon-cell">
          <span class="label">Active Leases</span>
          <span class="metric">48 req</span>
          <span class="sub">Across 3 worker nodes</span>
        </div>
        <div class="ribbon-cell">
          <span class="label">Circuit Breakers</span>
          <span class="metric good">0 / 5 OPEN</span>
          <span class="sub">100% target availability</span>
        </div>
        <div class="ribbon-cell">
          <span class="label">Token Volume (24h)</span>
          <span class="metric">18,429,102</span>
          <span class="sub">Estimated $24.81 USD</span>
        </div>
        <div class="ribbon-cell">
          <span class="label">Cache Hit Ratio</span>
          <span class="metric">31.4%</span>
          <span class="sub">Exact + Semantic</span>
        </div>
      </section>

      <!-- View 1: Intelligence Routing -->
      <div id="view-routing" class="view-content active">
        <div class="section-header">
          <div>
            <h1 class="section-title">Intelligence Routing Matrix</h1>
            <p class="section-desc">Multi-target resolution rules, fallback policies, capability filtering, and priority chains.</p>
          </div>
          <div class="toolbar-actions">
            <button class="btn" onclick="alert('Exporting YAML configuration...')">Export Config</button>
            <button class="btn btn-primary" onclick="alert('Testing route policy simulation...')">Simulate Policy</button>
          </div>
        </div>

        <div class="filter-bar">
          <input type="text" class="search-input" placeholder="Filter aliases or targets...">
          <button class="btn">Policy: All</button>
          <button class="btn">Tools: Required</button>
        </div>

        <div class="table-container">
          <table class="dense-table">
            <thead>
              <tr>
                <th>Alias Identifier</th>
                <th>Routing Policy</th>
                <th>Target Cascades (Priority &middot; Weight)</th>
                <th>Context Ceiling</th>
                <th>Capabilities</th>
                <th>Per-Attempt Deadline</th>
                <th>Overall Timeout</th>
                <th>Fallback Triggers</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong class="mono" style="color:var(--burnt-orange)">chat-default</strong></td>
                <td><span class="badge badge-burnt">priority</span></td>
                <td>
                  <span class="mono">1. gemini:gemini-1.5-flash (p1, w1)</span><br>
                  <span class="mono">2. openai:gpt-4o-mini (p2, w1)</span><br>
                  <span class="mono">3. ollama:llama3 (p3, w1)</span>
                </td>
                <td class="mono">128,000 tok</td>
                <td>
                  <span class="badge badge-ok">tools</span>
                  <span class="badge badge-ok">stream</span>
                </td>
                <td class="mono">30,000 ms</td>
                <td class="mono">30,000 ms</td>
                <td><span class="badge badge-neutral">timeout</span> <span class="badge badge-neutral">5xx</span> <span class="badge badge-neutral">429</span> <span class="badge badge-neutral">circuit_open</span></td>
              </tr>
              <tr>
                <td><strong class="mono" style="color:var(--burnt-orange)">chat-fast</strong></td>
                <td><span class="badge badge-olive">latency (EWMA)</span></td>
                <td>
                  <span class="mono">1. gemini:gemini-1.5-flash (w2)</span><br>
                  <span class="mono">2. anthropic:claude-3-5-haiku (w1)</span>
                </td>
                <td class="mono">200,000 tok</td>
                <td>
                  <span class="badge badge-ok">tools</span>
                  <span class="badge badge-ok">stream</span>
                </td>
                <td class="mono">15,000 ms</td>
                <td class="mono">20,000 ms</td>
                <td><span class="badge badge-neutral">timeout</span> <span class="badge badge-neutral">5xx</span> <span class="badge badge-neutral">circuit_open</span></td>
              </tr>
              <tr>
                <td><strong class="mono" style="color:var(--burnt-orange)">chat-cheap</strong></td>
                <td><span class="badge badge-neutral">cost-optimized</span></td>
                <td>
                  <span class="mono">1. ollama:mistral-7b (w1)</span><br>
                  <span class="mono">2. gemini:gemini-1.5-flash (w1)</span>
                </td>
                <td class="mono">32,000 tok</td>
                <td>
                  <span class="badge badge-warn">no-tools</span>
                  <span class="badge badge-ok">stream</span>
                </td>
                <td class="mono">30,000 ms</td>
                <td class="mono">45,000 ms</td>
                <td><span class="badge badge-neutral">timeout</span> <span class="badge badge-neutral">5xx</span> <span class="badge badge-neutral">429</span></td>
              </tr>
              <tr>
                <td><strong class="mono" style="color:var(--burnt-orange)">embed-default</strong></td>
                <td><span class="badge badge-burnt">priority</span></td>
                <td>
                  <span class="mono">1. openai:text-embedding-3-small</span><br>
                  <span class="mono">2. ollama:nomic-embed-text</span>
                </td>
                <td class="mono">8,191 tok</td>
                <td>
                  <span class="badge badge-neutral">vector</span>
                </td>
                <td class="mono">10,000 ms</td>
                <td class="mono">15,000 ms</td>
                <td><span class="badge badge-neutral">timeout</span> <span class="badge badge-neutral">5xx</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- View 2: Provider Registry -->
      <div id="view-providers" class="view-content">
        <div class="section-header">
          <div>
            <h1 class="section-title">Provider Registry & Circuit Engine</h1>
            <p class="section-desc">Upstream AI infrastructure connectivity, sliding window health metrics, and failure trip ratios.</p>
          </div>
          <div class="toolbar-actions">
            <button class="btn" onclick="alert('Running upstream health probes...')">Probe All Providers</button>
          </div>
        </div>

        <div class="grid-3">
          <div class="card">
            <div class="card-title">
              <span>OpenAI Upstream</span>
              <span class="badge badge-ok">CIRCUIT CLOSED</span>
            </div>
            <p class="card-desc">api.openai.com &middot; HTTP/2 connection pool</p>
            <div class="drawer-kv"><span class="key">Rolling EWMA Latency</span><span class="val">218 ms</span></div>
            <div class="drawer-kv"><span class="key">Failure Ratio (30s window)</span><span class="val">0.00%</span></div>
            <div class="drawer-kv"><span class="key">Consecutive Errors</span><span class="val">0 / 10 min</span></div>
            <div class="drawer-kv"><span class="key">Credential Handle</span><span class="val">$OPENAI_API_KEY</span></div>
          </div>
          <div class="card">
            <div class="card-title">
              <span>Anthropic Upstream</span>
              <span class="badge badge-ok">CIRCUIT CLOSED</span>
            </div>
            <p class="card-desc">api.anthropic.com &middot; Raw Messages wire translation</p>
            <div class="drawer-kv"><span class="key">Rolling EWMA Latency</span><span class="val">342 ms</span></div>
            <div class="drawer-kv"><span class="key">Failure Ratio (30s window)</span><span class="val">0.00%</span></div>
            <div class="drawer-kv"><span class="key">Consecutive Errors</span><span class="val">0 / 10 min</span></div>
            <div class="drawer-kv"><span class="key">Credential Handle</span><span class="val">$ANTHROPIC_API_KEY</span></div>
          </div>
          <div class="card">
            <div class="card-title">
              <span>Google Gemini</span>
              <span class="badge badge-ok">CIRCUIT CLOSED</span>
            </div>
            <p class="card-desc">generativelanguage.googleapis.com &middot; generateContent</p>
            <div class="drawer-kv"><span class="key">Rolling EWMA Latency</span><span class="val">185 ms</span></div>
            <div class="drawer-kv"><span class="key">Failure Ratio (30s window)</span><span class="val">0.00%</span></div>
            <div class="drawer-kv"><span class="key">Consecutive Errors</span><span class="val">0 / 10 min</span></div>
            <div class="drawer-kv"><span class="key">Credential Handle</span><span class="val">$GEMINI_API_KEY</span></div>
          </div>
        </div>

        <div class="table-container">
          <table class="dense-table">
            <thead>
              <tr>
                <th>Adapter Type</th>
                <th>Registry Name</th>
                <th>Base URL</th>
                <th>Timeout Setting</th>
                <th>Circuit Breaker Window</th>
                <th>Failure Threshold</th>
                <th>Cooldown Recovery</th>
                <th>State</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="mono">openai</td>
                <td><strong>openai-primary</strong></td>
                <td class="mono">https://api.openai.com/v1</td>
                <td class="mono">30,000 ms</td>
                <td class="mono">30.0 s (min 10 req)</td>
                <td class="mono">50.0%</td>
                <td class="mono">15.0 s</td>
                <td><span class="badge badge-ok">CLOSED</span></td>
              </tr>
              <tr>
                <td class="mono">anthropic</td>
                <td><strong>anthropic-core</strong></td>
                <td class="mono">https://api.anthropic.com</td>
                <td class="mono">30,000 ms</td>
                <td class="mono">30.0 s (min 10 req)</td>
                <td class="mono">50.0%</td>
                <td class="mono">15.0 s</td>
                <td><span class="badge badge-ok">CLOSED</span></td>
              </tr>
              <tr>
                <td class="mono">gemini</td>
                <td><strong>gemini-flash</strong></td>
                <td class="mono">https://generativelanguage.googleapis.com/v1beta</td>
                <td class="mono">30,000 ms</td>
                <td class="mono">30.0 s (min 10 req)</td>
                <td class="mono">50.0%</td>
                <td class="mono">15.0 s</td>
                <td><span class="badge badge-ok">CLOSED</span></td>
              </tr>
              <tr>
                <td class="mono">ollama</td>
                <td><strong>ollama-local</strong></td>
                <td class="mono">http://localhost:11434</td>
                <td class="mono">60,000 ms</td>
                <td class="mono">30.0 s (min 10 req)</td>
                <td class="mono">50.0%</td>
                <td class="mono">15.0 s</td>
                <td><span class="badge badge-ok">CLOSED</span></td>
              </tr>
              <tr>
                <td class="mono">mock</td>
                <td><strong>mock-resilience</strong></td>
                <td class="mono">in-process scriptable</td>
                <td class="mono">10,000 ms</td>
                <td class="mono">30.0 s (min 10 req)</td>
                <td class="mono">50.0%</td>
                <td class="mono">15.0 s</td>
                <td><span class="badge badge-ok">CLOSED</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- View 3: Governance & Quotas -->
      <div id="view-governance" class="view-content">
        <div class="section-header">
          <div>
            <h1 class="section-title">Governance, Tenant Scopes & Quotas</h1>
            <p class="section-desc">Hashed API keys (HMAC-SHA256), RPM/TPM token buckets, and hard/soft monthly budget enforcement.</p>
          </div>
          <div class="toolbar-actions">
            <button class="btn btn-burnt" onclick="alert('Creating new scoped API key...')">+ Provision Key</button>
          </div>
        </div>

        <div class="grid-2">
          <div class="card">
            <div class="card-title">Tenant Hierarchy & Project Budgets</div>
            <p class="card-desc">Usage aggregates grouped by month and project ID.</p>
            <div class="drawer-kv"><span class="key">Tenant 'Acme-Corp' (ID: t_91f4a)</span><span class="val">Project: Core-Backend</span></div>
            <div class="drawer-kv"><span class="key">Monthly Token Budget</span><span class="val">50,000,000 tok (Hard Cap)</span></div>
            <div class="drawer-kv"><span class="key">Consumed This Month</span><span class="val">14,291,040 tok (28.5%)</span></div>
            <div class="drawer-kv"><span class="key">Monthly Cost Cap</span><span class="val">$100.00 USD</span></div>
            <div class="drawer-kv"><span class="key">Current Accrued Cost</span><span class="val">$21.45 USD</span></div>
          </div>
          <div class="card">
            <div class="card-title">Rate Limiting Mechanics</div>
            <p class="card-desc">Atomic Redis Lua token bucket state.</p>
            <div class="drawer-kv"><span class="key">TPM Reservation Strategy</span><span class="val">Reserve &rarr; Reconcile</span></div>
            <div class="drawer-kv"><span class="key">Prompt Token Estimation</span><span class="val">Length/4 + max_tokens</span></div>
            <div class="drawer-kv"><span class="key">Settlement Precision</span><span class="val">Exact refund / deficit rollover</span></div>
            <div class="drawer-kv"><span class="key">Key Pepper Hash</span><span class="val">HMAC-SHA256 (Constant-time)</span></div>
          </div>
        </div>

        <div class="table-container">
          <table class="dense-table">
            <thead>
              <tr>
                <th>Key Handle (Prefix)</th>
                <th>Name</th>
                <th>Project Scope</th>
                <th>RPM Limit</th>
                <th>TPM Limit</th>
                <th>Allowed Model Aliases</th>
                <th>Expiry</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><span class="mono" style="font-weight:600">gk_a9c4e201bfa8</span></td>
                <td>Production Ingestion Engine</td>
                <td class="mono">Core-Backend</td>
                <td class="mono">1,200 req/m</td>
                <td class="mono">500,000 tok/m</td>
                <td><span class="badge badge-neutral">chat-default</span> <span class="badge badge-neutral">embed-default</span></td>
                <td class="mono">2027-12-31</td>
                <td><span class="badge badge-ok">ACTIVE</span></td>
              </tr>
              <tr>
                <td><span class="mono" style="font-weight:600">gk_bb41ef90981a</span></td>
                <td>Staging Agent Runner</td>
                <td class="mono">Agent-Platform</td>
                <td class="mono">300 req/m</td>
                <td class="mono">150,000 tok/m</td>
                <td><span class="badge badge-neutral">chat-fast</span> <span class="badge badge-neutral">chat-cheap</span></td>
                <td class="mono">2027-06-30</td>
                <td><span class="badge badge-ok">ACTIVE</span></td>
              </tr>
              <tr>
                <td><span class="mono" style="font-weight:600">gk_ee180c4412ab</span></td>
                <td>Dev Testbench Key</td>
                <td class="mono">Dev-Sandbox</td>
                <td class="mono">60 req/m</td>
                <td class="mono">50,000 tok/m</td>
                <td><span class="badge badge-neutral">ALL ALIASES</span></td>
                <td class="mono">Never</td>
                <td><span class="badge badge-ok">ACTIVE</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- View 4: Live Telemetry -->
      <div id="view-telemetry" class="view-content">
        <div class="section-header">
          <div>
            <h1 class="section-title">Execution Telemetry & Trace Feed</h1>
            <p class="section-desc">Per-request audit trail, TTFT measurements, provider duration, overhead latency, and settlement costs.</p>
          </div>
          <div class="toolbar-actions">
            <button class="btn" onclick="alert('Refreshing trace stream...')">Pause Stream</button>
            <button class="btn" onclick="alert('Flushing Redis Stream...')">Flush In-Process Sink</button>
          </div>
        </div>

        <div class="table-container">
          <table class="dense-table">
            <thead>
              <tr>
                <th>Request ID</th>
                <th>Timestamp</th>
                <th>Alias</th>
                <th>Target Provider &middot; Model</th>
                <th>Attempts</th>
                <th>TTFT</th>
                <th>Total Latency</th>
                <th>Overhead</th>
                <th>Tokens (P / C)</th>
                <th>Cost (USD)</th>
                <th>Cache</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="mono">req_88f9a2e1041c</td>
                <td class="mono">14:38:12.401</td>
                <td><strong class="mono">chat-default</strong></td>
                <td class="mono">gemini:gemini-1.5-flash</td>
                <td class="mono">1</td>
                <td class="mono">142 ms</td>
                <td class="mono">318 ms</td>
                <td class="mono">4.2 ms</td>
                <td class="mono">412 / 128</td>
                <td class="mono">$0.000148</td>
                <td><span class="badge badge-neutral">miss</span></td>
                <td><span class="badge badge-ok">200 OK</span></td>
              </tr>
              <tr>
                <td class="mono">req_77d10b9918ef</td>
                <td class="mono">14:38:10.129</td>
                <td><strong class="mono">chat-default</strong></td>
                <td class="mono">openai:gpt-4o-mini</td>
                <td class="mono">2 (failover)</td>
                <td class="mono">285 ms</td>
                <td class="mono">620 ms</td>
                <td class="mono">7.1 ms</td>
                <td class="mono">1,024 / 256</td>
                <td class="mono">$0.000412</td>
                <td><span class="badge badge-neutral">miss</span></td>
                <td><span class="badge badge-ok">200 OK</span></td>
              </tr>
              <tr>
                <td class="mono">req_66c2918844ba</td>
                <td class="mono">14:38:09.004</td>
                <td><strong class="mono">chat-fast</strong></td>
                <td class="mono">anthropic:claude-3-5-haiku</td>
                <td class="mono">1</td>
                <td class="mono">&mdash;</td>
                <td class="mono">12 ms</td>
                <td class="mono">2.1 ms</td>
                <td class="mono">340 / 84</td>
                <td class="mono">$0.000000</td>
                <td><span class="badge badge-ok">exact</span></td>
                <td><span class="badge badge-ok">200 OK</span></td>
              </tr>
              <tr>
                <td class="mono">req_55b018f4a123</td>
                <td class="mono">14:38:05.819</td>
                <td><strong class="mono">embed-default</strong></td>
                <td class="mono">openai:text-embedding-3-small</td>
                <td class="mono">1</td>
                <td class="mono">&mdash;</td>
                <td class="mono">94 ms</td>
                <td class="mono">1.8 ms</td>
                <td class="mono">128 / 0</td>
                <td class="mono">$0.000003</td>
                <td><span class="badge badge-neutral">miss</span></td>
                <td><span class="badge badge-ok">200 OK</span></td>
              </tr>
              <tr>
                <td class="mono">req_44a908129cbf</td>
                <td class="mono">14:37:59.214</td>
                <td><strong class="mono">chat-default</strong></td>
                <td class="mono">&mdash;</td>
                <td class="mono">0</td>
                <td class="mono">&mdash;</td>
                <td class="mono">3.4 ms</td>
                <td class="mono">3.4 ms</td>
                <td class="mono">0 / 0</td>
                <td class="mono">$0.000000</td>
                <td><span class="badge badge-neutral">&mdash;</span></td>
                <td><span class="badge badge-err">429 LIMIT</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- View 5: Cache Layer -->
      <div id="view-caching" class="view-content">
        <div class="section-header">
          <div>
            <h1 class="section-title">Multi-Tier Cache Topology</h1>
            <p class="section-desc">Exact cryptographic hash cache and embedding-assisted semantic cache with tenant isolation.</p>
          </div>
        </div>

        <div class="grid-2">
          <div class="card">
            <div class="card-title">Exact Response Cache</div>
            <p class="card-desc">SHA-256 canonical hash of normalized request parameters.</p>
            <div class="drawer-kv"><span class="key">Cache Store Backend</span><span class="val">Redis CacheStore / In-Memory</span></div>
            <div class="drawer-kv"><span class="key">Default TTL</span><span class="val">3600 seconds (1 hour)</span></div>
            <div class="drawer-kv"><span class="key">Tenant Partitioning</span><span class="val">Strict Isolated Namespaces</span></div>
            <div class="drawer-kv"><span class="key">Header Controls</span><span class="val">X-AgentBridge-Cache: exact|bypass</span></div>
          </div>
          <div class="card">
            <div class="card-title">Semantic Response Cache</div>
            <p class="card-desc">Cosine similarity gating on vector embeddings.</p>
            <div class="drawer-kv"><span class="key">Embedding Provider</span><span class="val">embed-default alias</span></div>
            <div class="drawer-kv"><span class="key">Similarity Threshold</span><span class="val">&ge; 0.95</span></div>
            <div class="drawer-kv"><span class="key">Reported Header</span><span class="val">X-AgentBridge-Cache-Similarity</span></div>
            <div class="drawer-kv"><span class="key">State Index</span><span class="val">Tenant-Isolated Vector Store</span></div>
          </div>
        </div>
      </div>

      <!-- View 6: System Topology -->
      <div id="view-system" class="view-content">
        <div class="section-header">
          <div>
            <h1 class="section-title">System Topology & Architecture</h1>
            <p class="section-desc">Unified control and data plane configuration parameters.</p>
          </div>
        </div>

        <div class="table-container" style="padding:16px;">
          <pre class="code-view">
# AgentBridge System Architecture Overview
Engine:             AgentBridge Core Pipeline (v1.0.0)
Process Protocol:   FastAPI + Uvicorn Asyncio Engine
Data Plane:         OpenAI-Compatible Wire Surface (/v1/chat/completions, /v1/embeddings, /v1/models)
Control Plane:      Role-Based Admin API (/admin/v1/...) with HMAC-hashed admin tokens
Router:             IntelligenceRouter (priority | weighted | cost-aware | latency-EWMA)
Executor:           AgentExecutionEngine (jittered backoff, circuit breaking, deadline caps)
Distributed State:  Redis 7 (Atomic Lua scripts, Redis Streams usage worker, Breaker state)
Storage of Truth:   PostgreSQL 16 / SQLite via SQLAlchemy 2.0 Async + Alembic Migrations
Telemetry Engine:   Prometheus Metrics (/metrics) + OpenTelemetry Spans (without prompt payloads)
          </pre>
        </div>
      </div>

    </main>
  </div>

  <script>
    // Tab switching logic
    document.querySelectorAll('.nav-item').forEach(link => {
      link.addEventListener('click', () => {
        document.querySelectorAll('.nav-item').forEach(l => l.classList.remove('active'));
        link.classList.add('active');
        const targetView = link.getAttribute('data-view');
        document.querySelectorAll('.view-content').forEach(view => {
          view.classList.remove('active');
        });
        const targetElement = document.getElementById('view-' + targetView);
        if (targetElement) {
          targetElement.classList.add('active');
        }
      });
    });
  </script>
</body>
</html>
"""


def render_console(
    *,
    providers: list[str] | None = None,
    aliases: list[str] | None = None,
) -> HTMLResponse:
    """Return the operations console HTML response populated with a lightweight live summary."""
    provider_names = providers or ["mock-primary", "mock-secondary"]
    alias_names = aliases or ["chat-default", "embed-default"]
    html = CONSOLE_HTML.replace("{{PROVIDER_COUNT}}", str(len(provider_names)))
    html = html.replace("{{ALIAS_COUNT}}", str(len(alias_names)))
    html = html.replace("{{PROVIDER_NAMES}}", ", ".join(provider_names))
    html = html.replace("{{ALIAS_NAMES}}", ", ".join(alias_names))
    return HTMLResponse(content=html, status_code=200)

