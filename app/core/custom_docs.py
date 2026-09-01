"""
Custom UI/UX Styling for Swagger UI & Developer Dashboard Portal.
Provides a modern dark-mode glassmorphic interface for API testing and docs.
"""

from fastapi.responses import HTMLResponse

CUSTOM_SWAGGER_CSS = """
/* Modern Dark Glassmorphic Theme for Swagger UI */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-primary: #0b0f19;
    --bg-card: rgba(17, 24, 39, 0.75);
    --bg-card-hover: rgba(30, 41, 59, 0.85);
    --accent-indigo: #6366f1;
    --accent-indigo-hover: #4f46e5;
    --accent-emerald: #10b981;
    --accent-amber: #f59e0b;
    --accent-rose: #f43f5e;
    --accent-cyan: #06b6d4;
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
    --border-color: rgba(255, 255, 255, 0.08);
}

body {
    background: var(--bg-primary) !important;
    color: var(--text-main) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-image: 
        radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.12) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(16, 185, 129, 0.08) 0px, transparent 50%) !important;
    background-attachment: fixed !important;
}

.swagger-ui {
    font-family: 'Inter', sans-serif !important;
}

/* Header / Topbar */
.swagger-ui .topbar {
    background: rgba(15, 23, 42, 0.8) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border-bottom: 1px solid var(--border-color) !important;
    padding: 14px 24px !important;
}

.swagger-ui .topbar a {
    font-weight: 700 !important;
    font-size: 1.25rem !important;
    color: #fff !important;
    letter-spacing: -0.02em !important;
}

.swagger-ui .topbar .download-url-wrapper {
    display: flex !important;
    align-items: center !important;
}

.swagger-ui .topbar input[type=text] {
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
    background: rgba(15, 23, 42, 0.9) !important;
    color: var(--text-main) !important;
    padding: 8px 12px !important;
}

.swagger-ui .topbar .download-url-button {
    background: linear-gradient(135deg, var(--accent-indigo), #4338ca) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

/* Info Section */
.swagger-ui .info {
    margin: 32px 0 !important;
    padding: 24px !important;
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(16px) !important;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3) !important;
}

.swagger-ui .info .title {
    color: #fff !important;
    font-size: 2.2rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em !important;
    background: linear-gradient(135deg, #fff 30%, #a5b4fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.swagger-ui .info p, .swagger-ui .info li {
    color: var(--text-muted) !important;
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
}

.swagger-ui .info a {
    color: #818cf8 !important;
}

/* Scheme Container & Authorize button */
.swagger-ui .scheme-container {
    background: transparent !important;
    box-shadow: none !important;
    padding: 16px 0 !important;
    border-bottom: 1px solid var(--border-color) !important;
    margin-bottom: 24px !important;
}

.swagger-ui .btn.authorize {
    background: linear-gradient(135deg, var(--accent-emerald), #059669) !important;
    border: none !important;
    color: #fff !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 8px 20px !important;
    box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3) !important;
    transition: all 0.2s ease !important;
}

.swagger-ui .btn.authorize:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4) !important;
}

.swagger-ui .btn.authorize svg {
    fill: #fff !important;
}

/* Operations Blocks */
.swagger-ui .opblock-tag {
    border-bottom: 1px solid var(--border-color) !important;
    padding: 12px 0 !important;
    color: #fff !important;
    font-size: 1.3rem !important;
    font-weight: 700 !important;
}

.swagger-ui .opblock-tag small {
    color: var(--text-muted) !important;
    font-weight: 400 !important;
}

.swagger-ui .opblock {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
    margin-bottom: 14px !important;
    transition: all 0.2s ease !important;
    overflow: hidden !important;
}

.swagger-ui .opblock:hover {
    border-color: rgba(99, 102, 241, 0.3) !important;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3) !important;
}

.swagger-ui .opblock .opblock-summary {
    padding: 12px 18px !important;
    border-bottom: 1px solid transparent !important;
}

.swagger-ui .opblock .opblock-summary-method {
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    padding: 6px 14px !important;
    min-width: 70px !important;
    text-align: center !important;
    text-shadow: none !important;
}

/* Method Badges */
.swagger-ui .opblock-get { border-color: rgba(59, 130, 246, 0.3) !important; }
.swagger-ui .opblock-get .opblock-summary-method { background: #2563eb !important; color: #fff !important; }
.swagger-ui .opblock-get .opblock-summary { background: rgba(37, 99, 235, 0.05) !important; }

.swagger-ui .opblock-post { border-color: rgba(16, 185, 129, 0.3) !important; }
.swagger-ui .opblock-post .opblock-summary-method { background: #059669 !important; color: #fff !important; }
.swagger-ui .opblock-post .opblock-summary { background: rgba(5, 150, 105, 0.05) !important; }

.swagger-ui .opblock-put { border-color: rgba(245, 158, 11, 0.3) !important; }
.swagger-ui .opblock-put .opblock-summary-method { background: #d97706 !important; color: #fff !important; }
.swagger-ui .opblock-put .opblock-summary { background: rgba(217, 119, 6, 0.05) !important; }

.swagger-ui .opblock-delete { border-color: rgba(239, 68, 68, 0.3) !important; }
.swagger-ui .opblock-delete .opblock-summary-method { background: #dc2626 !important; color: #fff !important; }
.swagger-ui .opblock-delete .opblock-summary { background: rgba(220, 38, 38, 0.05) !important; }

.swagger-ui .opblock .opblock-summary-path {
    color: var(--text-main) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
}

.swagger-ui .opblock .opblock-summary-description {
    color: var(--text-muted) !important;
    font-size: 0.88rem !important;
}

/* Expanded Operation Section */
.swagger-ui .opblock-body {
    background: rgba(11, 15, 25, 0.6) !important;
    padding: 20px !important;
}

.swagger-ui .opblock-section-header {
    background: rgba(30, 41, 59, 0.5) !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
}

.swagger-ui .opblock-section-header h4 {
    color: #cbd5e1 !important;
}

.swagger-ui table thead tr th, .swagger-ui table thead tr td {
    color: var(--text-muted) !important;
    border-bottom: 1px solid var(--border-color) !important;
}

.swagger-ui .parameter__name {
    color: #60a5fa !important;
    font-family: 'JetBrains Mono', monospace !important;
}

.swagger-ui .parameter__type {
    color: var(--text-muted) !important;
    font-family: 'JetBrains Mono', monospace !important;
}

.swagger-ui input[type=text], .swagger-ui select, .swagger-ui textarea {
    background: rgba(15, 23, 42, 0.9) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
    color: #fff !important;
    padding: 8px 12px !important;
    font-family: 'JetBrains Mono', monospace !important;
}

.swagger-ui input[type=text]:focus, .swagger-ui select:focus, .swagger-ui textarea:focus {
    border-color: var(--accent-indigo) !important;
    outline: none !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25) !important;
}

/* Buttons inside operations */
.swagger-ui .btn {
    border-radius: 8px !important;
    font-weight: 600 !important;
    border: none !important;
}

.swagger-ui .btn.execute {
    background: linear-gradient(135deg, var(--accent-indigo), var(--accent-indigo-hover)) !important;
    color: #fff !important;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
}

.swagger-ui .btn.btn-clear {
    background: rgba(255, 255, 255, 0.08) !important;
    color: #cbd5e1 !important;
}

/* Response Section */
.swagger-ui .responses-table {
    color: var(--text-main) !important;
}

.swagger-ui .highlight-code pre {
    background: #020617 !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 10px !important;
    color: #38bdf8 !important;
    font-family: 'JetBrains Mono', monospace !important;
}

.swagger-ui microlight {
    font-family: 'JetBrains Mono', monospace !important;
}

.swagger-ui section.models {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 16px !important;
}

.swagger-ui section.models h4 {
    color: #fff !important;
}

/* Scrollbars */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: #0b0f19;
}
::-webkit-scrollbar-thumb {
    background: #334155;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #475569;
}
"""

LANDING_PAGE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stock Portfolio & Investment API — Developer Portal</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #07090e;
            --bg-card: rgba(15, 23, 42, 0.7);
            --bg-card-hover: rgba(30, 41, 59, 0.8);
            --accent-indigo: #6366f1;
            --accent-purple: #a855f7;
            --accent-emerald: #10b981;
            --accent-cyan: #06b6d4;
            --text-white: #f8fafc;
            --text-dim: #94a3b8;
            --border-glow: rgba(99, 102, 241, 0.2);
            --border-subtle: rgba(255, 255, 255, 0.08);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-dark);
            color: var(--text-white);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            background-image: 
                radial-gradient(circle at 15% 15%, rgba(99, 102, 241, 0.15) 0%, transparent 45%),
                radial-gradient(circle at 85% 85%, rgba(16, 185, 129, 0.1) 0%, transparent 45%);
            background-attachment: fixed;
            overflow-x: hidden;
        }

        /* Glassmorphism Navbar */
        nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1.2rem 2.5rem;
            background: rgba(11, 15, 25, 0.8);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--border-subtle);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
            text-decoration: none;
            color: var(--text-white);
        }

        .brand-icon {
            width: 40px;
            height: 40px;
            border-radius: 12px;
            background: linear-gradient(135deg, var(--accent-indigo), var(--accent-purple));
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.3rem;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
        }

        .brand-title {
            font-size: 1.15rem;
            font-weight: 700;
            letter-spacing: -0.02em;
        }

        .brand-subtitle {
            font-size: 0.75rem;
            color: var(--text-dim);
        }

        .nav-links {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 0.6rem 1.2rem;
            border-radius: 10px;
            font-size: 0.9rem;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            border: none;
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--accent-indigo), var(--accent-purple));
            color: white;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.35);
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.5);
        }

        .btn-secondary {
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-white);
            border: 1px solid var(--border-subtle);
        }

        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.1);
            border-color: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
        }

        /* Container */
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 3rem 1.5rem;
            flex: 1;
        }

        /* Hero Section */
        .hero {
            text-align: center;
            margin-bottom: 3.5rem;
            position: relative;
        }

        .badge-status {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 14px;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 30px;
            font-size: 0.82rem;
            font-weight: 600;
            color: var(--accent-emerald);
            margin-bottom: 1.5rem;
        }

        .pulse-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: var(--accent-emerald);
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
        }

        .hero h1 {
            font-size: 3.2rem;
            font-weight: 800;
            letter-spacing: -0.04em;
            line-height: 1.15;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #ffffff 20%, #a5b4fc 70%, #c084fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero p {
            font-size: 1.15rem;
            color: var(--text-dim);
            max-width: 680px;
            margin: 0 auto 2.2rem;
            line-height: 1.6;
        }

        .hero-actions {
            display: flex;
            justify-content: center;
            gap: 16px;
            flex-wrap: wrap;
        }

        /* Metric Cards Grid */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 1.5rem;
            margin-bottom: 3.5rem;
        }

        .metric-card {
            background: var(--bg-card);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-subtle);
            border-radius: 16px;
            padding: 1.5rem;
            transition: all 0.3s ease;
        }

        .metric-card:hover {
            transform: translateY(-4px);
            border-color: var(--border-glow);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3);
        }

        .metric-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.8rem;
        }

        .metric-title {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .metric-icon {
            font-size: 1.2rem;
            opacity: 0.8;
        }

        .metric-value {
            font-size: 1.7rem;
            font-weight: 700;
            color: var(--text-white);
            font-family: 'JetBrains Mono', monospace;
        }

        .metric-desc {
            font-size: 0.8rem;
            color: var(--accent-emerald);
            margin-top: 0.4rem;
        }

        /* Interactive API Playground Section */
        .playground-section {
            background: var(--bg-card);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-subtle);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 3.5rem;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
        }

        .section-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1.5rem;
            border-bottom: 1px solid var(--border-subtle);
            padding-bottom: 1rem;
        }

        .section-title {
            font-size: 1.3rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .endpoint-selector {
            display: flex;
            gap: 10px;
            margin-bottom: 1.2rem;
            flex-wrap: wrap;
        }

        .endpoint-tab {
            padding: 8px 16px;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border-subtle);
            color: var(--text-dim);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .endpoint-tab.active, .endpoint-tab:hover {
            background: rgba(99, 102, 241, 0.15);
            border-color: var(--accent-indigo);
            color: var(--text-white);
        }

        .console-box {
            background: #02050a;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 1.2rem;
            font-family: 'JetBrains Mono', monospace;
            position: relative;
        }

        .console-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            font-size: 0.8rem;
            color: var(--text-dim);
        }

        .console-method {
            padding: 4px 8px;
            border-radius: 4px;
            background: #2563eb;
            color: white;
            font-weight: 700;
            font-size: 0.75rem;
        }

        .console-url {
            color: var(--accent-cyan);
        }

        pre {
            color: #38bdf8;
            font-size: 0.9rem;
            line-height: 1.5;
            overflow-x: auto;
            white-space: pre-wrap;
            word-break: break-all;
        }

        /* Roadmap Section */
        .roadmap-card {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: 20px;
            padding: 2rem;
        }

        .roadmap-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.2rem;
            margin-top: 1.5rem;
        }

        .day-card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 1rem 1.2rem;
            display: flex;
            align-items: flex-start;
            gap: 12px;
        }

        .day-card.completed {
            background: rgba(16, 185, 129, 0.05);
            border-color: rgba(16, 185, 129, 0.3);
        }

        .day-badge {
            min-width: 28px;
            height: 28px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.8rem;
            font-weight: 700;
            background: rgba(255, 255, 255, 0.1);
            color: var(--text-dim);
        }

        .day-card.completed .day-badge {
            background: var(--accent-emerald);
            color: white;
        }

        .day-info h4 {
            font-size: 0.95rem;
            margin-bottom: 2px;
        }

        .day-info p {
            font-size: 0.8rem;
            color: var(--text-dim);
        }

        /* Footer */
        footer {
            text-align: center;
            padding: 2rem;
            border-top: 1px solid var(--border-subtle);
            color: var(--text-dim);
            font-size: 0.85rem;
            margin-top: auto;
        }

        footer a {
            color: var(--accent-indigo);
            text-decoration: none;
        }
    </style>
</head>
<body>

    <!-- Navbar -->
    <nav>
        <a href="/" class="brand">
            <div class="brand-icon">📈</div>
            <div>
                <div class="brand-title">Stock Portfolio API</div>
                <div class="brand-subtitle">ZyoraByte Internship Project</div>
            </div>
        </a>
        <div class="nav-links">
            <a href="/docs" class="btn btn-primary">⚡ Swagger Docs</a>
            <a href="/redoc" class="btn btn-secondary">📖 ReDoc</a>
        </div>
    </nav>

    <!-- Main Content -->
    <div class="container">

        <!-- Hero Section -->
        <section class="hero">
            <div class="badge-status">
                <span class="pulse-dot"></span>
                API Operational & Live
            </div>
            <h1>Stock Portfolio & Investment<br>Management API</h1>
            <p>A production-grade FinTech backend platform built with FastAPI, PostgreSQL, SQLAlchemy 2.0, Pydantic v2, and JWT security.</p>
            <div class="hero-actions">
                <a href="/docs" class="btn btn-primary" style="padding: 0.8rem 1.8rem; font-size: 1rem;">
                    🚀 Open Interactive API Docs (/docs)
                </a>
                <a href="/health" target="_blank" class="btn btn-secondary" style="padding: 0.8rem 1.8rem; font-size: 1rem;">
                    🔍 Raw Health Endpoint (/health)
                </a>
            </div>
        </section>

        <!-- Metrics Grid -->
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-title">System Status</span>
                    <span class="metric-icon">🟢</span>
                </div>
                <div class="metric-value">Healthy</div>
                <div class="metric-desc">All core services online</div>
            </div>

            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-title">Framework</span>
                    <span class="metric-icon">⚡</span>
                </div>
                <div class="metric-value">FastAPI</div>
                <div class="metric-desc">Python 3.13 + Uvicorn</div>
            </div>

            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-title">Environment</span>
                    <span class="metric-icon">🛠️</span>
                </div>
                <div class="metric-value">Development</div>
                <div class="metric-desc">Debug mode enabled</div>
            </div>

            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-title">Roadmap Progress</span>
                    <span class="metric-icon">🏆</span>
                </div>
                <div class="metric-value">Day 1</div>
                <div class="metric-desc">Core setup & routing ready</div>
            </div>
        </div>

        <!-- Interactive Playground -->
        <section class="playground-section">
            <div class="section-header">
                <div class="section-title">
                    <span>🧪</span> Live API Sandbox Console
                </div>
                <button class="btn btn-primary" onclick="testEndpoint()" id="run-btn">
                    ▶️ Run Test Request
                </button>
            </div>

            <div class="endpoint-selector">
                <button class="endpoint-tab active" onclick="selectEndpoint('/health', this)">GET /health</button>
                <button class="endpoint-tab" onclick="selectEndpoint('/', this)">GET / (JSON)</button>
            </div>

            <div class="console-box">
                <div class="console-header">
                    <div>
                        <span class="console-method">GET</span>
                        <span class="console-url" id="target-url">http://127.0.0.1:8000/health</span>
                    </div>
                    <div id="latency-tag" style="color: var(--accent-emerald);">Response: 200 OK</div>
                </div>
                <pre id="json-output">Click 'Run Test Request' to test live API response...</pre>
            </div>
        </section>

        <!-- 15-Day Roadmap Timeline -->
        <section class="roadmap-card">
            <div class="section-title">
                <span>🗓️</span> 15-Day FinTech Roadmap Progress
            </div>
            <div class="roadmap-grid">
                <div class="day-card completed">
                    <div class="day-badge">✓</div>
                    <div class="day-info">
                        <h4>Day 1: Core Setup & Routing</h4>
                        <p>FastAPI boilerplate, CORS, exception handlers, health checks.</p>
                    </div>
                </div>

                <div class="day-card">
                    <div class="day-badge">2</div>
                    <div class="day-info">
                        <h4>Day 2: PostgreSQL & DB Setup</h4>
                        <p>Async SQLAlchemy 2.0, Alembic migrations & User model.</p>
                    </div>
                </div>

                <div class="day-card">
                    <div class="day-badge">3</div>
                    <div class="day-info">
                        <h4>Day 3: Authentication</h4>
                        <p>Bcrypt password hashing, JWT register & login endpoints.</p>
                    </div>
                </div>

                <div class="day-card">
                    <div class="day-badge">4</div>
                    <div class="day-info">
                        <h4>Day 4: Portfolios Management</h4>
                        <p>Portfolio CRUD operations, currency handling & user ownership.</p>
                    </div>
                </div>

                <div class="day-card">
                    <div class="day-badge">5</div>
                    <div class="day-info">
                        <h4>Day 5-9: Stock Market Data</h4>
                        <p>Buy/Sell transactions, holdings calculations & live market data.</p>
                    </div>
                </div>

                <div class="day-card">
                    <div class="day-badge">6</div>
                    <div class="day-info">
                        <h4>Day 10-15: Testing & Docker</h4>
                        <p>Watchlists, price alerts, pytest suite, Docker containerization.</p>
                    </div>
                </div>
            </div>
        </section>

    </div>

    <!-- Footer -->
    <footer>
        <p>Built with ❤️ for ZyoraByte FinTech Internship | Powered by <a href="https://fastapi.tiangolo.com" target="_blank">FastAPI</a> & Python 3.13</p>
    </footer>

    <script>
        let currentEndpoint = '/health';

        function selectEndpoint(path, el) {
            currentEndpoint = path;
            document.querySelectorAll('.endpoint-tab').forEach(tab => tab.classList.remove('active'));
            el.classList.add('active');
            document.getElementById('target-url').innerText = window.location.origin + path;
        }

        async function testEndpoint() {
            const outputEl = document.getElementById('json-output');
            const latencyEl = document.getElementById('latency-tag');
            const runBtn = document.getElementById('run-btn');

            outputEl.innerText = "Fetching live response...";
            runBtn.disabled = true;

            const startTime = performance.now();
            try {
                const response = await fetch(currentEndpoint, {
                    headers: { 'Accept': 'application/json' }
                });
                const duration = Math.round(performance.now() - startTime);
                const data = await response.json();

                latencyEl.innerText = `Response: ${response.status} OK (${duration}ms)`;
                latencyEl.style.color = '#10b981';
                outputEl.innerText = JSON.stringify(data, null, 2);
            } catch (err) {
                latencyEl.innerText = `Error connecting to API`;
                latencyEl.style.color = '#f43f5e';
                outputEl.innerText = "// Error: Could not connect to API server.\n" + err;
            } finally {
                runBtn.disabled = false;
            }
        }

        // Run auto-test on load
        window.addEventListener('DOMContentLoaded', testEndpoint);
    </script>
</body>
</html>
"""

def get_custom_swagger_ui_html(openapi_url: str, title: str):
    """
    Returns custom styled Swagger UI HTML page with glassmorphism dark theme.
    """
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
    <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">
    <title>{title}</title>
    <style>
    {CUSTOM_SWAGGER_CSS}
    </style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
        const ui = SwaggerUIBundle({{
            url: '{openapi_url}',
            dom_id: '#swagger-ui',
            presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIBundle.SwaggerUIStandalonePreset
            ],
            layout: "BaseLayout",
            deepLinking: true,
            showExtensions: true,
            showCommonExtensions: true,
            syntaxHighlight: {{ theme: "obsidian" }},
            docExpansion: "list",
            filter: true,
            displayRequestDuration: true
        }});
    </script>
</body>
</html>
"""
    return HTMLResponse(content=html_content, status_code=200)

def get_developer_dashboard_html():
    """
    Returns the modern developer landing page HTML.
    """
    return HTMLResponse(content=LANDING_PAGE_HTML, status_code=200)
