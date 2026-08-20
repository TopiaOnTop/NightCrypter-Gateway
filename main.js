document.addEventListener('DOMContentLoaded', async () => {
    const loader = document.getElementById('loader');
    const urlParams = new URLSearchParams(window.location.search);
    const selectedServerId = urlParams.get('id');

    const isLayer7Route = window.location.pathname.startsWith('/l7') || window.location.pathname.startsWith('/layer7') || urlParams.has('l7');
    const layer = isLayer7Route ? 'layer7' : 'layer4';

    try {
        const servers = await fetch('/api/servers').then(r => r.json());
        const serversLayer = servers[layer] || {};

        let selectedServer = null;
        let activeServerKey = null;

        if (selectedServerId) {
            for (const cat of Object.values(serversLayer)) {
                if (cat.servers) {
                    for (const [sKey, sVal] of Object.entries(cat.servers)) {
                        if (sKey.toLowerCase() === selectedServerId.toLowerCase() || sVal.name.toLowerCase() === selectedServerId.toLowerCase()) {
                            selectedServer = sVal;
                            activeServerKey = sKey;
                            break;
                        }
                    }
                }
                if (selectedServer) break;
            }
        }
        if (!selectedServer) {
            for (const cat of Object.values(serversLayer)) {
                for (const [sKey, sVal] of Object.entries(cat.servers || {})) {
                    selectedServer = sVal;
                    activeServerKey = sKey;
                    break;
                }
                if (selectedServer) break;
            }
        }
        if (!selectedServer) {
            selectedServer = isLayer7Route
                ? { name: 'FDCServer', ip: 'https://50.7.24.51/', ports: '443', bandwidth: '2M' }
                : { name: 'Vantiva', ip: '157.254.50.8', ports: '22 & 80', bandwidth: '400 Gbps' };
            activeServerKey = isLayer7Route ? 'FDCServer' : 'Vantiva';
        }

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

        const sid = activeServerKey;
        const chartRes = await fetch(`/api/${layer}/${sid}`).then(r => r.json()).catch(() => ({ bandwidth: Array(50).fill(0), packets: Array(50).fill(0) }));
        createChart({
            bandwidth: (chartRes.bandwidth || []).map(Number),
            packets: (chartRes.packets || []).map(Number)
        });

        if (typeof lucide !== 'undefined') lucide.createIcons();

        setInterval(() => updateChart(layer, sid), 1500);

    } catch(e) {
        console.error('main.js error:', e);
    } finally {
        if (loader) loader.classList.add('hidden');
    }
});
