function initializeUI() {
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

function renderGraphDetails(server) {
    const isLayer7 = window.location.pathname.includes('/l7') || window.location.search.includes('l7');
    if (isLayer7) {
        const url = server.ip;
        document.getElementById('graph-details').innerHTML = `
            <div><p class="text-sm text-[--text-secondary]">Graph Name</p><p class="text-sm font-medium text-[--text-primary]">${server.name}</p></div>
            <div><p class="text-sm text-[--text-secondary]">URL</p><div class="flex items-center gap-2"><p class="text-sm font-medium text-[--text-primary]" id="ipAddress">${url}</p><button class="group rounded-md p-0 transition-colors" onclick="copyToClipboard('${url}', this)"><i class="fa-regular fa-copy h-4 w-4 text-[--text-secondary]"></i></button></div></div>
            <div><p class="text-sm text-[--text-secondary]">Requests</p><p class="text-sm font-medium text-[--text-primary]">${server.bandwidth}</p></div>`;
    } else {
        document.getElementById('graph-details').innerHTML = `
            <div><p class="text-sm text-[--text-secondary]">Graph Name</p><p class="text-sm font-medium text-[--text-primary]">${server.name}</p></div>
            <div><p class="text-sm text-[--text-secondary]">IP Address</p><div class="flex items-center gap-2"><p class="text-sm font-medium text-[--text-primary]" id="ipAddress">${server.ip}</p><button class="group rounded-md p-0 transition-colors" onclick="copyToClipboard('${server.ip}', this)"><i class="fa-regular fa-copy h-4 w-4 text-[--text-secondary]"></i></button></div></div>
            <div><p class="text-sm text-[--text-secondary]">TCP & UDP Port</p><p class="text-sm font-medium text-[--text-primary]">${server.ports || '22 & 53'}</p></div>
            <div><p class="text-sm text-[--text-secondary]">Bandwidth</p><p class="text-sm font-medium text-[--text-primary]">${server.bandwidth}</p></div>`;
    }
}

function copyToClipboard(text, element) {
    navigator.clipboard.writeText(text).catch(() => {
        const input = document.createElement('input');
        input.value = text;
        document.body.appendChild(input);
        input.select();
        document.execCommand('copy');
        document.body.removeChild(input);
    });
    const icon = element.querySelector('i');
    if (icon) {
        icon.className = 'fa-solid fa-check h-4 w-4';
        icon.style.color = '#9ca3af';
        setTimeout(() => {
            icon.className = 'fa-regular fa-copy h-4 w-4 text-[--text-secondary]';
            icon.style.color = '';
        }, 700);
    }
}

function renderBanners(banners) {
    const buyImage = '/buy.png';
    const ethoneImage = '/assets/ethone-gif.gif';
    ['banner-list-1', 'banner-list-2'].forEach((listId, idx) => {
        const container = document.getElementById(listId);
        if (!container) return;
        container.innerHTML = '';
        const items = idx === 0
            ? [{ img: ethoneImage, url: 'https://ethone.net/' }, { img: buyImage, url: 'https://t.me/Layer4Terrorist' }, { img: buyImage, url: 'https://t.me/Layer4Terrorist' }, { img: buyImage, url: 'https://t.me/Layer4Terrorist' }]
            : [{ img: buyImage, url: 'https://t.me/Layer4Terrorist' }, { img: buyImage, url: 'https://t.me/Layer4Terrorist' }, { img: buyImage, url: 'https://t.me/Layer4Terrorist' }, { img: buyImage, url: 'https://t.me/Layer4Terrorist' }];
        items.forEach(item => {
            const div = document.createElement('div');
            div.className = 'rounded-lg overflow-hidden cursor-pointer';
            div.innerHTML = `<div class="relative w-full h-20 flex items-center justify-center"><img src="${item.img}" class="w-full h-full object-contain p-2"></div>`;
            div.addEventListener('click', () => window.open(item.url, '_blank'));
            container.appendChild(div);
        });
    });
}
