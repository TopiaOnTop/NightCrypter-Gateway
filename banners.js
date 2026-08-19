document.addEventListener('DOMContentLoaded', async function() {
    try {
        const res = await fetch('/api/banners');
        const banners = await res.json();

        const bannerList1 = document.getElementById('banner-list-1');
        const bannerList2 = document.getElementById('banner-list-2');

        if (bannerList1) bannerList1.innerHTML = '';
        if (bannerList2) bannerList2.innerHTML = '';

        if (Array.isArray(banners) && banners.length > 0) {
            banners.forEach((b, idx) => {
                const targetContainer = (idx % 2 === 0) ? (bannerList1 || bannerList2) : (bannerList2 || bannerList1);
                if (!targetContainer) return;

                const clickUrl = `/api/banners/click/${b.id}`;
                const div = document.createElement('div');
                div.className = 'rounded-lg overflow-hidden cursor-pointer border border-gray-800/40 hover:border-blue-500/50 transition-all';
                div.innerHTML = `<div class="relative w-full h-16 flex items-center justify-center bg-slate-900/60"><img src="${b.img}" class="w-full h-full object-cover p-0"></div>`;
                div.addEventListener('click', () => window.open(clickUrl, '_blank'));
                targetContainer.appendChild(div);
            });
        }
    } catch (e) {
        console.error('Failed to load banners from API:', e);
    }
});
