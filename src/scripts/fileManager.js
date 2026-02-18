// Trajanus Enterprise Hub - File Manager

const FileManager = {
    files: [],
    selectedFiles: new Set(),
    storageKey: 'trajanus_files',

    init: function(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) return;

        this.loadFiles();
        this.render();
        this.setupDragDrop();
    },

    loadFiles: function() {
        const toolkit = this.getCurrentToolkit();
        const stored = localStorage.getItem(`${this.storageKey}_${toolkit}`);
        if (stored) {
            this.files = JSON.parse(stored);
        }
    },

    saveFiles: function() {
        const toolkit = this.getCurrentToolkit();
        localStorage.setItem(`${this.storageKey}_${toolkit}`, JSON.stringify(this.files));
    },

    getCurrentToolkit: function() {
        const path = window.location.pathname;
        if (path.includes('pm.html')) return 'pm';
        if (path.includes('traffic.html')) return 'traffic';
        if (path.includes('developer.html')) return 'developer';
        if (path.includes('qcm.html')) return 'qcm';
        return 'default';
    },

    render: function() {
        this.container.innerHTML = `
            <h2>Document Browser</h2>
            <div class="panel-content">
                <div class="upload-area" id="upload-area">
                    <input type="file" id="file-input" multiple style="display: none;">
                    <p>Drop files here or click to upload</p>
                </div>
                <div class="file-list" id="file-list">
                    ${this.renderFileList()}
                </div>
            </div>
        `;

        this.setupEventListeners();
    },

    renderFileList: function() {
        if (this.files.length === 0) {
            return '<p class="placeholder">No documents uploaded</p>';
        }

        return this.files.map((file, index) => `
            <div class="file-item" data-index="${index}">
                <input type="checkbox"
                       ${this.selectedFiles.has(index) ? 'checked' : ''}
                       onchange="FileManager.toggleSelection(${index})">
                <div class="file-info">
                    <span class="file-name" title="${file.name}">${file.name}</span>
                    <span class="file-meta">${this.formatFileSize(file.size)} - ${this.formatDate(file.added)}</span>
                </div>
                <button class="file-delete" onclick="FileManager.deleteFile(${index})" title="Delete">X</button>
            </div>
        `).join('');
    },

    setupEventListeners: function() {
        const uploadArea = document.getElementById('upload-area');
        const fileInput = document.getElementById('file-input');

        if (uploadArea) {
            uploadArea.addEventListener('click', () => fileInput.click());
        }

        if (fileInput) {
            fileInput.addEventListener('change', (e) => this.handleFiles(e.target.files));
        }
    },

    setupDragDrop: function() {
        const uploadArea = document.getElementById('upload-area');
        if (!uploadArea) return;

        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
            });
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.classList.add('dragover');
            });
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.classList.remove('dragover');
            });
        });

        uploadArea.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            this.handleFiles(files);
        });
    },

    handleFiles: function(fileList) {
        Array.from(fileList).forEach(file => {
            // Read file content
            const reader = new FileReader();
            reader.onload = (e) => {
                const fileData = {
                    name: file.name,
                    size: file.size,
                    type: file.type || this.getFileType(file.name),
                    added: new Date().toISOString(),
                    content: e.target.result
                };
                this.files.push(fileData);
                this.saveFiles();
                this.render();
                this.setupDragDrop();
            };
            reader.readAsText(file);
        });
    },

    getFileType: function(filename) {
        const ext = filename.split('.').pop().toLowerCase();
        const types = {
            'pdf': 'application/pdf',
            'doc': 'application/msword',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'txt': 'text/plain',
            'md': 'text/markdown',
            'json': 'application/json',
            'csv': 'text/csv'
        };
        return types[ext] || 'text/plain';
    },

    toggleSelection: function(index) {
        if (this.selectedFiles.has(index)) {
            this.selectedFiles.delete(index);
        } else {
            this.selectedFiles.add(index);
        }
        this.updateContextIndicator();
    },

    deleteFile: function(index) {
        this.files.splice(index, 1);
        this.selectedFiles.delete(index);
        // Reindex selected files
        const newSelected = new Set();
        this.selectedFiles.forEach(i => {
            if (i > index) newSelected.add(i - 1);
            else if (i < index) newSelected.add(i);
        });
        this.selectedFiles = newSelected;
        this.saveFiles();
        this.render();
        this.setupDragDrop();
        this.updateContextIndicator();
    },

    getSelectedContent: function() {
        const content = [];
        this.selectedFiles.forEach(index => {
            if (this.files[index]) {
                content.push({
                    name: this.files[index].name,
                    content: this.files[index].content
                });
            }
        });
        return content;
    },

    updateContextIndicator: function() {
        const indicator = document.getElementById('context-indicator');
        if (indicator) {
            const count = this.selectedFiles.size;
            indicator.innerHTML = count > 0
                ? `Context: <span>${count} document${count > 1 ? 's' : ''} selected</span>`
                : 'No documents selected for context';
        }
    },

    formatFileSize: function(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    },

    formatDate: function(isoString) {
        const date = new Date(isoString);
        return date.toLocaleDateString();
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('document-browser')) {
        FileManager.init('document-browser');
    }
});
