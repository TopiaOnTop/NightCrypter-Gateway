
// Shadow/glow plugin for Chart.js
const glowPlugin = {
    id: 'glowPlugin',
    beforeDatasetsDraw(chart) {
        const ctx = chart.ctx;
        ctx.save();
        ctx.shadowBlur = 8;
        ctx.shadowColor = 'rgba(200,200,255,0.25)';
    },
    afterDatasetsDraw(chart) {
        chart.ctx.restore();
    }
};
let chart;

function createChart(data) {
    const ctx = document.createElement('canvas').getContext('2d');
    const chartContainer = document.getElementById('chart-container');
    chartContainer.innerHTML = '';
    const wrapper = document.createElement('div');
    wrapper.style.cssText = 'position:relative;width:100%;height:100%;';
    const watermark = document.createElement('div');
    watermark.textContent = 'dstat.topia';
    watermark.style.cssText = 'position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-size:48px;font-family:Bungee,cursive;font-weight:400;color:rgba(255,255,255,0.1);pointer-events:none;z-index:1;';
    wrapper.appendChild(ctx.canvas);
    wrapper.appendChild(watermark);
    chartContainer.appendChild(wrapper);

    const isL7 = window.location.pathname.includes('/l7');
    const bw = Array.isArray(data.bandwidth) ? data.bandwidth : Array(50).fill(0);
    const pk = Array.isArray(data.packets) ? data.packets : Array(50).fill(0);
    const maxVal = isL7 ? Math.max(...bw, 10) : Math.max(...bw, ...pk, 0.0001);
    const dynamicMax = maxVal * 1.3;

    const datasets = isL7 ? [
        { label: 'Requests Per Second', fill: true, borderColor: 'rgba(180,180,200,0.7)', tension: 0.5, backgroundColor: 'rgba(140,140,180,0.06)', data: bw }
    ] : [
        { label: 'Bandwidth', fill: true, borderColor: 'rgba(180,180,200,0.7)', tension: 0.5, backgroundColor: 'rgba(140,140,180,0.06)', data: bw },
        { label: 'Packets', fill: true, borderColor: 'rgba(180,180,200,0.7)', tension: 0.5, backgroundColor: 'rgba(140,140,180,0.06)', data: pk }
    ];

    chart = new Chart(ctx, {
        type: 'line',
        data: { labels: Array(bw.length).fill(''), datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            elements: { point: { radius: 0 } },
            interaction: { intersect: false },
            plugins: {
                legend: { display: false },
                tooltip: {
                    intersect: false,
                    callbacks: {
                        label: function(c) {
                            if (isL7) { const v = formatRps(c.parsed.y); return `RPS: ${v.value}${v.unit}`; }
                            const v = c.dataset.label === 'Bandwidth' ? formatBps(c.parsed.y) : formatPps(c.parsed.y);
                            return `${c.dataset.label}: ${v.value} ${v.unit}`;
                        }
                    },
                    backgroundColor: '#0D0F14', titleColor: '#fff', bodyColor: '#fff', borderRadius: 8
                }
            },
            scales: {
                x: { ticks: { display: false }, grid: { display: false } },
                y: {
                    beginAtZero: true, min: 0, max: dynamicMax,
                    ticks: { maxTicksLimit: 6, color: '#ccc', callback: v => { if(isL7){const r=formatRps(v);return r.value+r.unit;}const r=formatBps(v);return r.value+' '+r.unit; } },
                    grid: { display: false }
                }
            }
        }
    });
}

const _fl = { count: 0, last: -1 };
async function updateChart(layer, serverId) {
    try {
        const controller = new AbortController();
        const t = setTimeout(() => controller.abort(), 1500);
        const res = await fetch('/api/' + layer + '/' + serverId, { signal: controller.signal, cache: 'no-cache' });
        clearTimeout(t);
        const data = await res.json();
        const isL7 = layer === 'layer7';
        if (isL7) {
            const rps = parseFloat((data.bandwidth || [])[data.bandwidth.length - 1]) || 0;
            chart.data.datasets[0].data.shift();
            chart.data.datasets[0].data.push(rps);
            chart.options.scales.y.max = Math.max(...chart.data.datasets[0].data, 10) * 1.3;
        } else {
            let bw = parseFloat((data.bandwidth || [])[data.bandwidth.length - 1]) || 0;
            let pk = parseFloat((data.packets || [])[data.packets.length - 1]) || 0;

            // Flatline: if same non-zero value for 10 updates (~15s), crash to 0
            if (bw > 0 && Math.abs(bw - _fl.last) < 0.0001) {
                _fl.count++;
            } else {
                _fl.count = 0;
                _fl.last = bw;
            }
            if (_fl.count >= 10) { bw = 0; pk = 0; }

            // Flatline detection for bandwidth


            chart.data.datasets[0].data.shift(); chart.data.datasets[0].data.push(bw);
            chart.data.datasets[1].data.shift(); chart.data.datasets[1].data.push(pk);
            const max = Math.max(...chart.data.datasets[0].data, ...chart.data.datasets[1].data, 0.0001);
            chart.options.scales.y.max = max * 1.3;
        }
        chart.update();
    } catch(e) {
        chart.data.datasets.forEach(ds => { ds.data.shift(); ds.data.push(0); });
        chart.update();
    }
}

function formatBps(v) {
    return v >= 1000 ? { value: (v/1000).toFixed(2), unit: 'Tb/s' } :
           v >= 1 ? { value: v.toFixed(2), unit: 'Gb/s' } :
           v >= 0.001 ? { value: (v*1000).toFixed(2), unit: 'Mb/s' } :
           { value: (v*1000000).toFixed(2), unit: 'Kb/s' };
}

function formatPps(v) {
    return v >= 1000 ? { value: (v/1000).toFixed(2), unit: 'BPPS' } :
           v >= 1 ? { value: v.toFixed(2), unit: 'MPPS' } :
           v >= 0.001 ? { value: (v*1000).toFixed(2), unit: 'kPPS' } :
           { value: (v*1000000).toFixed(2), unit: 'PPS' };
}

function formatRps(v) {
    if (v <= 0) return { value: '0', unit: ' RPS' };
    return v >= 1000000 ? { value: (v/1000000).toFixed(1), unit: 'M RPS' } :
           v >= 1000 ? { value: (v/1000).toFixed(1), unit: 'K RPS' } :
           { value: v.toFixed(0), unit: ' RPS' };
}
