document.addEventListener('DOMContentLoaded', async () => {
    const loader = document.getElementById('loader');
    const urlParams = new URLSearchParams(window.location.search);
    const selectedServerId = urlParams.get('id');
    const layer = 'layer4';

    try {
        const servers = await fetch('/api/servers').then(r => r.json());
        const serversLayer = servers[layer] || {};

        let selectedServer = null;
        if (selectedServerId) {
            for (const cat of Object.values(serversLayer)) {
                if (cat.servers && cat.servers[selectedServerId]) {
                    selectedServer = cat.servers[selectedServerId]; break;
                }
            }
        }
        if (!selectedServer) {
            for (const cat of Object.values(serversLayer)) {
                for (const srv of Object.values(cat.servers || {})) {
                    selectedServer = srv; break;
                }
                if (selectedServer) break;
            }
        }
        if (!selectedServer) selectedServer = { name: 'Unknown', ip: '0.0.0.0', ports: '22 & 53', bandwidth: '0 Gbps' };

        renderGraphDetails(selectedServer);
        renderServers(servers, layer);

        document.querySelectorAll('.layer-button').forEach(function(btn) {
            btn.addEventListener('click', function() {
                var c = btn.nextElementSibling;
                var i = btn.querySelector('.rotate-icon');
                var o = c.style.maxHeight && c.style.maxHeight !== '0px';
                c.style.maxHeight = o ? '0px' : '600px';
                c.style.opacity = o ? '0' : '1';
                if(i) i.classList.toggle('open');
            });
        });
        document.querySelectorAll('.category-button').forEach(function(btn) {
            btn.addEventListener('click', function() {
                var c = btn.nextElementSibling;
                var i = btn.querySelector('.rotate-icon');
                var o = c.style.maxHeight && c.style.maxHeight !== '0px';
                c.style.maxHeight = o ? '0px' : '600px';
                c.style.opacity = o ? '0' : '1';
                if(i) i.classList.toggle('open');
            });
        });

        const sid = selectedServerId || Object.keys((Object.values(serversLayer)[0] || {}).servers || {})[0] || 'gcore';
        const chartRes = await fetch(`/api/layer4/${sid}`).then(r => r.json()).catch(() => ({ bandwidth: Array(50).fill(0), packets: Array(50).fill(0) }));
        createChart({
            bandwidth: (chartRes.bandwidth || []).map(Number),
            packets: (chartRes.packets || []).map(Number)
        });

        if (typeof lucide !== 'undefined') lucide.createIcons();

        setInterval(() => updateChart('layer4', sid), 1500);

    } catch(e) {
        console.error('main.js error:', e);
    } finally {
        if (loader) loader.classList.add('hidden');
    }
});
