const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods to renderer process
contextBridge.exposeInMainWorld('electronAPI', {
    // Platform info
    platform: process.platform,
    version: '2.0.0',
    
    // Get platform (for compatibility)
    getPlatform: () => process.platform,
    
    // CRITICAL: List directory contents - used by file browser
    listDirectory: (path) => {
        console.log('[Preload] listDirectory called:', path);
        return ipcRenderer.invoke('list-directory', path);
    },
    
    // Run shell command
    runCommand: (command) => {
        console.log('[Preload] runCommand called:', command);
        return ipcRenderer.invoke('run-command', command);
    },
    
    // Run Python script
    runPythonScript: (scriptName, args) => {
        console.log('[Preload] runPythonScript called:', scriptName, args);
        return ipcRenderer.invoke('run-python-script', scriptName, args);
    },
    
    // Open external URL in default browser
    openExternal: (url) => {
        console.log('[Preload] openExternal called:', url);
        return ipcRenderer.invoke('open-external', url);
    },
    
    // Open file with default application
    openFile: (filePath) => {
        console.log('[Preload] openFile called:', filePath);
        return ipcRenderer.invoke('open-file', filePath);
    },
    
    // Show file in folder (Explorer)
    showInFolder: (filePath) => {
        console.log('[Preload] showInFolder called:', filePath);
        return ipcRenderer.invoke('show-in-folder', filePath);
    },
    
    // File picker dialog
    showOpenDialog: (options) => {
        console.log('[Preload] showOpenDialog called');
        return ipcRenderer.invoke('show-open-dialog', options);
    },
    
    // Save dialog
    showSaveDialog: (options) => {
        console.log('[Preload] showSaveDialog called');
        return ipcRenderer.invoke('show-save-dialog', options);
    },
    
    // Read file contents
    readFile: (filePath) => {
        console.log('[Preload] readFile called:', filePath);
        return ipcRenderer.invoke('read-file', filePath);
    },
    
    // Write file contents
    writeFile: (filePath, content) => {
        console.log('[Preload] writeFile called:', filePath);
        return ipcRenderer.invoke('write-file', filePath, content);
    },
    
    // Get app info
    getAppInfo: () => {
        return ipcRenderer.invoke('get-app-info');
    },
    
    // Listen for script output (streaming)
    onScriptOutput: (callback) => {
        ipcRenderer.on('script-output', (event, data) => callback(data));
    },
    
    // Remove script output listener
    removeScriptOutputListener: () => {
        ipcRenderer.removeAllListeners('script-output');
    }
});

console.log('[Preload] electronAPI exposed to renderer');
console.log('[Preload] Available methods: listDirectory, runCommand, runPythonScript, openExternal, openFile, showInFolder, showOpenDialog, showSaveDialog, readFile, writeFile, getAppInfo');

// Expose Knowledge Base API
contextBridge.exposeInMainWorld('kb', {
    // Search knowledge base
    search: (query, options = {}) => {
        console.log('[Preload] kb.search:', query, options);
        return ipcRenderer.invoke('kb:search', query, options);
    },

    // List all document sources
    listSources: () => {
        console.log('[Preload] kb.listSources');
        return ipcRenderer.invoke('kb:listSources');
    },

    // Get document by URL
    getByUrl: (url) => {
        console.log('[Preload] kb.getByUrl:', url);
        return ipcRenderer.invoke('kb:getByUrl', url);
    },

    // Browse by source category
    browseBySource: (source, limit = 50) => {
        console.log('[Preload] kb.browseBySource:', source, limit);
        return ipcRenderer.invoke('kb:browseBySource', source, limit);
    },

    // Get recent documents
    getRecent: (limit = 20) => {
        console.log('[Preload] kb.getRecent:', limit);
        return ipcRenderer.invoke('kb:getRecent', limit);
    },

    // Get source categories
    getCategories: () => {
        console.log('[Preload] kb.getCategories');
        return ipcRenderer.invoke('kb:getCategories');
    },

    // Test connection
    testConnection: () => {
        console.log('[Preload] kb.testConnection');
        return ipcRenderer.invoke('kb:testConnection');
    }
});

console.log('[Preload] KB API exposed to renderer');
console.log('[Preload] KB methods: search, listSources, getByUrl, browseBySource, getRecent, getCategories, testConnection');
