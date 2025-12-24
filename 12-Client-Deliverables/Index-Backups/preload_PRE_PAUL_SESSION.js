const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods to renderer process
contextBridge.exposeInMainWorld('electronAPI', {
    // Run commands (app launchers)
    runCommand: (command) => ipcRenderer.invoke('run-command', command),

    // Open external URLs
    openExternal: (url) => ipcRenderer.invoke('open-external', url),

    // Get platform info
    getPlatform: () => ipcRenderer.invoke('get-platform'),

    // File picker
    pickFiles: (options) => ipcRenderer.invoke('pick-files', options),

    // List directory contents (NEW)
    listDirectory: (path) => ipcRenderer.invoke('list-directory', path)
});

console.log('Preload script loaded - electronAPI exposed');
