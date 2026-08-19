function renderServers(servers, currentLayer) {
    const nav = document.getElementById('servers-nav');
    if (!nav) return;
    nav.innerHTML = '';
    ['layer4', 'layer7'].forEach(layer => {
        const layerData = servers[layer];
        if (!layerData) return;
        const layerDiv = document.createElement('div');
        layerDiv.className = 'layer-container';
        layerDiv.innerHTML = `
            <button class="layer-button w-full flex items-center justify-between gap-3 px-3 py-2 text-[--text-secondary] hover:text-[--text-primary] transition-colors">
                <span class="flex items-center gap-3"><i data-lucide="layers" class="w-5 h-5"></i>Layer ${layer.slice(-1)}</span>
                <i data-lucide="chevron-right" class="w-4 h-4 rotate-icon"></i>
            </button>
            <div class="layer-content pl-4 space-y-1 category-content"></div>`;
        Object.entries(layerData).forEach(([catId, category]) => {
            const catDiv = document.createElement('div');
            catDiv.className = 'category-container';
            catDiv.innerHTML = `
                <button class="category-button w-full flex items-center justify-between gap-3 px-3 py-2 text-[--text-secondary] hover:text-[--text-primary]">
                    <span>${category.category_name}</span>
                    <i data-lucide="chevron-right" class="w-4 h-4 rotate-icon"></i>
                </button>
                <div class="pl-4 space-y-1 category-content"></div>`;
            const content = catDiv.querySelector('.category-content:last-child');
            const servers2 = category.servers || {};
            if (Object.keys(servers2).length === 0) {
                content.innerHTML = '<p class="text-sm text-gray-400 px-3 py-1">No servers</p>';
            } else {
                Object.entries(servers2).forEach(([id, srv]) => {
                    content.innerHTML += `
                        <a href="/${layer === 'layer4' ? 'l4' : 'l7'}?id=${id}" class="sub-server-button flex items-center gap-2 px-3 py-1.5 text-sm text-gray-400 hover:text-white rounded-md">
                            <img src="${srv.flag}" class="w-4 h-4 rounded-full flex-shrink-0">
                            <span class="flex-1 truncate">${srv.name}</span>
                            <span class="text-xs bg-gray-500/10 text-gray-500 px-1.5 py-0.5 rounded font-semibold">${srv.bandwidth}</span>
                        </a>`;
                });
            }
            layerDiv.querySelector('.layer-content').appendChild(catDiv);
        });
        nav.appendChild(layerDiv);
    });
    if (typeof lucide !== 'undefined') lucide.createIcons();
}

function initializeSidebar() {
    const sidebar = document.getElementById('sidebar');
    const openBtn = document.getElementById('openSidebar');
    const closeBtn = document.getElementById('closeSidebar');
    if (openBtn && sidebar) openBtn.addEventListener('click', () => sidebar.classList.remove('-translate-x-full'));
    if (closeBtn && sidebar) closeBtn.addEventListener('click', () => sidebar.classList.add('-translate-x-full'));
    document.querySelectorAll('.layer-button').forEach(btn => {
        btn.addEventListener('click', function() {
            const content = btn.nextElementSibling;
            const icon = btn.querySelector('.rotate-icon');
            const isOpen = content.style.maxHeight && content.style.maxHeight !== '0px';
            content.style.maxHeight = isOpen ? '0px' : '600px';
            content.style.opacity = isOpen ? '0' : '1';
            if (icon) icon.classList.toggle('open');
        });
    });
    document.querySelectorAll('.category-button').forEach(btn => {
        btn.addEventListener('click', function() {
            const content = btn.nextElementSibling;
            const icon = btn.querySelector('.rotate-icon');
            const isOpen = content.style.maxHeight && content.style.maxHeight !== '0px';
            content.style.maxHeight = isOpen ? '0px' : '600px';
            content.style.opacity = isOpen ? '0' : '1';
            if (icon) icon.classList.toggle('open');
        });
    });
}
