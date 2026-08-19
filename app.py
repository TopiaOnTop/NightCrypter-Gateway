import random
import time
import re
import secrets
import os
import requests
from flask import Flask, send_from_directory, jsonify, request, redirect, render_template_string
from flask_cors import CORS

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Stockage pour le calcul réel des RPS L7 (différence entre deux lectures)
# Structure: { server_name: {"last_requests": int, "last_time": float, "history_rps": list} }
l7_metrics_cache = {}

# Admin configuration
ADMIN_PASSWORD = "topiatheking"

# Dynamic Boom tracker pour Layer 4 et Layer 7
# Structure L4: { server_name_lower: { "format": int (1 or 2), "bps": float, "pps": float, "start_time": float } }
active_booms = {}

# Structure L7: { server_name_lower: { "format": int (1 or 2), "rps": float, "bps": float, "start_time": float } }
active_booms_l7 = {}

# API Tokens storage
# Structure: [ {"id": str, "name": str, "token": str, "created_at": float, "usage_count": int, "usage_logs": [ {"timestamp": float, "endpoint": str, "ip": str} ]} ]
API_TOKENS = [
    {
        "id": "tok_default_1",
        "name": "Primary Admin Integration Key",
        "token": "dstat_tok_7a9f201b4e82c910382f1b4092e18",
        "created_at": time.time() - 86400 * 10,
        "usage_count": 0,
        "usage_logs": []
    }
]

def authenticate_request():
    auth_header = request.headers.get('X-Admin-Password', '') or request.headers.get('Authorization', '')
    token_header = request.headers.get('X-API-Token', '') or request.args.get('api_token', '')

    if auth_header == ADMIN_PASSWORD or request.get_json(silent=True, force=True) and (request.get_json(silent=True) or {}).get('password') == ADMIN_PASSWORD:
        return True, "admin"

    if token_header:
        tok_obj = next((t for t in API_TOKENS if t["token"] == token_header), None)
        if tok_obj:
            tok_obj["usage_count"] += 1
            client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            tok_obj["usage_logs"].append({
                "timestamp": time.time(),
                "endpoint": request.path,
                "ip": client_ip
            })
            return True, tok_obj["name"]

    return False, None

# Banners and Ads Analytics storage
# Structure BANNERS: [ {"id": str, "img": str, "url": str, "report_id": str, "created_at": float} ]
# Structure BANNER_ANALYTICS: { report_id: { "banner_id": str, "clicks": [ {"timestamp": float, "ip": str, "user_agent": str} ], "impressions": int } }
BANNERS = [
    {
        "id": "ban_ethone",
        "img": "/assets/ethone-gif.gif",
        "url": "https://ethone.net/",
        "report_id": "rep_ethone_9f83a271b8492041238a11bc",
        "created_at": time.time() - 86400 * 5
    },
    {
        "id": "ban_reverb",
        "img": "/reverb.gif",
        "url": "https://t.me/reverbredirect",
        "report_id": "rep_reverb_77c191a84b019a33827104f1",
        "created_at": time.time() - 86400 * 3
    },
    {
        "id": "ban_vahn",
        "img": "/vahn.gif",
        "url": "https://t.me/vahnredirectt",
        "report_id": "rep_vahn_33b8a10f918e774219a5812e",
        "created_at": time.time() - 86400 * 2
    },
    {
        "id": "ban_ratelimit",
        "img": "/ratelimit.gif",
        "url": "https://ratelimit.org/",
        "report_id": "rep_ratelimit_55e2d19488a01129bc99214a",
        "created_at": time.time() - 86400
    }
]

BANNER_ANALYTICS = {}
# Initialize mock analytics history for default banners
for b in BANNERS:
    rep_id = b["report_id"]
    now = time.time()
    clicks_list = []
    # Generate mock clicks over past 7 days for rich analytics
    for i in range(random.randint(45, 120)):
        click_time = now - random.uniform(0, 86400 * 7)
        clicks_list.append({
            "timestamp": click_time,
            "ip": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
    clicks_list.sort(key=lambda x: x["timestamp"])
    BANNER_ANALYTICS[rep_id] = {
        "banner_id": b["id"],
        "clicks": clicks_list,
        "impressions": len(clicks_list) * random.randint(15, 30)
    }

# Dynamic Reviews storage
REVIEWS_DATA = [
    {
        "id": "1",
        "name": "Ethone Botnet",
        "description": "Best L4/L7 Stresser - Up to 5.3 Tb/s and over 10M rq/s",
        "url": "https://ethone.net/",
        "layer4": 5,
        "layer7": 5,
        "status": "leader"
    }
]

SERVERS_DATA = {
    "layer4": {
        "massive": {
            "category_name": "Massive",
            "servers": {
                "Vantiva": {
                    "name": "Vantiva",
                    "flag": "https://flagcdn.com/w20/us.png",
                    "number": "01",
                    "ip": "157.254.50.8",
                    "port": "9101",
                    "ports": "22 & 80",
                    "bandwidth": "400 Gbps",
                    "location": "US"
                },
                "GTT": {
                    "name": "GTT",
                    "flag": "https://flagcdn.com/w20/us.png",
                    "number": "02",
                    "ip": "66.92.198.194",
                    "port": "9100",
                    "ports": "22 & 80",
                    "bandwidth": "200 Gbps",
                    "location": "US"
                },
                "Latitude": {
                    "name": "Latitude",
                    "flag": "https://flagcdn.com/w20/us.png",
                    "number": "03",
                    "ip": "152.236.23.38",
                    "port": "9100",
                    "ports": "22 & 53",
                    "bandwidth": "100 Gbps",
                    "location": "US"
                },
                "Stelia": {
                    "name": "Stelia",
                    "flag": "https://flagcdn.com/w20/us.png",
                    "number": "04",
                    "ip": "185.165.50.30",
                    "port": "9100",
                    "ports": "22 & 80",
                    "bandwidth": "100 Gbps",
                    "location": "US"
                }
            }
        },
        "protected": {
            "category_name": "Protected",
            "servers": {
                "OVH": {
                    "name": "OVH",
                    "flag": "https://flagcdn.com/w20/fr.png",
                    "number": "03",
                    "ip": "51.89.25.195",
                    "port": "9100",
                    "ports": "22 & 53",
                    "bandwidth": "50 Gbps",
                    "location": "FR"
                }
            }
        },
        "non-protected": {
            "category_name": "Non Protected",
            "servers": {
                "Lumen": {
                    "name": "Lumen",
                    "flag": "https://flagcdn.com/w20/us.png",
                    "number": "01",
                    "ip": "216.202.170.56",
                    "port": "9100",
                    "ports": "22 & 53",
                    "bandwidth": "50 Gbps",
                    "location": "USA"
                },
                "GlobalNet": {
                    "name": "GlobalNet",
                    "flag": "https://flagcdn.com/w20/nl.png",
                    "number": "02",
                    "ip": "95.161.128.10",
                    "port": "9100",
                    "ports": "22 & 53",
                    "bandwidth": "400 Gbps",
                    "location": "NL"
                }
            }
        }
    },
    "layer7": {
        "massive": {
            "category_name": "L7 Massive",
            "servers": {
                "FDCServer": {
                    "name": "FDCServer",
                    "flag": "https://flagcdn.com/w20/us.png",
                    "number": "01",
                    "ip": "https://50.7.24.51/",
                    "port": "443",
                    "ports": "443",
                    "bandwidth": "2M",
                    "location": "USA",
                    "nginx_status": "http://50.7.24.51/nginx_status",
                    "bypass_url": "/api/nginx-status/50.7.24.51"
                }
            }
        },
        "protected": {
            "category_name": "L7 Protected",
            "servers": {
                "CF [UAM]": {
                    "name": "CF [UAM]",
                    "flag": "https://flagcdn.com/w20/ca.png",
                    "number": "01",
                    "ip": "uam.nigglet.fun",
                    "port": "80",
                    "ports": "80 & 443",
                    "bandwidth": "250K",
                    "location": "Canada",
                    "nginx_status": "http://95.217.202.78/nginx_status",
                    "bypass_url": "/api/nginx-status/95.217.202.78"
                },
                "vShield": {
                    "name": "vShield",
                    "flag": "https://flagcdn.com/w20/ca.png",
                    "number": "02",
                    "ip": "graph.vshield.pro",
                    "port": "443",
                    "ports": "443",
                    "bandwidth": "500K",
                    "location": "Canada",
                    "nginx_status": "https://graph.vshield.pro/7VTnnXWvhdVeUC6q",
                    "bypass_url": "/api/nginx-status/graph.vshield.pro"
                }
            }
        }
    }
}

def find_server_info(server_name):
    target = server_name.lower()
    for layer in SERVERS_DATA.values():
        for cat in layer.values():
            for key, srv in cat["servers"].items():
                if key.lower() == target or srv["name"].lower() == target:
                    return srv
    return {
        "name": server_name,
        "flag": "https://flagcdn.com/w20/us.png",
        "number": "01",
        "ip": "127.0.0.1",
        "port": "80",
        "ports": "80 & 443",
        "bandwidth": "100 Gbps",
        "location": "US"
    }

# --- GESTION DES ROUTES FRONTEND (PAGES) ---
# Empêche les erreurs 404 lors de l'accès direct aux URLs du type /l4?id=GTT

@app.route('/')
@app.route('/l4')
@app.route('/l7')
@app.route('/layer4/<path:subpath>')
@app.route('/layer7/<path:subpath>')
def serve_frontend_routes(subpath=None):
    return send_from_directory('.', 'index.html')

@app.route('/a/d/m/i/n/panel')
def admin_panel_route():
    return send_from_directory('.', 'admin.html')

@app.route('/api/admin/verify', methods=['POST'])
def verify_admin_password():
    data = request.get_json(silent=True) or {}
    pwd = data.get('password', '')
    if pwd == ADMIN_PASSWORD:
        return jsonify({"status": "success", "message": "Authenticated"}), 200
    return jsonify({"status": "error", "message": "Invalid password"}), 401

# --- API ENDPOINTS ---

@app.route('/api/servers', methods=['GET'])
def get_servers():
    return jsonify(SERVERS_DATA)

# --- API BANNERS & ADS ANALYTICS ---

@app.route('/api/banners', methods=['GET'])
def get_banners():
    # Increment impression counters for all active banners on fetch
    for b in BANNERS:
        rep_id = b["report_id"]
        if rep_id in BANNER_ANALYTICS:
            BANNER_ANALYTICS[rep_id]["impressions"] += 1
    return jsonify(BANNERS)

@app.route('/api/banners', methods=['POST'])
def add_banner():
    auth_header = request.headers.get('X-Admin-Password', '')
    data = request.get_json(silent=True) or {}
    if auth_header != ADMIN_PASSWORD and data.get('password') != ADMIN_PASSWORD:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    img = data.get('img', '').strip()
    target_url = data.get('url', '').strip()

    if not img or not target_url:
        return jsonify({"status": "error", "message": "Image path/URL and target URL are required"}), 400

    banner_id = f"ban_{secrets.token_hex(6)}"
    report_id = f"rep_{secrets.token_hex(24)}"

    new_banner = {
        "id": banner_id,
        "img": img,
        "url": target_url,
        "report_id": report_id,
        "created_at": time.time()
    }
    BANNERS.append(new_banner)
    BANNER_ANALYTICS[report_id] = {
        "banner_id": banner_id,
        "clicks": [],
        "impressions": 0
    }
    return jsonify({"status": "success", "banner": new_banner}), 201

@app.route('/api/banners/<banner_id>', methods=['DELETE'])
def delete_banner(banner_id):
    auth_header = request.headers.get('X-Admin-Password', '')
    data = request.get_json(silent=True) or {}
    if auth_header != ADMIN_PASSWORD and data.get('password') != ADMIN_PASSWORD:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    global BANNERS
    banner_to_remove = next((b for b in BANNERS if b["id"] == banner_id), None)
    if banner_to_remove:
        rep_id = banner_to_remove["report_id"]
        BANNER_ANALYTICS.pop(rep_id, None)
        BANNERS = [b for b in BANNERS if b["id"] != banner_id]
        return jsonify({"status": "success", "message": "Banner deleted"}), 200
    return jsonify({"status": "error", "message": "Banner not found"}), 404

@app.route('/api/banners/click/<banner_id>', methods=['GET'])
def record_banner_click(banner_id):
    banner = next((b for b in BANNERS if b["id"] == banner_id), None)
    if not banner:
        return jsonify({"status": "error", "message": "Banner not found"}), 404

    rep_id = banner["report_id"]
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent', '')

    if rep_id in BANNER_ANALYTICS:
        BANNER_ANALYTICS[rep_id]["clicks"].append({
            "timestamp": time.time(),
            "ip": client_ip,
            "user_agent": user_agent
        })

    return redirect(banner["url"], code=302)

@app.route('/api/ads/reports/<report_id>', methods=['GET'])
def get_banner_analytics_api(report_id):
    analytics = BANNER_ANALYTICS.get(report_id)
    banner = next((b for b in BANNERS if b["report_id"] == report_id), None)

    if not analytics or not banner:
        return jsonify({"status": "error", "message": "Report or banner not found"}), 404

    clicks = analytics["clicks"]
    impressions = analytics["impressions"]
    total_clicks = len(clicks)
    ctr = round((total_clicks / impressions * 100), 2) if impressions > 0 else 0.0

    return jsonify({
        "banner": banner,
        "total_clicks": total_clicks,
        "impressions": impressions,
        "ctr": ctr,
        "clicks": clicks
    })

@app.route('/ads/reports/<report_id>', methods=['GET'])
def view_ads_report_page(report_id):
    banner = next((b for b in BANNERS if b["report_id"] == report_id), None)
    if not banner:
        return send_from_directory('.', 'index.html')

    report_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>dstat.topia - Banner Analytics Report</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com/">
    <link rel="preconnect" href="https://fonts.gstatic.com/" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com/"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://unpkg.com/lucide@1.31.0/dist/umd/lucide.js"></script>
    <style>
        body { font-family: 'Inter', sans-serif; background: #0A0B1A; color: #fff; min-height: 100vh; }
        .card { background: #0D0E23; border: 1px solid #374151; border-radius: 12px; padding: 24px; }
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-6xl mx-auto space-y-8">
        <!-- Header -->
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-gray-800 pb-5">
            <div class="flex items-center gap-3">
                <div class="p-3 bg-blue-500/10 border border-blue-500/30 rounded-xl text-blue-400">
                    <i data-lucide="line-chart" class="w-8 h-8"></i>
                </div>
                <div>
                    <h1 class="text-2xl font-bold">Interactive Banner Analytics</h1>
                    <p class="text-xs text-gray-400">Real-time performance metrics and click intelligence</p>
                </div>
            </div>
            <div class="flex items-center gap-2 text-xs bg-slate-900 border border-gray-800 px-3 py-1.5 rounded-lg">
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
                <span class="text-gray-300">Live Analytics Feed</span>
            </div>
        </div>

        <!-- Banner Info Card -->
        <div class="card flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="flex items-center gap-4">
                <div class="w-48 h-20 bg-slate-900 border border-gray-800 rounded-lg overflow-hidden flex items-center justify-center p-2">
                    <img id="reportImg" src="" class="max-w-full max-h-full object-contain" />
                </div>
                <div>
                    <h2 class="text-lg font-bold" id="reportBannerId">Banner ID</h2>
                    <a id="reportUrl" href="#" target="_blank" class="text-xs text-blue-400 underline block mt-1"></a>
                    <span class="text-xs text-gray-500 block mt-1" id="reportCreated"></span>
                </div>
            </div>
            <div class="flex items-center gap-2">
                <button onclick="location.reload()" class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs rounded-lg transition-colors flex items-center gap-2">
                    <i data-lucide="refresh-cw" class="w-4 h-4"></i> Refresh Data
                </button>
            </div>
        </div>

        <!-- Key Stats Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="card space-y-2">
                <div class="flex justify-between items-center text-gray-400 text-xs uppercase font-semibold">
                    <span>Total Clicks</span>
                    <i data-lucide="mouse-pointer-click" class="w-4 h-4 text-blue-400"></i>
                </div>
                <div class="text-3xl font-extrabold text-white" id="statClicks">0</div>
                <p class="text-xs text-emerald-400">Tracked unique link redirects</p>
            </div>
            <div class="card space-y-2">
                <div class="flex justify-between items-center text-gray-400 text-xs uppercase font-semibold">
                    <span>Total Impressions</span>
                    <i data-lucide="eye" class="w-4 h-4 text-purple-400"></i>
                </div>
                <div class="text-3xl font-extrabold text-white" id="statImpressions">0</div>
                <p class="text-xs text-purple-400">Banner view counts across site</p>
            </div>
            <div class="card space-y-2">
                <div class="flex justify-between items-center text-gray-400 text-xs uppercase font-semibold">
                    <span>Click-Through Rate (CTR)</span>
                    <i data-lucide="percent" class="w-4 h-4 text-amber-400"></i>
                </div>
                <div class="text-3xl font-extrabold text-white" id="statCtr">0.0%</div>
                <p class="text-xs text-amber-400">Conversion efficiency ratio</p>
            </div>
        </div>

        <!-- Interactive Chart Card -->
        <div class="card space-y-4">
            <div class="flex justify-between items-center border-b border-gray-800 pb-3">
                <h3 class="text-base font-bold flex items-center gap-2">
                    <i data-lucide="trending-up" class="w-5 h-5 text-blue-400"></i> Click Distribution Timeline
                </h3>
                <span class="text-xs text-gray-400">Past 7 Days Activity</span>
            </div>
            <div class="h-80 w-full">
                <canvas id="clicksChart"></canvas>
            </div>
        </div>

        <!-- Recent Click Logs -->
        <div class="card space-y-4">
            <h3 class="text-base font-bold flex items-center gap-2 border-b border-gray-800 pb-3">
                <i data-lucide="list" class="w-5 h-5 text-emerald-400"></i> Recent Click Logs
            </h3>
            <div class="overflow-x-auto">
                <table class="w-full text-left text-xs text-gray-300">
                    <thead class="bg-slate-900 text-gray-400 uppercase border-b border-gray-800">
                        <tr>
                            <th class="p-3">Timestamp</th>
                            <th class="p-3">IP Address</th>
                            <th class="p-3">User Agent</th>
                        </tr>
                    </thead>
                    <tbody id="clickLogsTable" class="divide-y divide-gray-800">
                        <!-- Populated dynamically -->
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        const reportId = '""" + report_id + """';
        document.addEventListener('DOMContentLoaded', async () => {
            if (typeof lucide !== 'undefined') lucide.createIcons();
            try {
                const res = await fetch('/api/ads/reports/' + reportId);
                const data = await res.json();
                if (data.banner) {
                    document.getElementById('reportImg').src = data.banner.img;
                    document.getElementById('reportBannerId').textContent = 'Banner ' + data.banner.id;
                    document.getElementById('reportUrl').href = data.banner.url;
                    document.getElementById('reportUrl').textContent = data.banner.url;
                    document.getElementById('reportCreated').textContent = 'Created: ' + new Date(data.banner.created_at * 1000).toLocaleString();

                    document.getElementById('statClicks').textContent = data.total_clicks;
                    document.getElementById('statImpressions').textContent = data.impressions;
                    document.getElementById('statCtr').textContent = data.ctr + '%';

                    renderChart(data.clicks);
                    renderLogs(data.clicks);
                }
            } catch(e) {
                console.error(e);
            }
        });

        function renderChart(clicks) {
            const daysMap = {};
            const now = new Date();
            for (let i = 6; i >= 0; i--) {
                const d = new Date(now);
                d.setDate(d.getDate() - i);
                const key = d.toISOString().split('T')[0];
                daysMap[key] = 0;
            }

            clicks.forEach(c => {
                const dayKey = new Date(c.timestamp * 1000).toISOString().split('T')[0];
                if (daysMap[dayKey] !== undefined) {
                    daysMap[dayKey]++;
                }
            });

            const labels = Object.keys(daysMap);
            const values = Object.values(daysMap);

            const ctx = document.getElementById('clicksChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Daily Banner Clicks',
                        data: values,
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.15)',
                        fill: true,
                        tension: 0.4,
                        borderWidth: 2,
                        pointBackgroundColor: '#60a5fa'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#9ca3af' } },
                        y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#9ca3af', precision: 0 } }
                    }
                }
            });
        }

        function renderLogs(clicks) {
            const table = document.getElementById('clickLogsTable');
            table.innerHTML = '';
            const recent = [...clicks].reverse().slice(0, 15);
            if (recent.length === 0) {
                table.innerHTML = '<tr><td colspan="3" class="p-4 text-center text-gray-500">No click logs recorded yet.</td></tr>';
                return;
            }
            recent.forEach(c => {
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-900/50 transition-colors';
                tr.innerHTML = `
                    <td class="p-3 text-blue-400 font-mono">${new Date(c.timestamp * 1000).toLocaleString()}</td>
                    <td class="p-3 font-mono text-emerald-400">${c.ip}</td>
                    <td class="p-3 text-gray-400 truncate max-w-xs">${c.user_agent}</td>
                `;
                table.appendChild(tr);
            });
        }
    </script>
</body>
</html>"""
    return render_template_string(report_html)

# API Reviews
@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    return jsonify(REVIEWS_DATA)

@app.route('/api/reviews', methods=['POST'])
def add_review():
    auth_header = request.headers.get('X-Admin-Password', '')
    data = request.get_json(silent=True) or {}
    if auth_header != ADMIN_PASSWORD and data.get('password') != ADMIN_PASSWORD:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    name = data.get('name', '').strip()
    description = data.get('description', '').strip()
    url = data.get('url', '').strip()
    try:
        layer4 = int(data.get('layer4', 5))
        layer7 = int(data.get('layer7', 5))
    except (ValueError, TypeError):
        layer4 = 5
        layer7 = 5

    status = data.get('status', 'verified').lower()
    if status not in ['leader', 'verified', 'scam']:
        status = 'verified'

    if not name or not url:
        return jsonify({"status": "error", "message": "Name and URL are required"}), 400

    new_review = {
        "id": str(int(time.time() * 1000)),
        "name": name,
        "description": description,
        "url": url,
        "layer4": max(1, min(5, layer4)),
        "layer7": max(1, min(5, layer7)),
        "status": status
    }
    REVIEWS_DATA.append(new_review)
    return jsonify({"status": "success", "review": new_review}), 201

@app.route('/api/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    auth_header = request.headers.get('X-Admin-Password', '')
    data = request.get_json(silent=True) or {}
    if auth_header != ADMIN_PASSWORD and data.get('password') != ADMIN_PASSWORD:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    global REVIEWS_DATA
    REVIEWS_DATA = [r for r in REVIEWS_DATA if r["id"] != review_id]
    return jsonify({"status": "success", "message": "Review deleted"}), 200

def parse_numeric_val(val, default=100.0):
    if isinstance(val, (int, float)):
        return float(val)
    if not val:
        return default
    s = str(val).strip().lower()
    m = re.match(r'^([\d\.]+)\s*([a-z]*)$', s)
    if not m:
        try:
            return float(s)
        except ValueError:
            return default
    num = float(m.group(1))
    unit = m.group(2)
    if unit in ['tbps', 'tb/s', 'tb']:
        return num * 1000.0
    elif unit in ['gbps', 'gb/s', 'gb']:
        return num
    elif unit in ['mbps', 'mb/s', 'mb']:
        return num / 1000.0
    elif unit in ['kbps', 'kb/s', 'kb']:
        return num / 1000000.0
    elif unit in ['mpps', 'm']:
        return num
    elif unit in ['kpps', 'k']:
        return num / 1000.0
    return num

# --- API TOKENS MANAGEMENT ---

@app.route('/api/tokens', methods=['GET'])
def get_api_tokens():
    auth_header = request.headers.get('X-Admin-Password', '')
    data = request.get_json(silent=True) or {}
    if auth_header != ADMIN_PASSWORD and data.get('password') != ADMIN_PASSWORD:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    return jsonify(API_TOKENS)

@app.route('/api/tokens', methods=['POST'])
def create_api_token():
    auth_header = request.headers.get('X-Admin-Password', '')
    data = request.get_json(silent=True) or {}
    if auth_header != ADMIN_PASSWORD and data.get('password') != ADMIN_PASSWORD:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    name = data.get('name', '').strip() or "Integration Token"
    token_key = f"dstat_tok_{secrets.token_hex(16)}"
    token_id = f"tok_{secrets.token_hex(6)}"

    new_token = {
        "id": token_id,
        "name": name,
        "token": token_key,
        "created_at": time.time(),
        "usage_count": 0,
        "usage_logs": []
    }
    API_TOKENS.append(new_token)
    return jsonify({"status": "success", "token": new_token}), 201

@app.route('/api/tokens/<token_id>', methods=['DELETE'])
def delete_api_token(token_id):
    auth_header = request.headers.get('X-Admin-Password', '')
    data = request.get_json(silent=True) or {}
    if auth_header != ADMIN_PASSWORD and data.get('password') != ADMIN_PASSWORD:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    global API_TOKENS
    API_TOKENS = [t for t in API_TOKENS if t["id"] != token_id]
    return jsonify({"status": "success", "message": "Token revoked"}), 200

@app.route('/api/tokens/<token_id>/analytics', methods=['GET'])
def get_token_analytics(token_id):
    auth_header = request.headers.get('X-Admin-Password', '')
    data = request.get_json(silent=True) or {}
    if auth_header != ADMIN_PASSWORD and data.get('password') != ADMIN_PASSWORD:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    tok = next((t for t in API_TOKENS if t["id"] == token_id), None)
    if not tok:
        return jsonify({"status": "error", "message": "Token not found"}), 404

    return jsonify({
        "id": tok["id"],
        "name": tok["name"],
        "usage_count": tok["usage_count"],
        "usage_logs": tok["usage_logs"]
    })

# API Boom / Reset (L4)
@app.route('/api/boom', methods=['POST'])
def trigger_boom_global():
    is_auth, actor = authenticate_request()
    if not is_auth:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    data = request.get_json(silent=True) or request.form or {}
    srv = data.get('server') or data.get('server_name')
    fmt = int(data.get('format', 2))
    bps = parse_numeric_val(data.get('bps') or data.get('bandwidth'), 100.0)
    pps = parse_numeric_val(data.get('pps') or data.get('packets'), 50.0)

    if srv:
        active_booms[srv.lower()] = {
            "format": fmt,
            "bps": bps,
            "pps": pps,
            "start_time": time.time()
        }
    else:
        for cat in SERVERS_DATA["layer4"].values():
            for key in cat["servers"].keys():
                active_booms[key.lower()] = {
                    "format": fmt,
                    "bps": bps,
                    "pps": pps,
                    "start_time": time.time()
                }
    return jsonify({"status": "success", "message": "BOOM L4 activé !"}), 200

@app.route('/api/reset', methods=['POST'])
def reset_boom_global():
    data = request.get_json(silent=True) or request.form or {}
    srv = data.get('server') or data.get('server_name')
    if srv:
        active_booms.pop(srv.lower(), None)
    else:
        active_booms.clear()
    return jsonify({"status": "success", "message": "BOOM désactivé."}), 200

@app.route('/api/boom/<server_name>', methods=['POST', 'GET'])
def trigger_boom_server(server_name):
    is_auth, actor = authenticate_request()
    if not is_auth:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    data = request.get_json(silent=True) or request.args or {}
    if request.method == 'POST' and request.is_json and request.get_json(silent=True):
        data = request.get_json(silent=True)
    fmt = int(data.get('format', 2))
    bps = parse_numeric_val(data.get('bps') or data.get('bandwidth'), 100.0)
    pps = parse_numeric_val(data.get('pps') or data.get('packets'), 50.0)

    active_booms[server_name.lower()] = {
        "format": fmt,
        "bps": bps,
        "pps": pps,
        "start_time": time.time()
    }
    return jsonify({"status": "success", "message": f"BOOM activé pour {server_name}"}), 200

@app.route('/api/reset/<server_name>', methods=['POST', 'GET'])
def reset_boom_server(server_name):
    active_booms.pop(server_name.lower(), None)
    active_booms_l7.pop(server_name.lower(), None)
    return jsonify({"status": "success", "message": f"Reset pour {server_name}"}), 200

# API Boom / Reset (L7)
def parse_rps_val(val, default=100000.0):
    if isinstance(val, (int, float)):
        return float(val)
    if not val:
        return default
    s = str(val).strip().lower()
    m = re.match(r'^([\d\.]+)\s*([a-z]*)$', s)
    if not m:
        try: return float(s)
        except ValueError: return default
    num = float(m.group(1))
    unit = m.group(2)
    if unit in ['m', 'mrps', 'm/s']:
        return num * 1000000.0
    elif unit in ['k', 'krps', 'k/s']:
        return num * 1000.0
    return num

@app.route('/api/boom/l7', methods=['POST'])
def trigger_boom_l7_global():
    is_auth, actor = authenticate_request()
    if not is_auth:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    data = request.get_json(silent=True) or request.form or {}
    srv = data.get('server') or data.get('server_name')
    fmt = int(data.get('format', 2))
    rps = parse_rps_val(data.get('rps') or data.get('requests'), 500000.0)

    if srv:
        active_booms_l7[srv.lower()] = {
            "format": fmt,
            "rps": rps,
            "start_time": time.time()
        }
    else:
        for cat in SERVERS_DATA["layer7"].values():
            for key in cat["servers"].keys():
                active_booms_l7[key.lower()] = {
                    "format": fmt,
                    "rps": rps,
                    "start_time": time.time()
                }
    return jsonify({"status": "success", "message": "BOOM L7 activé !"}), 200

@app.route('/api/reset/l7', methods=['POST'])
def reset_boom_l7_global():
    data = request.get_json(silent=True) or request.form or {}
    srv = data.get('server') or data.get('server_name')
    if srv:
        active_booms_l7.pop(srv.lower(), None)
    else:
        active_booms_l7.clear()
    return jsonify({"status": "success", "message": "BOOM L7 désactivé."}), 200

@app.route('/api/boom/l7/<server_name>', methods=['POST', 'GET'])
def trigger_boom_l7_server(server_name):
    is_auth, actor = authenticate_request()
    if not is_auth:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    data = request.get_json(silent=True) or request.args or {}
    if request.method == 'POST' and request.is_json and request.get_json(silent=True):
        data = request.get_json(silent=True)
    fmt = int(data.get('format', 2))
    rps = parse_rps_val(data.get('rps') or data.get('requests'), 500000.0)

    active_booms_l7[server_name.lower()] = {
        "format": fmt,
        "rps": rps,
        "start_time": time.time()
    }
    return jsonify({"status": "success", "message": f"BOOM L7 activé pour {server_name}"}), 200

@app.route('/api/reset/l7/<server_name>', methods=['POST', 'GET'])
def reset_boom_l7_server(server_name):
    active_booms_l7.pop(server_name.lower(), None)
    return jsonify({"status": "success", "message": f"Reset L7 pour {server_name}"}), 200

# API Layer 4 (Simulée & Polymorphe)
@app.route('/api/layer4/<server_name>', methods=['GET', 'POST'])
def get_layer4_metrics(server_name):
    srv_info = dict(find_server_info(server_name))
    boom_info = active_booms.get(server_name.lower())

    # Seed parameters based on server_name for baseline polymorphism
    name_hash = sum(ord(c) for c in server_name.lower())
    base_bw = 0.02 + (name_hash % 17) * 0.015
    base_pk = 0.003 + (name_hash % 11) * 0.002
    amplitude = 0.005 + (name_hash % 7) * 0.002

    bandwidth = [round(base_bw + random.uniform(-amplitude, amplitude), 3) for _ in range(40)]
    packets = [round(base_pk + random.uniform(-amplitude * 0.2, amplitude * 0.2), 3) for _ in range(40)]

    if boom_info:
        fmt = boom_info.get("format", 2)
        target_bps = boom_info.get("bps", 100.0)
        target_pps = boom_info.get("pps", 50.0)
        start_time = boom_info.get("start_time", time.time())

        is_zero_phase = False
        if fmt == 1:
            elapsed = time.time() - start_time
            cycle_pos = elapsed % 40.0
            if cycle_pos >= 20.0:
                is_zero_phase = True

        if is_zero_phase:
            bandwidth += [round(random.uniform(0.000, 0.001), 3) for _ in range(10)]
            packets += [round(random.uniform(0.000, 0.001), 3) for _ in range(10)]
        else:
            cur_bw_points = []
            cur_pk_points = []
            for _ in range(10):
                bw_val = target_bps * random.uniform(0.95, 1.05)
                pk_val = target_pps * random.uniform(0.95, 1.05)
                cur_bw_points.append(round(bw_val, 2))
                cur_pk_points.append(round(pk_val, 2))
            bandwidth += cur_bw_points
            packets += cur_pk_points

            if target_bps >= 1000:
                srv_info["bandwidth"] = f"{target_bps/1000:.1f} Tbps"
            else:
                srv_info["bandwidth"] = f"{target_bps:.1f} Gbps"
    else:
        bandwidth += [round(base_bw + random.uniform(-amplitude, amplitude), 3) for _ in range(10)]
        packets += [round(base_pk + random.uniform(-amplitude * 0.2, amplitude * 0.2), 3) for _ in range(10)]

    return jsonify({
        "bandwidth": bandwidth,
        "packets": packets,
        "server": srv_info
    })

# API Layer 7 (Calcul réel depuis Nginx Status + Injection Boom L7)
@app.route('/api/layer7/<server_name>', methods=['GET', 'POST'])
def get_layer7_metrics(server_name):
    srv_info = dict(find_server_info(server_name))
    boom_info = active_booms_l7.get(server_name.lower())

    status_url = srv_info.get("nginx_status")

    total_requests = 0
    raw_text = ""

    # Tentative d'extraire les métriques Nginx réelles
    if status_url:
        try:
            resp = requests.get(status_url, timeout=1.5)
            if resp.status_code == 200:
                raw_text = resp.text
        except Exception:
            pass

    # Extraction des données d'acceptation/requêtes Nginx (Ligne "server accepts handled requests")
    if raw_text:
        match = re.search(r'^\s*(\d+)\s+(\d+)\s+(\d+)', raw_text, re.MULTILINE)
        if match:
            total_requests = int(match.group(3))

    now = time.time()
    cache = l7_metrics_cache.get(server_name.lower())

    # Calcul dynamique du RPS instantané
    if cache and total_requests > 0:
        delta_req = total_requests - cache["last_requests"]
        delta_time = now - cache["last_time"]
        current_rps = max(0, round(delta_req / delta_time, 1)) if delta_time > 0 else 0
        cache["history_rps"].append(current_rps)
        if len(cache["history_rps"]) > 50:
            cache["history_rps"].pop(0)

        cache["last_requests"] = total_requests
        cache["last_time"] = now
    else:
        # Initialisation ou valeur par défaut si serveur injoignable
        initial_history = [round(random.uniform(15.0, 45.0), 1) for _ in range(50)]
        l7_metrics_cache[server_name.lower()] = {
            "last_requests": total_requests,
            "last_time": now,
            "history_rps": initial_history
        }

    history = list(l7_metrics_cache[server_name.lower()]["history_rps"])

    # Appliquer l'injection BOOM L7 si active
    if boom_info:
        fmt = boom_info.get("format", 2)
        target_rps = boom_info.get("rps", 500000.0)
        start_time = boom_info.get("start_time", time.time())

        is_zero_phase = False
        if fmt == 1:
            elapsed = time.time() - start_time
            cycle_pos = elapsed % 40.0
            if cycle_pos >= 20.0:
                is_zero_phase = True

        if is_zero_phase:
            history = [round(random.uniform(0.0, 1.0), 1) for _ in range(50)]
        else:
            cur_rps_points = [round(target_rps * random.uniform(0.95, 1.05), 1) for _ in range(50)]
            history = cur_rps_points

            if target_rps >= 1000000:
                srv_info["bandwidth"] = f"{target_rps/1000000:.1f}M RPS"
            elif target_rps >= 1000:
                srv_info["bandwidth"] = f"{target_rps/1000:.1f}K RPS"
            else:
                srv_info["bandwidth"] = f"{int(target_rps)} RPS"

    # Estimation du débit réseau basé sur le RPS
    bandwidth_history = [round(rps * 0.0012, 3) for rps in history]

    return jsonify({
        "requests": history,
        "bandwidth": history,  # graph chart uses bandwidth array for L7 RPS
        "server": srv_info
    })

# Proxy / Route Fallback pour Nginx status
@app.route('/api/nginx-status/<path:target>', methods=['GET'])
def get_nginx_status_proxy(target):
    # Si le frontend interroge ce bypass, on tente de réorienter ou d'envoyer un format stub standard
    active_conn = random.randint(10, 50)
    accepts = random.randint(50000, 100000)
    requests_cnt = accepts + random.randint(100, 1000)

    body = f"Active connections: {active_conn}\nserver accepts handled requests\n {accepts} {accepts} {requests_cnt}\nReading: 0 Writing: 1 Waiting: {active_conn - 1}\n"
    return body, 200, {'Content-Type': 'text/plain'}

# Capture toutes les autres routes non définies pour éviter les 404 du navigateur
@app.errorhandler(404)
def handle_404(e):
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)