const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods to the renderer process
contextBridge.exposeInMainWorld('electronAPI', {// Read text file
readTextFile: (filePath) => ipcRenderer.invoke('read-text-file', filePath),
    // Run Python scripts
    runPythonScript: (scriptName, args) => ipcRenderer.invoke('run-python-script', scriptName, args),
    
    // Listen for real-time script output
    onScriptOutput: (callback) => ipcRenderer.on('script-output', (event, data) => callback(data)),
    
    // Remove script output listener
    removeScriptOutputListener: () => ipcRenderer.removeAllListeners('script-output'),
    
    // File picker
    selectFiles: (options) => ipcRenderer.invoke('select-files', options),
    
    // Open external URL
    openExternal: (url) => ipcRenderer.invoke('open-external', url),
    
    // Get directory contents
    getDirectoryContents: (path) => ipcRenderer.invoke('get-directory-contents', path),
    
    // App info
    platform: process.platform,
    version: '1.0.0'
});
