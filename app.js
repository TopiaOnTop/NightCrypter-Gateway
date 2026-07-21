/**
 * Oblivion OS - Main Frontend State Orchestration Engine
 */

// ==========================================================================
// 1. SYSTEM DICTIONARY LOCALIZATION
// ==========================================================================
const LOCALIZATION_DICTIONARY = {
    en: {
        login_sub: "SECURE MULTI-THREAD VIRTUAL SYSTEM",
        username_placeholder: "Authorized Username",
        password_placeholder: "Cryptographic Key",
        login_btn: "INITIALIZE HANDSHAKE",
        sys_secured: "ENCRYPTED STATE",
        security_shield: "Secure Tunnel",
        app_terminal: "Shell Emulator",
        app_ide: "Monaco Editor IDE",
        save_btn: "Save File",
        active_file: "Active File:",
        app_media: "Universal Media Viewer",
        app_filemanager: "System File Manager",
        quick_access: "QUICK ACCESS",
        nav_desktop: "Desktop",
        nav_docs: "Documents",
        nav_downloads: "Downloads",
        nav_media: "Media Hub",
        dir_up: "Dir Up",
        app_settings: "System Panel Settings",
        settings_tab1: "Generalization",
        settings_tab2: "Personalization",
        settings_tab3: "Adapter Mapping",
        settings_tab4: "Monitoring",
        tab1_hdr: "Global Language & Clock Settings",
        set_language: "System Localization Strings",
        set_clock: "Time Representation Scheme",
        clock_12: "12-Hour (AM/PM)",
        clock_24: "24-Hour (Military)",
        tab2_hdr: "Visual Environment Preferences",
        set_wallpaper: "Canvas Desktop Wallpaper",
        upload_wallpaper: "Load Host Image File",
        dock_scale: "Base Dock Scale Dimension",
        dock_magnify: "Icon Magnification Hover Effect",
        enable_magnify: "Enable Dynamic Scales",
        anim_speed: "Interface Transition Velocity",
        speed_ultra: "Ultra-Fluid (Default)",
        speed_fast: "High-Velocity Fast",
        speed_none: "Deactivated Transitions",
        tab3_hdr: "Register Host Executables Mapping",
        tab3_descr: "Bind native system applications dynamically into your Oblivion workspace shortcuts grid layout.",
        map_name: "Application Signature Name",
        map_path: "Native Executable Local Disk Path",
        map_icon: "Associated System Style Icon",
        register_shortcut: "Register Custom Application Shortcut",
        tab4_hdr: "Performance Hardware Telemetry",
        monitor_insulation: "Security Data Insulation:",
        insulation_opt: "SECURE CONTEXT SHIFTED",
        monitor_user: "User Security Handle:",
        monitor_session: "Valid Session Token:",
        cpu_label: "Process Core CPU Utilization",
        ram_label: "Volatile Core Memory Utilization",
        modal_acknowledge: "Acknowledge",
        tooltip_terminal: "Live Terminal",
        tooltip_ide: "Monaco IDE",
        tooltip_media: "Media Viewer",
        tooltip_files: "File Manager",
        tooltip_settings: "Settings"
    },
    fr: {
        login_sub: "SYSTÈME VIRTUEL SÉCURISÉ MULTI-THREAD",
        username_placeholder: "Nom d'utilisateur autorisé",
        password_placeholder: "Clé cryptographique",
        login_btn: "INITIALISER LA CONNEXION",
        sys_secured: "ÉTAT ENCRYPTÉ",
        security_shield: "Tunnel Sécurisé",
        app_terminal: "Émulateur de Terminal",
        app_ide: "Monaco Éditeur IDE",
        save_btn: "Enregistrer le fichier",
        active_file: "Fichier Actif:",
        app_media: "Lecteur Multimédia Universel",
        app_filemanager: "Gestionnaire de Fichiers",
        quick_access: "ACCÈS RAPIDE",
        nav_desktop: "Bureau",
        nav_docs: "Documents",
        nav_downloads: "Téléchargements",
        nav_media: "Médiathèque",
        dir_up: "Dossier Parent",
        app_settings: "Paramètres Système",
        settings_tab1: "Généralisation",
        settings_tab2: "Personnalisation",
        settings_tab3: "Mappage d'Adaptateur",
        settings_tab4: "Surveillance",
        tab1_hdr: "Paramètres de Langue Globale & Horloge",
        set_language: "Traduction de Localisation Système",
        set_clock: "Format d'affichage de l'heure",
        clock_12: "Format 12 Heures (AM/PM)",
        clock_24: "Format 24 Heures (Militaire)",
        tab2_hdr: "Préférences d'Environnement Visuel",
        set_wallpaper: "Fond d'écran du Bureau",
        upload_wallpaper: "Charger une image locale",
        dock_scale: "Dimension d'Échelle de Base du Dock",
        dock_magnify: "Effet d'Agrandissement des Icônes",
        enable_magnify: "Activer les Échelles Dynamiques",
        anim_speed: "Vitesse de Transition de l'Interface",
        speed_ultra: "Ultra-Fluide (Défaut)",
        speed_fast: "Haute Vélocité Rapide",
        speed_none: "Transitions Désactivées",
        tab3_hdr: "Enregistrer un exécutable local",
        tab3_descr: "Liez dynamiquement des applications système natives à la grille de raccourcis d'Oblivion.",
        map_name: "Nom Signature de l'Application",
        map_path: "Chemin Local de l'Exécutable Disque",
        map_icon: "Icône de Style Associée",
        register_shortcut: "Enregistrer le raccourci d'application",
        tab4_hdr: "Télémétrie Matérielle de Performance",
        monitor_insulation: "Isolation des données sécurisées:",
        insulation_opt: "CONTEXTE SÉCURISÉ TRANSFÉRÉ",
        monitor_user: "Identifiant utilisateur de sécurité:",
        monitor_session: "Jeton de session valide:",
        cpu_label: "Utilisation du Processeur Core CPU",
        ram_label: "Utilisation de la Mémoire Vive RAM",
        modal_acknowledge: "Prendre acte",
        tooltip_terminal: "Terminal Live",
        tooltip_ide: "Monaco IDE",
        tooltip_media: "Média Universel",
        tooltip_files: "Fichiers",
        tooltip_settings: "Paramètres"
    }
};

// ==========================================================================
// 2. MAIN STATE STORE (OS_STATE)
// ==========================================================================
const SYSTEM_APPS = [
    { id: 'winTerminal', titleKey: 'app_terminal', icon: 'fa-solid fa-terminal', tooltipKey: 'tooltip_terminal' },
    { id: 'winIde', titleKey: 'app_ide', icon: 'fa-solid fa-code', tooltipKey: 'tooltip_ide' },
    { id: 'winMedia', titleKey: 'app_media', icon: 'fa-solid fa-photo-film', tooltipKey: 'tooltip_media' },
    { id: 'winFileManager', titleKey: 'app_filemanager', icon: 'fa-solid fa-folder', tooltipKey: 'tooltip_files' },
    { id: 'winSettings', titleKey: 'app_settings', icon: 'fa-solid fa-gears', tooltipKey: 'tooltip_settings' }
];

const OS_STATE = {
    locale: 'en',
    clockFormat24: false,
    focusedWindow: null,
    windowLayers: [],
    customShortcuts: [],
    pinnedDockApps: [...SYSTEM_APPS],

    // File manager state
    currentDirPath: '',
    homeDirPath: '',

    // Visual preferences
    wallpaperType: 'gradient',
    wallpaperVal: 'linear-gradient(135deg, #0A192F, #0D1B2A)',
    dockScale: 60,
    dockMagnify: true,
    transitionSpeed: 'ultra', // ultra, fast, none

    // Canvas panning/zoom state for Universal Media Viewer
    imageZoom: 1.0,
    imagePanX: 0,
    imagePanY: 0,
    isDraggingImage: false,
    dragStartX: 0,
    dragStartY: 0,
    currentImage: null, // Keep track of active Image element reference

    // Monaco Instance
    monacoInstance: null,
    activeEditingFilePath: null
};

// ==========================================================================
// 3. CENTRAL OBJECT PROVIDER & DRAG/DROP INITIALIZATION
// ==========================================================================
const OS = {
    init() {
        this.bindEvents();
        this.initClock();
        this.renderDesktopAndDock();
        this.initTerminal();
        this.initMonaco();
        this.initImageCanvas();
        this.initSystemMetrics();
        this.loadInitialDirectory();
    },

    bindEvents() {
        // Form logins
        document.getElementById('loginSubmitBtn').addEventListener('click', () => this.handleAuthentication());

        // Modal confirm button action
        document.getElementById('modalConfirmBtn').addEventListener('click', () => {
            document.getElementById('modalOverlay').classList.add('hidden');
        });

        // Dynamic z-index layering on window clicks
        document.querySelectorAll('.os-window').forEach(win => {
            win.addEventListener('mousedown', () => this.bringToFront(win.id));
            this.makeWindowDraggable(win);
        });

        // Seekers and players
        const vidPlayer = document.getElementById('mediaVideoPlayer');
        const audPlayer = document.getElementById('mediaAudioPlayer');

        vidPlayer.addEventListener('timeupdate', () => this.updateVideoSeeker());
        vidPlayer.addEventListener('loadedmetadata', () => {
            document.getElementById('vidSeeker').max = vidPlayer.duration;
        });
        document.getElementById('vidSeeker').addEventListener('input', (e) => {
            vidPlayer.currentTime = e.target.value;
        });
        document.getElementById('vidVolume').addEventListener('input', (e) => {
            vidPlayer.volume = e.target.value;
        });

        audPlayer.addEventListener('timeupdate', () => this.updateAudioSeeker());
        audPlayer.addEventListener('loadedmetadata', () => {
            document.getElementById('audSeeker').max = audPlayer.duration;
        });
        document.getElementById('audSeeker').addEventListener('input', (e) => {
            audPlayer.currentTime = e.target.value;
        });
        document.getElementById('audVolume').addEventListener('input', (e) => {
            audPlayer.volume = e.target.value;
        });
    },

    // CUSTOM OVERLAY DIALOG POPUP (REPLACING BROWSER ALERTS)
    showAlert(title, message, iconClass = 'fa-solid fa-circle-exclamation text-cyan') {
        document.getElementById('modalTitle').textContent = title.toUpperCase();
        document.getElementById('modalMessage').textContent = message;
        document.getElementById('modalIcon').className = iconClass;

        const overlay = document.getElementById('modalOverlay');
        overlay.classList.remove('hidden');

        // Scale GSAP Fluid popup animation
        gsap.fromTo(".custom-modal-dialog",
            { scale: 0.85, opacity: 0 },
            { scale: 1, opacity: 1, duration: 0.3, ease: "back.out(1.7)" }
        );
    },

    // SECURE AUTHENTICATION SYSTEM HANDSHAKE DELAY
    handleAuthentication() {
        const user = document.getElementById('usernameInput').value;
        const key = document.getElementById('passwordInput').value;

        if (user === 'Topia' && key === 'topiatheking') {
            const progressBox = document.getElementById('authProgress');
            progressBox.style.display = 'flex';

            let progress = 0;
            const bar = document.getElementById('authProgressBar');
            const logText = document.getElementById('authProgressText');

            const steps = [
                { limit: 20, text: "Generating 512-bit secure salt..." },
                { limit: 50, text: "Computing Argon2id cryptographic parameters..." },
                { limit: 80, text: "Insulating local memory storage blocks..." },
                { limit: 100, text: "Handshake verify complete. Mounting user desktop state..." }
            ];

            let stepIdx = 0;
            const interval = setInterval(() => {
                if (progress < 100) {
                    progress += 2;
                    bar.style.width = `${progress}%`;

                    if (stepIdx < steps.length && progress >= steps[stepIdx].limit) {
                        logText.textContent = steps[stepIdx].text;
                        stepIdx++;
                    }
                } else {
                    clearInterval(interval);

                    // Secure transition into the virtualized environment
                    gsap.to("#loginLayer", {
                        opacity: 0,
                        duration: 0.8,
                        ease: "power2.out",
                        onComplete: () => {
                            document.getElementById('loginLayer').classList.add('hidden');
                            document.getElementById('desktopLayer').classList.remove('hidden');
                            gsap.fromTo("#desktopLayer", { opacity: 0 }, { opacity: 1, duration: 0.5 });
                        }
                    });
                }
            }, 50);

        } else {
            this.showAlert("Access Denied", "Cryptographic authentication signature mismatch. Verify authorized admin credentials.", "fa-solid fa-triangle-exclamation text-cyan");
        }
    },

    // BILINGUAL LANGUAGE LOCALIZATION ROUTER
    toggleLanguage(lang) {
        OS_STATE.locale = lang;
        const dict = LOCALIZATION_DICTIONARY[lang];

        // Find elements with translate tags
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (dict[key]) {
                if (el.tagName === 'SPAN' || el.tagName === 'H3' || el.tagName === 'P' || el.tagName === 'LABEL' || el.tagName === 'BUTTON') {
                    // Retain icon elements if present
                    const icon = el.querySelector('i');
                    if (icon) {
                        el.innerHTML = '';
                        el.appendChild(icon);
                        el.innerHTML += ` ${dict[key]}`;
                    } else {
                        el.textContent = dict[key];
                    }
                } else {
                    el.textContent = dict[key];
                }
            }
        });

        // Set inputs placeholders
        document.querySelectorAll('[data-i18n-placeholder]').forEach(input => {
            const key = input.getAttribute('data-i18n-placeholder');
            if (dict[key]) {
                input.placeholder = dict[key];
            }
        });

        // Update tooltips on dock
        this.renderDesktopAndDock();
    },

    toggleClockFormat(format) {
        OS_STATE.clockFormat24 = (format === '24');
    },

    initClock() {
        const update = () => {
            const now = new Date();
            let hours = now.getHours();
            const minutes = String(now.getMinutes()).padStart(2, '0');
            const seconds = String(now.getSeconds()).padStart(2, '0');

            if (!OS_STATE.clockFormat24) {
                const ampm = hours >= 12 ? 'PM' : 'AM';
                hours = hours % 12;
                hours = hours ? hours : 12; // hour '0' should be '12'
                document.getElementById('systemClock').textContent = `${String(hours).padStart(2, '0')}:${minutes}:${seconds} ${ampm}`;
            } else {
                document.getElementById('systemClock').textContent = `${String(hours).padStart(2, '0')}:${minutes}:${seconds}`;
            }
        };
        update();
        setInterval(update, 1000);
    },

    // RENDERS THE DESKTOP AND CENTRED GLASSMORPHISM DOCK
    renderDesktopAndDock() {
        const workbench = document.getElementById('desktopWorkbench');
        const dock = document.getElementById('systemDock');
        const dict = LOCALIZATION_DICTIONARY[OS_STATE.locale];

        workbench.innerHTML = '';
        dock.innerHTML = '';

        // Combine system and custom executable registered adapters
        const shortcuts = [...SYSTEM_APPS, ...OS_STATE.customShortcuts];

        // 1. Render desktop shortcuts
        shortcuts.forEach(app => {
            const shortcut = document.createElement('div');
            shortcut.className = 'desktop-shortcut';
            shortcut.draggable = true;
            shortcut.innerHTML = `
                <div class="shortcut-icon-wrap">
                    <i class="${app.icon}"></i>
                </div>
                <div class="shortcut-label">${dict[app.titleKey] || app.titleKey}</div>
            `;

            // Open window on double click
            shortcut.addEventListener('dblclick', () => this.openWindow(app.id));

            // Drag and drop capability onto dock
            shortcut.addEventListener('dragstart', (e) => {
                e.dataTransfer.setData('text/plain', JSON.stringify(app));
            });

            workbench.appendChild(shortcut);
        });

        // 2. Render pinned app launchers in the dock
        OS_STATE.pinnedDockApps.forEach(app => {
            const dockItemWrap = document.createElement('div');
            dockItemWrap.className = 'dock-item-wrapper';
            dockItemWrap.id = `dock-${app.id}`;
            dockItemWrap.innerHTML = `
                <div class="dock-item" style="width: ${OS_STATE.dockScale}px; height: ${OS_STATE.dockScale}px;">
                    <i class="${app.icon}"></i>
                </div>
                <div class="dock-tooltip">${dict[app.tooltipKey] || app.tooltipKey || (dict[app.titleKey] || app.titleKey)}</div>
                <div class="dock-active-dot"></div>
            `;

            dockItemWrap.addEventListener('click', () => this.toggleWindow(app.id, `dock-${app.id}`));

            // Dock icon scale hover effect magnification logic
            if (OS_STATE.dockMagnify) {
                const dockItem = dockItemWrap.querySelector('.dock-item');
                dockItemWrap.addEventListener('mousemove', (e) => {
                    const rect = dockItemWrap.getBoundingClientRect();
                    const offset = Math.abs(e.clientX - (rect.left + rect.width / 2));
                    const scale = Math.max(1, 1.3 - (offset / 100));
                    dockItem.style.width = `${OS_STATE.dockScale * scale}px`;
                    dockItem.style.height = `${OS_STATE.dockScale * scale}px`;
                });
                dockItemWrap.addEventListener('mouseleave', () => {
                    dockItem.style.width = `${OS_STATE.dockScale}px`;
                    dockItem.style.height = `${OS_STATE.dockScale}px`;
                });
            }

            dock.appendChild(dockItemWrap);
        });

        // Register drag events to let user drop pinned applications onto the dock
        dock.addEventListener('dragover', (e) => e.preventDefault());
        dock.addEventListener('drop', (e) => {
            e.preventDefault();
            try {
                const data = JSON.parse(e.dataTransfer.getData('text/plain'));

                // Add to pinnedDockApps if not already exists
                const alreadyPinned = OS_STATE.pinnedDockApps.some(app => app.id === data.id);
                if (!alreadyPinned) {
                    OS_STATE.pinnedDockApps.push(data);
                    this.renderDesktopAndDock();
                    this.showAlert("Dock Sync", `Successfully pinned ${dict[data.titleKey] || data.titleKey} into Glassmorphic dock area.`, "fa-solid fa-circle-check text-cyan");
                } else {
                    this.showAlert("Dock Sync", `${dict[data.titleKey] || data.titleKey} is already pinned to the dock.`, "fa-solid fa-circle-info text-cyan");
                }
            } catch (err) {}
        });
    },

    // ==========================================================================
    // 4. WINDOWS AND LAYERING Focus Z-INDEX HANDLER
    // ==========================================================================
    makeWindowDraggable(win) {
        const titlebar = win.querySelector('.window-titlebar');
        let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;

        titlebar.onmousedown = dragMouseDown;

        function dragMouseDown(e) {
            e = e || window.event;
            e.preventDefault();
            pos3 = e.clientX;
            pos4 = e.clientY;
            document.onmouseup = closeDragElement;
            document.onmousemove = elementDrag;
        }

        function elementDrag(e) {
            e = e || window.event;
            e.preventDefault();
            pos1 = pos3 - e.clientX;
            pos2 = pos4 - e.clientY;
            pos3 = e.clientX;
            pos4 = e.clientY;

            // Restrict bounds slightly to prevent absolute loss off-screen
            const topBoundary = Math.max(0, win.offsetTop - pos2);
            win.style.top = topBoundary + "px";
            win.style.left = (win.offsetLeft - pos1) + "px";
        }

        function closeDragElement() {
            document.onmouseup = null;
            document.onmousemove = null;
        }
    },

    bringToFront(windowId) {
        const index = OS_STATE.windowLayers.indexOf(windowId);
        if (index > -1) {
            OS_STATE.windowLayers.splice(index, 1);
        }
        OS_STATE.windowLayers.push(windowId);

        // Apply z-index according to tracking array order
        OS_STATE.windowLayers.forEach((id, idx) => {
            const win = document.getElementById(id);
            if (win) {
                win.style.zIndex = 10 + idx;
            }
        });
        OS_STATE.focusedWindow = windowId;
    },

    openWindow(windowId) {
        const win = document.getElementById(windowId);
        if (!win) return;

        win.classList.remove('hidden');
        win.classList.remove('minimized');

        const dockEl = document.getElementById(`dock-${windowId}`);
        if (dockEl) {
            dockEl.classList.add('active');
        }

        this.bringToFront(windowId);

        // Transition animations
        if (OS_STATE.transitionSpeed === 'ultra') {
            gsap.fromTo(win, { scale: 0.9, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: "back.out(1.5)" });
        } else if (OS_STATE.transitionSpeed === 'fast') {
            gsap.fromTo(win, { scale: 0.95, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.2, ease: "power1.out" });
        } else {
            win.style.opacity = '1';
            win.style.transform = 'scale(1)';
        }

        // Initialize Monaco when its containing window opens
        if (windowId === 'winIde' && OS_STATE.monacoInstance) {
            OS_STATE.monacoInstance.layout();
        }
    },

    closeWindow(windowId) {
        const win = document.getElementById(windowId);
        if (!win) return;

        const dockEl = document.getElementById(`dock-${windowId}`);
        if (dockEl) {
            dockEl.classList.remove('active');
        }

        // Reset video or music if currently playing inside the closing sandbox
        if (windowId === 'winMedia') {
            document.getElementById('mediaVideoPlayer').pause();
            document.getElementById('mediaAudioPlayer').pause();
            document.getElementById('audioDisc').style.animationPlayState = 'paused';
        }

        if (OS_STATE.transitionSpeed === 'none') {
            win.classList.add('hidden');
        } else {
            gsap.to(win, {
                scale: 0.9,
                opacity: 0,
                duration: OS_STATE.transitionSpeed === 'ultra' ? 0.3 : 0.15,
                ease: "power2.in",
                onComplete: () => win.classList.add('hidden')
            });
        }
    },

    toggleWindow(windowId, dockItemId) {
        const win = document.getElementById(windowId);
        if (!win) return;

        if (win.classList.contains('hidden') || win.classList.contains('minimized')) {
            this.openWindow(windowId);
        } else {
            if (OS_STATE.focusedWindow === windowId) {
                this.minimizeWindow(windowId, dockItemId);
            } else {
                this.bringToFront(windowId);
            }
        }
    },

    // THE GENIE EFFECT MINIMIZE VACUUM SCALE ANIMATION (GSAP COORDS TARGETING)
    minimizeWindow(windowId, dockItemId) {
        const win = document.getElementById(windowId);
        const dockItem = document.getElementById(dockItemId);
        if (!win || !dockItem) return;

        win.classList.add('minimized');
        const dockRect = dockItem.getBoundingClientRect();
        const winRect = win.getBoundingClientRect();

        // Target coordinates
        const targetX = dockRect.left + (dockRect.width / 2) - winRect.left;
        const targetY = dockRect.top - winRect.top;

        if (OS_STATE.transitionSpeed === 'none') {
            win.classList.add('hidden');
        } else {
            const tl = gsap.timeline({
                onComplete: () => {
                    win.classList.add('hidden');
                }
            });

            // Vacuum/Genie curve scale down
            tl.to(win, {
                x: targetX - (winRect.width / 2),
                y: targetY,
                scaleX: 0.05,
                scaleY: 0.05,
                opacity: 0.1,
                duration: OS_STATE.transitionSpeed === 'ultra' ? 0.55 : 0.3,
                ease: "power2.inOut"
            });

            // Clean up coordinates after completion of the transition sequence
            tl.set(win, { x: 0, y: 0, scaleX: 1, scaleY: 1 });
        }
    },

    maximizeWindow(windowId) {
        const win = document.getElementById(windowId);
        if (!win) return;

        if (win.style.width === '100vw') {
            win.style.width = '750px';
            win.style.height = '480px';
            win.style.top = '10%';
            win.style.left = '15%';
        } else {
            win.style.width = '100vw';
            win.style.height = 'calc(100vh - 32px)';
            win.style.top = '32px';
            win.style.left = '0';
        }

        if (windowId === 'winIde' && OS_STATE.monacoInstance) {
            setTimeout(() => OS_STATE.monacoInstance.layout(), 100);
        }
    },

    // ==========================================================================
    // 5. NATIVE CORE APPLICATIONS INTEGRATIONS
    // ==========================================================================

    // A. SHELL TERMINAL EMULATOR
    initTerminal() {
        if (!window.api || !window.api.terminal) return;

        const term = new Terminal({
            cursorBlink: true,
            theme: {
                background: '#030712',
                foreground: '#00f0ff',
                cursor: '#00f0ff',
                selection: 'rgba(0, 240, 255, 0.3)'
            },
            fontFamily: 'JetBrains Mono, monospace',
            fontSize: 12,
            letterSpacing: 1
        });

        const fitAddon = new FitAddon.FitAddon();
        term.loadAddon(fitAddon);
        term.open(document.getElementById('terminalContainer'));
        fitAddon.fit();

        window.api.terminal.init();
        window.api.terminal.onIncoming((data) => {
            term.write(data);
        });

        term.onData((data) => {
            window.api.terminal.write(data);
        });

        // Resize handler
        window.addEventListener('resize', () => fitAddon.fit());
    },

    // B. STANDALONE MONACO CODE EDITOR
    initMonaco() {
        // Wait for Monaco library to complete mounting loader
        if (typeof monaco === 'undefined') {
            setTimeout(() => this.initMonaco(), 100);
            return;
        }

        OS_STATE.monacoInstance = monaco.editor.create(document.getElementById('monacoEditorContainer'), {
            value: [
                '// Welcome to Monaco Source Code Editor IDE inside Oblivion OS',
                'function initializeSystem() {',
                '    console.log("Oblivion Workspace Active.");',
                '}'
            ].join('\n'),
            language: 'javascript',
            theme: 'vs-dark',
            automaticLayout: true,
            minimap: { enabled: true },
            fontSize: 12,
            fontFamily: 'JetBrains Mono, monospace'
        });

        // Trigger Ctrl+S interception
        OS_STATE.monacoInstance.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyS, () => {
            this.saveIdeFile();
        });
    },

    async saveIdeFile() {
        if (!OS_STATE.activeEditingFilePath) {
            this.showAlert("IDE Status", "No active file is currently open to write stream updates directly back to host disk.", "fa-solid fa-triangle-exclamation text-cyan");
            return;
        }

        const editorValue = OS_STATE.monacoInstance.getValue();
        try {
            await window.api.fs.writeFile(OS_STATE.activeEditingFilePath, editorValue);
            this.showAlert("IDE Status", `Changes saved successfully to local host path: ${OS_STATE.activeEditingFilePath}`, "fa-solid fa-circle-check text-cyan");
        } catch (err) {
            this.showAlert("Error", `An error occurred writing data stream: ${err.message}`, "fa-solid fa-triangle-exclamation text-cyan");
        }
    },

    // C. UNIVERSAL MEDIA VIEWPORT CANVAS ZOOM/PAN HANDLERS
    initImageCanvas() {
        const canvas = document.getElementById('mediaImageCanvas');
        if (!canvas) return;

        canvas.addEventListener('mousedown', (e) => {
            OS_STATE.isDraggingImage = true;
            OS_STATE.dragStartX = e.clientX - OS_STATE.imagePanX;
            OS_STATE.dragStartY = e.clientY - OS_STATE.imagePanY;
        });

        window.addEventListener('mousemove', (e) => {
            if (!OS_STATE.isDraggingImage) return;
            OS_STATE.imagePanX = e.clientX - OS_STATE.dragStartX;
            OS_STATE.imagePanY = e.clientY - OS_STATE.dragStartY;
            this.renderImageToCanvas();
        });

        window.addEventListener('mouseup', () => {
            OS_STATE.isDraggingImage = false;
        });

        canvas.addEventListener('wheel', (e) => {
            e.preventDefault();
            const zoomFactor = e.deltaY < 0 ? 1.1 : 0.9;
            this.zoomMediaImage(zoomFactor);
        });
    },

    zoomMediaImage(factor) {
        OS_STATE.imageZoom *= factor;
        // Bound scaling dimension
        OS_STATE.imageZoom = Math.max(0.1, Math.min(OS_STATE.imageZoom, 5.0));
        this.renderImageToCanvas();
    },

    resetMediaImage() {
        OS_STATE.imageZoom = 1.0;
        OS_STATE.imagePanX = 0;
        OS_STATE.imagePanY = 0;
        this.renderImageToCanvas();
    },

    renderImageToCanvas() {
        const img = OS_STATE.currentImage;
        if (!img) return;

        const canvas = document.getElementById('mediaImageCanvas');
        const ctx = canvas.getContext('2d');
        const parent = canvas.parentElement;

        // Auto size
        canvas.width = parent.clientWidth;
        canvas.height = parent.clientHeight;

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.save();
        ctx.translate(canvas.width / 2 + OS_STATE.imagePanX, canvas.height / 2 + OS_STATE.imagePanY);
        ctx.scale(OS_STATE.imageZoom, OS_STATE.imageZoom);
        ctx.drawImage(img, -img.width / 2, -img.height / 2);
        ctx.restore();
    },

    // MEDIA VIEWER VIDEO PLAYBACK CONTROLLERS
    toggleVideo() {
        const v = document.getElementById('mediaVideoPlayer');
        const btn = document.getElementById('vidPlayBtn');
        if (v.paused) {
            v.play();
            btn.innerHTML = `<i class="fa-solid fa-pause"></i>`;
        } else {
            v.pause();
            btn.innerHTML = `<i class="fa-solid fa-play"></i>`;
        }
    },

    toggleVideoMute() {
        const v = document.getElementById('mediaVideoPlayer');
        const btn = document.getElementById('vidMuteBtn');
        v.muted = !v.muted;
        if (v.muted) {
            btn.innerHTML = `<i class="fa-solid fa-volume-xmark"></i>`;
        } else {
            btn.innerHTML = `<i class="fa-solid fa-volume-high"></i>`;
        }
    },

    updateVideoSeeker() {
        const v = document.getElementById('mediaVideoPlayer');
        const seeker = document.getElementById('vidSeeker');
        const label = document.getElementById('vidTimeLabel');

        seeker.value = v.currentTime;

        const curMins = Math.floor(v.currentTime / 60);
        const curSecs = String(Math.floor(v.currentTime % 60)).padStart(2, '0');
        const durMins = Math.floor(v.duration / 60) || 0;
        const durSecs = String(Math.floor(v.duration % 60) || 0).padStart(2, '0');

        label.textContent = `${curMins}:${curSecs} / ${durMins}:${durSecs}`;
    },

    // MEDIA VIEWER AUDIO PLAYBACK CONTROLLERS
    toggleAudio() {
        const a = document.getElementById('mediaAudioPlayer');
        const btn = document.getElementById('audPlayBtn');
        const disc = document.getElementById('audioDisc');

        if (a.paused) {
            a.play();
            btn.innerHTML = `<i class="fa-solid fa-pause"></i>`;
            disc.style.animationPlayState = 'running';
        } else {
            a.pause();
            btn.innerHTML = `<i class="fa-solid fa-play"></i>`;
            disc.style.animationPlayState = 'paused';
        }
    },

    toggleAudioMute() {
        const a = document.getElementById('mediaAudioPlayer');
        const btn = document.getElementById('audMuteBtn');
        a.muted = !a.muted;
        if (a.muted) {
            btn.innerHTML = `<i class="fa-solid fa-volume-xmark"></i>`;
        } else {
            btn.innerHTML = `<i class="fa-solid fa-volume-high"></i>`;
        }
    },

    updateAudioSeeker() {
        const a = document.getElementById('mediaAudioPlayer');
        const seeker = document.getElementById('audSeeker');
        const label = document.getElementById('audTimeLabel');

        seeker.value = a.currentTime;

        const curMins = Math.floor(a.currentTime / 60);
        const curSecs = String(Math.floor(a.currentTime % 60)).padStart(2, '0');
        const durMins = Math.floor(a.duration / 60) || 0;
        const durSecs = String(Math.floor(a.duration % 60) || 0).padStart(2, '0');

        label.textContent = `${curMins}:${curSecs} / ${durMins}:${durSecs}`;
    },

    // D. FILE MANAGER DIRECTORY LOAD ENGINE
    async loadInitialDirectory() {
        if (!window.api || !window.api.fs) return;
        OS_STATE.homeDirPath = await window.api.fs.getHomeDir();
        OS_STATE.currentDirPath = OS_STATE.homeDirPath;
        this.openDirectory(OS_STATE.homeDirPath);
    },

    async openDirectory(dirPath) {
        if (!window.api || !window.api.fs) return;

        // Map alias keys down to native structures
        let target = dirPath;
        if (dirPath === 'desktop') target = `${OS_STATE.homeDirPath}/Desktop`;
        if (dirPath === 'documents') target = `${OS_STATE.homeDirPath}/Documents`;
        if (dirPath === 'downloads') target = `${OS_STATE.homeDirPath}/Downloads`;
        if (dirPath === 'media') target = `${OS_STATE.homeDirPath}/Videos`; // Default media routing

        try {
            const list = await window.api.fs.readDir(target);
            OS_STATE.currentDirPath = target;
            document.getElementById('currentDirPathDisplay').textContent = target;

            // Update sidebar navigation selection state
            const sidebarItems = document.querySelectorAll('.sidebar-nav-item');
            sidebarItems.forEach(item => item.classList.remove('active'));

            // Render file grid layout dynamically
            const grid = document.getElementById('fileManagerGrid');
            grid.innerHTML = '';

            list.forEach(item => {
                const itemEl = document.createElement('div');
                itemEl.className = `file-grid-item ${item.isDirectory ? 'dir-item' : 'file-item'}`;

                // Extension icon routing
                let iconClass = 'fa-solid fa-file';
                if (item.isDirectory) {
                    iconClass = 'fa-solid fa-folder';
                } else {
                    const ext = item.name.split('.').pop().toLowerCase();
                    if (['txt', 'json', 'md'].includes(ext)) iconClass = 'fa-solid fa-file-lines';
                    else if (['png', 'jpg', 'jpeg', 'svg'].includes(ext)) iconClass = 'fa-solid fa-file-image';
                    else if (['mp4', 'webm'].includes(ext)) iconClass = 'fa-solid fa-file-video';
                    else if (['mp3', 'wav'].includes(ext)) iconClass = 'fa-solid fa-file-audio';
                    else if (['js', 'ts', 'html', 'css', 'json', 'cpp', 'py'].includes(ext)) iconClass = 'fa-solid fa-file-code';
                }

                itemEl.innerHTML = `
                    <i class="${iconClass}"></i>
                    <span class="file-item-name">${item.name}</span>
                `;

                // Handle routing on double click
                itemEl.addEventListener('dblclick', () => {
                    if (item.isDirectory) {
                        this.openDirectory(item.path);
                    } else {
                        this.routeFileToViewer(item.path);
                    }
                });

                grid.appendChild(itemEl);
            });
        } catch (err) {
            this.showAlert("Error", `Unable to parse target file manager path: ${err.message}`, "fa-solid fa-circle-exclamation text-cyan");
        }
    },

    navDirUp() {
        const parts = OS_STATE.currentDirPath.split(/[\\/]/);
        if (parts.length > 1) {
            parts.pop();
            const parentPath = parts.join('/') || '/';
            this.openDirectory(parentPath);
        }
    },

    // EXTENSION DETECTOR AND ROUTER
    async routeFileToViewer(filePath) {
        const ext = filePath.split('.').pop().toLowerCase();

        // 1. Image Viewer Routing
        if (['png', 'jpg', 'jpeg', 'svg'].includes(ext)) {
            this.openWindow('winMedia');
            document.querySelectorAll('.media-screen').forEach(el => el.classList.add('hidden'));
            document.getElementById('mediaBoxImage').classList.remove('hidden');

            const img = new Image();
            img.src = filePath;
            img.onload = () => {
                OS_STATE.currentImage = img;
                this.resetMediaImage();
            };
        }
        // 2. Text / Markdown / Log Viewer Routing
        else if (['txt', 'md', 'json', 'log'].includes(ext)) {
            this.openWindow('winMedia');
            document.querySelectorAll('.media-screen').forEach(el => el.classList.add('hidden'));
            document.getElementById('mediaBoxText').classList.remove('hidden');

            try {
                const text = await window.api.fs.readFile(filePath);
                document.getElementById('mediaTextContent').value = text;
            } catch (err) {
                this.showAlert("Error", `An error occurred loading text file: ${err.message}`);
            }
        }
        // 3. Video Playback Routing
        else if (['mp4', 'webm'].includes(ext)) {
            this.openWindow('winMedia');
            document.querySelectorAll('.media-screen').forEach(el => el.classList.add('hidden'));
            document.getElementById('mediaBoxVideo').classList.remove('hidden');

            const video = document.getElementById('mediaVideoPlayer');
            video.src = filePath;
            video.play();
            document.getElementById('vidPlayBtn').innerHTML = `<i class="fa-solid fa-pause"></i>`;
        }
        // 4. Audio Playback Routing
        else if (['mp3', 'wav'].includes(ext)) {
            this.openWindow('winMedia');
            document.querySelectorAll('.media-screen').forEach(el => el.classList.add('hidden'));
            document.getElementById('mediaBoxAudio').classList.remove('hidden');

            const audio = document.getElementById('mediaAudioPlayer');
            audio.src = filePath;
            audio.play();
            document.getElementById('audPlayBtn').innerHTML = `<i class="fa-solid fa-pause"></i>`;
            document.getElementById('audioDisc').style.animationPlayState = 'running';
        }
        // Default routing down to Monaco Code Editor IDE
        else {
            this.openWindow('winIde');
            OS_STATE.activeEditingFilePath = filePath;
            document.getElementById('ideActiveFilePath').textContent = filePath;

            try {
                const code = await window.api.fs.readFile(filePath);
                OS_STATE.monacoInstance.setValue(code);

                // Match syntax mode
                let language = 'javascript';
                if (ext === 'py') language = 'python';
                else if (ext === 'html') language = 'html';
                else if (ext === 'css') language = 'css';
                else if (ext === 'ts') language = 'typescript';
                else if (ext === 'cpp') language = 'cpp';
                else if (ext === 'json') language = 'json';

                monaco.editor.setModelLanguage(OS_STATE.monacoInstance.getModel(), language);
            } catch (err) {
                this.showAlert("Error", `An error occurred initializing source file: ${err.message}`);
            }
        }
    },

    // E. SETTINGS TAB MANAGER
    switchSettingsTab(tabId, tabItem) {
        // Switch nav selected styling
        document.querySelectorAll('.settings-tab-item').forEach(item => item.classList.remove('active'));
        tabItem.classList.add('active');

        // Toggle pane displays
        document.querySelectorAll('.settings-tab-pane').forEach(pane => pane.classList.add('hidden'));
        document.getElementById(tabId).classList.remove('hidden');
    },

    // TAB 2 VISUAL PREFERENCES CONFIG
    changeWallpaper(type, value) {
        OS_STATE.wallpaperType = type;
        OS_STATE.wallpaperVal = value;
        const desk = document.getElementById('desktopLayer');
        if (type === 'solid') {
            desk.style.background = value;
        } else {
            desk.style.background = value;
        }
    },

    triggerCustomWallpaperUpload() {
        document.getElementById('customWallpaperInput').click();
    },

    uploadCustomWallpaper(input) {
        if (input.files && input.files[0]) {
            const file = input.files[0];
            const url = URL.createObjectURL(file);
            this.changeWallpaper('image', `url(${url}) no-repeat center center / cover`);
            this.showAlert("Personalization", "Custom local host wallpaper image mounted successfully.", "fa-solid fa-image text-cyan");
        }
    },

    updateDockScale(val) {
        OS_STATE.dockScale = Number(val);
        document.getElementById('dockScaleLabel').textContent = `${val}px`;
        this.renderDesktopAndDock();
    },

    toggleDockMagnify(enabled) {
        OS_STATE.dockMagnify = enabled;
        this.renderDesktopAndDock();
    },

    toggleTransitionSpeed(speed) {
        OS_STATE.transitionSpeed = speed;
    },

    // TAB 3 NATIVE WINDOWS SHORTCUTS REGISTRATOR
    registerShortcutMapping() {
        const name = document.getElementById('mapAppName').value.trim();
        const path = document.getElementById('mapAppPath').value.trim();
        const icon = document.getElementById('mapAppIcon').value;

        if (!name || !path) {
            this.showAlert("Adapter Error", "Application signature name and local executables disk path are required fields.", "fa-solid fa-triangle-exclamation text-cyan");
            return;
        }

        const shortcutId = `custom-win-${Date.now()}`;
        const newApp = {
            id: shortcutId,
            titleKey: name,
            icon: icon,
            tooltipKey: name,
            isCustom: true,
            path: path
        };

        // Add to active states
        OS_STATE.customShortcuts.push(newApp);
        OS_STATE.pinnedDockApps.push(newApp);

        // Build dynamic container window block
        const container = document.getElementById('windowWorkbench');
        const customWin = document.createElement('div');
        customWin.id = shortcutId;
        customWin.className = 'os-window hidden';
        customWin.style.cssText = "width: 400px; height: 180px; top: 30%; left: 35%; z-index: 100;";
        customWin.innerHTML = `
            <div class="window-titlebar">
                <div class="window-controls">
                    <button class="win-btn win-close" onclick="OS.closeWindow('${shortcutId}')"></button>
                    <button class="win-btn win-max" onclick="OS.maximizeWindow('${shortcutId}')"></button>
                    <button class="win-btn win-min" onclick="OS.minimizeWindow('${shortcutId}', 'dock-${shortcutId}')"></button>
                </div>
                <div class="window-title-txt">
                    <i class="${icon} text-cyan"></i>
                    <span>${name}</span>
                </div>
            </div>
            <div class="window-body flex-col justify-center gap-12 padding-24 bg-darkblue">
                <p class="section-descr text-center">Execute native mapped host binary file:</p>
                <div class="dir-path-string text-center">${path}</div>
                <button class="action-bar-btn flex-center" onclick="OS.executeNativeHostBinary('${path}')">
                    <i class="fa-solid fa-rocket"></i>
                    <span>Launch Program</span>
                </button>
            </div>
        `;

        customWin.addEventListener('mousedown', () => this.bringToFront(shortcutId));
        this.makeWindowDraggable(customWin);

        container.appendChild(customWin);

        // Reset forms and rebuild layouts
        document.getElementById('mapAppName').value = '';
        document.getElementById('mapAppPath').value = '';
        this.renderDesktopAndDock();

        this.showAlert("Adapter Mapping", `Successfully mapped application shortcut: ${name}`, "fa-solid fa-circle-check text-cyan");
    },

    async executeNativeHostBinary(path) {
        if (!window.api || !window.api.system) {
            this.showAlert("Execution Adapter", "Native executable interface is only active in real Electron builds.", "fa-solid fa-triangle-exclamation text-cyan");
            return;
        }

        try {
            this.showAlert("Launching", `Initiating spawn thread sequence for: ${path}`, "fa-solid fa-circle-nodes text-cyan");
            const result = await window.api.system.execute(path);
            this.showAlert("Success", `Launch stream exited: ${result}`, "fa-solid fa-circle-check text-cyan");
        } catch (err) {
            this.showAlert("Execution Error", `Failed to spin binary thread: ${err}`, "fa-solid fa-triangle-exclamation text-cyan");
        }
    },

    // TAB 4 SYSTEM METRICS TELEMETRY
    initSystemMetrics() {
        const updateMetrics = async () => {
            if (!window.api || !window.api.system) return;
            try {
                const metrics = await window.api.system.getMetrics();

                // Top header bar indicators
                document.getElementById('menubarCpu').textContent = `CPU: ${metrics.cpu}%`;

                // Settings progress meters
                document.getElementById('telemetryCpuPct').textContent = `${metrics.cpu}%`;
                document.getElementById('telemetryCpuBar').style.width = `${metrics.cpu}%`;

                document.getElementById('telemetryRamText').textContent = `${metrics.ramUsed} / ${metrics.ramTotal} GB (${metrics.ramPercent}%)`;
                document.getElementById('telemetryRamBar').style.width = `${metrics.ramPercent}%`;
            } catch (err) {}
        };
        setInterval(updateMetrics, 2000);
    }
};

// Start system on page mount
document.addEventListener('DOMContentLoaded', () => {
    OS.init();
});
