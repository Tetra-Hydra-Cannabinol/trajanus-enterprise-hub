/**
 * KB Browser Component - Trajanus Command Center
 * Two-tab video browser: Office Videos, Claude Tutorials
 * Created: 2026-01-18
 * Updated: 2026-01-18 - Simplified to 2 video categories
 */

class KBBrowserComponent {
    constructor(containerId, config = {}) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.error(`KBBrowserComponent: Container '${containerId}' not found`);
            return;
        }

        this.config = {
            platformName: config.platformName || 'enterprise',
            sectionTitle: config.sectionTitle || 'KNOWLEDGE BASE',
            officeTabLabel: config.officeTabLabel || 'Office Videos',
            claudeTabLabel: config.claudeTabLabel || 'Claude Tutorials',
            supabaseUrl: 'https://iaxtwrswinygwwwdkvok.supabase.co',
            supabaseKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlheHR3cnN3aW55Z3d3d2Rrdm9rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjUyOTc4NjAsImV4cCI6MjA4MDg3Mzg2MH0.JGSdki3TtDiRS7OQrpBDuyN4nxPW1Qc9ImMunnjHFoE',
            ...config
        };

        this.activeTab = 'office';
        this.items = [];
        this.selectedItem = null;
        this.isLoading = false;

        this.injectStyles();
        this.render();
        this.loadContent();
    }

    // ==================== URL PATTERN DETECTION ====================

    isYouTubeUrl(url) {
        if (!url) return false;
        return url.includes('youtube.com') || url.includes('youtu.be');
    }

    extractVideoId(url) {
        if (!url) return null;
        const patterns = [
            /youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})/,
            /youtu\.be\/([a-zA-Z0-9_-]{11})/,
            /youtube\.com\/embed\/([a-zA-Z0-9_-]{11})/,
            /youtube\.com\/v\/([a-zA-Z0-9_-]{11})/
        ];
        for (const pattern of patterns) {
            const match = url.match(pattern);
            if (match) return match[1];
        }
        return null;
    }

    getThumbnailUrl(videoId) {
        return `https://img.youtube.com/vi/${videoId}/mqdefault.jpg`;
    }

    // ==================== DATA FETCHING ====================

    async fetchData(queryParams) {
        const url = `${this.config.supabaseUrl}/rest/v1/knowledge_base?${queryParams}`;
        try {
            const response = await fetch(url, {
                headers: {
                    'apikey': this.config.supabaseKey,
                    'Authorization': `Bearer ${this.config.supabaseKey}`,
                    'Content-Type': 'application/json'
                }
            });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('KBBrowser fetch error:', error);
            return [];
        }
    }

    async fetchOfficeVideos() {
        // MS Office videos: category = Microsoft_Office OR application contains Excel/Word/PowerPoint
        // Using title patterns as fallback since metadata varies
        const params = [
            'or=(url.ilike.*youtube.com*,url.ilike.*youtu.be*)',
            'chunk_number=eq.1',
            'or=(metadata->>category.eq.Microsoft_Office,metadata->>application.ilike.*Excel*,metadata->>application.ilike.*Word*,metadata->>application.ilike.*PowerPoint*,title.ilike.*Excel*,title.ilike.*Word*,title.ilike.*PowerPoint*,title.ilike.*Office*,metadata->>channel.eq.MyOnlineTrainingHub)',
            'order=title.asc',
            'limit=100'
        ].join('&');
        return this.fetchData(params);
    }

    async fetchClaudeVideos() {
        // Claude tutorials: category = DEV OR source contains Claude OR title contains Claude
        const params = [
            'or=(url.ilike.*youtube.com*,url.ilike.*youtu.be*)',
            'chunk_number=eq.1',
            'or=(metadata->>category.eq.DEV,metadata->>source.ilike.*Claude*,title.ilike.*Claude*)',
            'order=created_at.desc',
            'limit=100'
        ].join('&');
        return this.fetchData(params);
    }

    async loadContent() {
        this.isLoading = true;
        this.renderThumbnailList();

        switch (this.activeTab) {
            case 'office':
                this.items = await this.fetchOfficeVideos();
                break;
            case 'claude':
                this.items = await this.fetchClaudeVideos();
                break;
        }

        this.isLoading = false;
        this.selectedItem = null;
        this.renderThumbnailList();
        this.renderDetailPanel();
    }

    // ==================== RENDERING ====================

    render() {
        this.container.innerHTML = `
            <div class="kb-browser-panel">
                <!-- Tab Buttons -->
                <div class="kb-tabs">
                    <button class="kb-tab-btn ${this.activeTab === 'office' ? 'active' : ''}" data-tab="office">
                        <span class="kb-tab-icon">&#128202;</span>
                        ${this.config.officeTabLabel}
                    </button>
                    <button class="kb-tab-btn ${this.activeTab === 'claude' ? 'active' : ''}" data-tab="claude">
                        <span class="kb-tab-icon">&#129302;</span>
                        ${this.config.claudeTabLabel}
                    </button>
                </div>

                <!-- Content Area -->
                <div class="kb-content-area">
                    <!-- Thumbnail List (Left Panel) -->
                    <div class="kb-thumbnail-panel" id="kb-thumbnail-panel-${this.config.platformName}">
                        <div class="kb-loading">Loading...</div>
                    </div>

                    <!-- Detail Panel (Right Panel) -->
                    <div class="kb-detail-panel" id="kb-detail-panel-${this.config.platformName}">
                        <div class="kb-empty-state">
                            <div class="kb-empty-icon">&#128218;</div>
                            <div>Select a video to view details</div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Attach tab event listeners
        this.container.querySelectorAll('.kb-tab-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.activeTab = btn.dataset.tab;
                this.container.querySelectorAll('.kb-tab-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                this.loadContent();
            });
        });
    }

    renderThumbnailList() {
        const panel = this.container.querySelector(`#kb-thumbnail-panel-${this.config.platformName}`);
        if (!panel) return;

        if (this.isLoading) {
            panel.innerHTML = '<div class="kb-loading">Loading...</div>';
            return;
        }

        if (this.items.length === 0) {
            panel.innerHTML = `
                <div class="kb-empty-state">
                    <div class="kb-empty-icon">&#128269;</div>
                    <div>No videos found</div>
                </div>
            `;
            return;
        }

        // All items are videos - render with thumbnails
        panel.innerHTML = this.items.map((item, index) => {
            const videoId = this.extractVideoId(item.url);
            const thumbUrl = videoId ? this.getThumbnailUrl(videoId) : '';
            return `
                <div class="kb-thumbnail-item ${this.selectedItem === item ? 'selected' : ''}" data-index="${index}">
                    <div class="kb-thumbnail-img-wrapper">
                        ${thumbUrl
                            ? `<img class="kb-thumbnail-img" src="${thumbUrl}" alt="${this.escapeHtml(item.title)}" onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 320 180%22><rect fill=%22%23333%22 width=%22320%22 height=%22180%22/><text x=%22160%22 y=%2290%22 text-anchor=%22middle%22 fill=%22%23888%22 font-size=%2240%22>&#9654;</text></svg>'">`
                            : `<div class="kb-thumbnail-placeholder">&#9654;</div>`
                        }
                    </div>
                    <div class="kb-thumbnail-title">${this.escapeHtml(item.title || 'Untitled')}</div>
                </div>
            `;
        }).join('');

        // Attach click handlers
        panel.querySelectorAll('.kb-thumbnail-item').forEach(el => {
            el.addEventListener('click', () => {
                const index = parseInt(el.dataset.index);
                this.selectItem(this.items[index]);
            });
        });
    }

    renderDetailPanel() {
        const panel = this.container.querySelector(`#kb-detail-panel-${this.config.platformName}`);
        if (!panel) return;

        if (!this.selectedItem) {
            panel.innerHTML = `
                <div class="kb-empty-state">
                    <div class="kb-empty-icon">&#128218;</div>
                    <div>Select a video to view details</div>
                </div>
            `;
            return;
        }

        const item = this.selectedItem;
        const videoId = this.extractVideoId(item.url);
        const category = this.activeTab === 'office' ? 'MS Office Tutorial' : 'Claude Tutorial';

        // Extract metadata for display
        const metadata = item.metadata || {};
        const channel = metadata.channel || '';
        const duration = metadata.duration || '';
        const level = metadata.level || '';

        panel.innerHTML = `
            <div class="kb-detail-title">${this.escapeHtml(item.title || 'Untitled')}</div>
            <div class="kb-detail-meta">
                <div><strong>Type:</strong> ${category}</div>
                ${channel ? `<div><strong>Channel:</strong> ${this.escapeHtml(channel)}</div>` : ''}
                ${duration ? `<div><strong>Duration:</strong> ${this.escapeHtml(duration)}</div>` : ''}
                ${level ? `<div><strong>Level:</strong> ${this.escapeHtml(level)}</div>` : ''}
            </div>
            <div class="kb-detail-summary">
                ${item.summary ? this.escapeHtml(item.summary) : (item.content ? this.escapeHtml(item.content.substring(0, 500)) + '...' : 'No description available.')}
            </div>
            <div class="kb-detail-actions">
                ${videoId
                    ? `<button class="kb-action-btn kb-action-primary" onclick="kbBrowsers['${this.config.platformName}'].openVideo('${videoId}', '${this.escapeHtml(item.title).replace(/'/g, "\\'")}')">
                        <span>&#9654;</span> Watch Video
                       </button>`
                    : `<button class="kb-action-btn kb-action-secondary" disabled>Video unavailable</button>`
                }
            </div>
        `;
    }

    // ==================== ACTIONS ====================

    selectItem(item) {
        this.selectedItem = item;

        // Update selection UI
        this.container.querySelectorAll('.kb-thumbnail-item').forEach(el => {
            el.classList.remove('selected');
        });
        const index = this.items.indexOf(item);
        const selectedEl = this.container.querySelector(`.kb-thumbnail-item[data-index="${index}"]`);
        if (selectedEl) selectedEl.classList.add('selected');

        this.renderDetailPanel();
    }

    openVideo(videoId, title) {
        // Use TrajnausWindow if available, otherwise create modal
        try {
            if (typeof TrajnausWindow !== 'undefined' && TrajnausWindow.prototype) {
                const iframe = `<iframe width="100%" height="500" src="https://www.youtube.com/embed/${videoId}?autoplay=1" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`;
                new TrajnausWindow({
                    title: title || 'Video',
                    content: iframe,
                    width: '1000px'
                }).show();
                return;
            }
        } catch (e) {
            console.log('TrajnausWindow not available, using fallback modal');
        }
        // Fallback: create simple modal
        this.showVideoModal(videoId, title);
    }

    showVideoModal(videoId, title) {
        const overlay = document.createElement('div');
        overlay.className = 'kb-video-overlay';
        overlay.innerHTML = `
            <div class="kb-video-modal">
                <div class="kb-video-header">
                    <div class="kb-video-title">${this.escapeHtml(title || 'Video')}</div>
                    <button class="kb-video-close">&times;</button>
                </div>
                <div class="kb-video-body">
                    <iframe width="100%" height="500" src="https://www.youtube.com/embed/${videoId}?autoplay=1" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                </div>
            </div>
        `;
        document.body.appendChild(overlay);

        // Close handlers
        overlay.querySelector('.kb-video-close').addEventListener('click', () => overlay.remove());
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) overlay.remove();
        });
        document.addEventListener('keydown', function handler(e) {
            if (e.key === 'Escape') {
                overlay.remove();
                document.removeEventListener('keydown', handler);
            }
        });
    }

    // ==================== UTILITIES ====================

    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // ==================== STYLES ====================

    injectStyles() {
        if (document.getElementById('kb-browser-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'kb-browser-styles';
        styles.textContent = `
            /* KB Browser Panel */
            .kb-browser-panel {
                background: #0a0a0a;
                border: 2px solid #0066CC;
                border-radius: 8px;
                overflow: hidden;
            }

            /* Tab Buttons */
            .kb-tabs {
                display: flex;
                gap: 0;
                background: #111;
                border-bottom: 2px solid #0066CC;
            }

            .kb-tab-btn {
                flex: 1;
                padding: 14px 20px;
                background: transparent;
                border: none;
                border-right: 1px solid #333;
                color: #888;
                font-size: 14px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
            }

            .kb-tab-btn:last-child {
                border-right: none;
            }

            .kb-tab-btn:hover {
                background: #1a1a1a;
                color: #c0c0c0;
            }

            .kb-tab-btn.active {
                background: #0a1929;
                color: #00AAFF;
                border-bottom: 2px solid #00AAFF;
                margin-bottom: -2px;
            }

            .kb-tab-icon {
                font-size: 16px;
            }

            /* Content Area */
            .kb-content-area {
                display: grid;
                grid-template-columns: 35% 65%;
                height: 400px;
                max-height: 400px;
                overflow: hidden;
            }

            /* Thumbnail Panel (Left) - Hidden Scrollbar */
            .kb-thumbnail-panel {
                background: #0d0d0d;
                border-right: 1px solid #333;
                overflow-y: scroll;
                overflow-x: hidden;
                padding: 12px;
                height: 100%;
                max-height: 400px;
                scrollbar-width: none; /* Firefox */
                -ms-overflow-style: none; /* IE/Edge */
            }

            .kb-thumbnail-panel::-webkit-scrollbar {
                display: none; /* Chrome/Safari/Opera */
            }

            /* Thumbnail Items */
            .kb-thumbnail-item {
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 10px;
                margin-bottom: 8px;
                background: #111;
                border: 1px solid #222;
                border-radius: 6px;
                cursor: pointer;
                transition: all 0.2s ease;
            }

            .kb-thumbnail-item:hover {
                background: #1a1a1a;
                border-color: #444;
            }

            .kb-thumbnail-item.selected {
                background: #0a1929;
                border-color: #00AAFF;
            }

            .kb-thumbnail-img-wrapper {
                flex-shrink: 0;
                width: 120px;
                height: 68px;
                background: #222;
                border-radius: 4px;
                overflow: hidden;
            }

            .kb-thumbnail-img {
                width: 100%;
                height: 100%;
                object-fit: cover;
            }

            .kb-thumbnail-placeholder {
                width: 100%;
                height: 100%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
                color: #666;
                background: #1a1a1a;
            }

            .kb-thumbnail-title {
                font-size: 13px;
                color: #c0c0c0;
                line-height: 1.4;
                overflow: hidden;
                text-overflow: ellipsis;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
            }

            /* Detail Panel (Right) - Hidden Scrollbar */
            .kb-detail-panel {
                padding: 20px;
                overflow-y: scroll;
                overflow-x: hidden;
                background: #0a0a0a;
                height: 100%;
                max-height: 400px;
                scrollbar-width: none; /* Firefox */
                -ms-overflow-style: none; /* IE/Edge */
            }

            .kb-detail-panel::-webkit-scrollbar {
                display: none; /* Chrome/Safari/Opera */
            }

            .kb-detail-title {
                font-size: 20px;
                font-weight: 600;
                color: #00AAFF;
                margin-bottom: 12px;
                line-height: 1.3;
            }

            .kb-detail-meta {
                display: flex;
                flex-wrap: wrap;
                gap: 16px;
                margin-bottom: 16px;
                font-size: 13px;
                color: #888;
            }

            .kb-detail-meta strong {
                color: #aaa;
            }

            .kb-detail-summary {
                font-size: 14px;
                color: #c0c0c0;
                line-height: 1.6;
                margin-bottom: 20px;
                padding: 16px;
                background: #111;
                border-radius: 6px;
                border: 1px solid #222;
                max-height: 200px;
                overflow-y: auto;
                scrollbar-width: none; /* Firefox */
                -ms-overflow-style: none; /* IE/Edge */
            }

            .kb-detail-summary::-webkit-scrollbar {
                display: none; /* Chrome/Safari/Opera */
            }

            .kb-detail-actions {
                display: flex;
                gap: 12px;
            }

            .kb-action-btn {
                padding: 12px 24px;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                gap: 8px;
            }

            .kb-action-primary {
                background: linear-gradient(135deg, #00AAFF 0%, #0088CC 100%);
                color: #fff;
            }

            .kb-action-primary:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0, 170, 255, 0.3);
            }

            .kb-action-secondary {
                background: #333;
                color: #888;
            }

            /* Empty & Loading States */
            .kb-empty-state {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100%;
                min-height: 200px;
                color: #666;
                text-align: center;
            }

            .kb-empty-icon {
                font-size: 48px;
                margin-bottom: 12px;
                opacity: 0.5;
            }

            .kb-loading {
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100%;
                min-height: 200px;
                color: #00AAFF;
                font-size: 14px;
            }

            /* Video Modal Overlay */
            .kb-video-overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.85);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 10000;
                animation: kbOverlayFadeIn 0.2s ease;
            }

            @keyframes kbOverlayFadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }

            .kb-video-modal {
                background: #111;
                border: 2px solid #00AAFF;
                border-radius: 12px;
                width: 90%;
                max-width: 1000px;
                overflow: hidden;
                box-shadow: 0 20px 60px rgba(0, 170, 255, 0.2);
                animation: kbModalSlideIn 0.3s ease;
            }

            @keyframes kbModalSlideIn {
                from { transform: translateY(-20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }

            .kb-video-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 16px 20px;
                background: linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%);
                border-bottom: 1px solid #333;
            }

            .kb-video-title {
                font-size: 16px;
                font-weight: 600;
                color: #c0c0c0;
            }

            .kb-video-close {
                width: 32px;
                height: 32px;
                border: none;
                background: #333;
                color: #888;
                font-size: 20px;
                border-radius: 6px;
                cursor: pointer;
                transition: all 0.2s ease;
            }

            .kb-video-close:hover {
                background: #444;
                color: #fff;
            }

            .kb-video-body {
                padding: 0;
                background: #000;
            }

            .kb-video-body iframe {
                display: block;
            }
        `;
        document.head.appendChild(styles);
    }
}

// Global registry for KB browsers (needed for onclick handlers)
window.kbBrowsers = window.kbBrowsers || {};
