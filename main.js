const { app, BrowserWindow, ipcMain, shell, dialog } = require('electron');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');
const kbService = require('./services/kb-service');

let mainWindow;

// Base paths
const SCRIPTS_DIR = 'G:\\My Drive\\00 - Trajanus USA\\00-Command-Center\\05-Scripts';

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1600,
        height: 1000,
        minWidth: 1200,
        minHeight: 800,
        title: 'Trajanus Enterprise Hub',
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            nodeIntegration: false
        },
        backgroundColor: '#1a1a2e',
        show: false
    });

    mainWindow.loadFile('index.html');
    
    // Open DevTools automatically for debugging
    mainWindow.webContents.openDevTools();
    
    mainWindow.once('ready-to-show', () => {
        mainWindow.show();
    });

    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});

// ============================================
// IPC HANDLERS
// ============================================

// List directory contents - THIS IS THE CRITICAL ONE FOR FILE BROWSER
ipcMain.handle('list-directory', async (event, dirPath) => {
    console.log('[Main] list-directory called with:', dirPath);
    
    try {
        // Check if directory exists
        if (!fs.existsSync(dirPath)) {
            console.log('[Main] Directory does not exist:', dirPath);
            return { success: false, error: `Directory not found: ${dirPath}`, files: [] };
        }
        
        const items = fs.readdirSync(dirPath, { withFileTypes: true });
        const files = [];
        
        for (const item of items) {
            const fullPath = path.join(dirPath, item.name);
            let stats = null;
            
            try {
                stats = fs.statSync(fullPath);
            } catch (e) {
                console.log('[Main] Could not stat:', fullPath);
                continue;
            }
            
            files.push({
                name: item.name,
                isDirectory: item.isDirectory(),
                path: fullPath,
                size: stats ? stats.size : 0,
                modified: stats ? stats.mtime.toISOString() : null
            });
        }
        
        // Sort: folders first, then files, alphabetically
        files.sort((a, b) => {
            if (a.isDirectory && !b.isDirectory) return -1;
            if (!a.isDirectory && b.isDirectory) return 1;
            return a.name.localeCompare(b.name);
        });
        
        console.log('[Main] list-directory success, found', files.length, 'items');
        return { success: true, files };
        
    } catch (error) {
        console.error('[Main] list-directory error:', error);
        return { success: false, error: error.message, files: [] };
    }
});

// Run shell command
ipcMain.handle('run-command', async (event, command) => {
    console.log('[Main] run-command:', command);
    return new Promise((resolve) => {
        const child = spawn('cmd.exe', ['/c', command], {
            cwd: SCRIPTS_DIR
        });
        
        let stdout = '';
        let stderr = '';
        
        child.stdout.on('data', (data) => {
            stdout += data.toString();
        });
        
        child.stderr.on('data', (data) => {
            stderr += data.toString();
        });
        
        child.on('close', (code) => {
            resolve({ code, stdout, stderr });
        });
        
        child.on('error', (err) => {
            resolve({ code: -1, stdout: '', stderr: err.message });
        });
    });
});

// Run Python script
ipcMain.handle('run-python-script', async (event, scriptName, args = []) => {
    console.log('[Main] run-python-script:', scriptName, args);
    
    const scriptPath = path.join(SCRIPTS_DIR, scriptName);
    
    return new Promise((resolve) => {
        const child = spawn('python', [scriptPath, ...args], {
            cwd: SCRIPTS_DIR
        });
        
        let stdout = '';
        let stderr = '';
        
        child.stdout.on('data', (data) => {
            stdout += data.toString();
            // Send streaming output to renderer
            if (mainWindow && !mainWindow.isDestroyed()) {
                mainWindow.webContents.send('script-output', data.toString());
            }
        });
        
        child.stderr.on('data', (data) => {
            stderr += data.toString();
        });
        
        child.on('close', (code) => {
            resolve({ success: code === 0, code, stdout, stderr });
        });
        
        child.on('error', (err) => {
            resolve({ success: false, code: -1, stdout: '', stderr: err.message });
        });
    });
});

// Open external URL
ipcMain.handle('open-external', async (event, url) => {
    console.log('[Main] open-external:', url);
    await shell.openExternal(url);
    return { success: true };
});

// Open file with default application
ipcMain.handle('open-file', async (event, filePath) => {
    console.log('[Main] open-file:', filePath);
    try {
        await shell.openPath(filePath);
        return { success: true };
    } catch (error) {
        return { success: false, error: error.message };
    }
});

// Show file in folder
ipcMain.handle('show-in-folder', async (event, filePath) => {
    console.log('[Main] show-in-folder:', filePath);
    shell.showItemInFolder(filePath);
    return { success: true };
});

// File picker dialog
ipcMain.handle('show-open-dialog', async (event, options) => {
    console.log('[Main] show-open-dialog');
    const result = await dialog.showOpenDialog(mainWindow, options);
    return result;
});

// Save dialog
ipcMain.handle('show-save-dialog', async (event, options) => {
    console.log('[Main] show-save-dialog');
    const result = await dialog.showSaveDialog(mainWindow, options);
    return result;
});

// Read file
ipcMain.handle('read-file', async (event, filePath) => {
    console.log('[Main] read-file:', filePath);
    try {
        const content = fs.readFileSync(filePath, 'utf8');
        return { success: true, content };
    } catch (error) {
        return { success: false, error: error.message };
    }
});

// Write file
ipcMain.handle('write-file', async (event, filePath, content) => {
    console.log('[Main] write-file:', filePath);
    try {
        fs.writeFileSync(filePath, content, 'utf8');
        return { success: true };
    } catch (error) {
        return { success: false, error: error.message };
    }
});

// Get app info
ipcMain.handle('get-app-info', async () => {
    return {
        version: app.getVersion(),
        platform: process.platform,
        arch: process.arch,
        nodeVersion: process.versions.node,
        electronVersion: process.versions.electron
    };
});

// ============================================
// KNOWLEDGE BASE IPC HANDLERS
// ============================================

// KB: Search knowledge base
ipcMain.handle('kb:search', async (event, query, options = {}) => {
    console.log('[Main] kb:search:', query, options);
    try {
        const results = await kbService.search(query, options);
        return { success: true, data: results };
    } catch (error) {
        console.error('[Main] kb:search error:', error);
        return { success: false, error: error.message };
    }
});

// KB: List all sources
ipcMain.handle('kb:listSources', async () => {
    console.log('[Main] kb:listSources');
    try {
        const results = await kbService.listSources();
        return { success: true, data: results };
    } catch (error) {
        console.error('[Main] kb:listSources error:', error);
        return { success: false, error: error.message };
    }
});

// KB: Get document by URL
ipcMain.handle('kb:getByUrl', async (event, url) => {
    console.log('[Main] kb:getByUrl:', url);
    try {
        const results = await kbService.getByUrl(url);
        return { success: true, data: results };
    } catch (error) {
        console.error('[Main] kb:getByUrl error:', error);
        return { success: false, error: error.message };
    }
});

// KB: Browse by source category
ipcMain.handle('kb:browseBySource', async (event, source, limit = 50) => {
    console.log('[Main] kb:browseBySource:', source, limit);
    try {
        const results = await kbService.browseBySource(source, limit);
        return { success: true, data: results };
    } catch (error) {
        console.error('[Main] kb:browseBySource error:', error);
        return { success: false, error: error.message };
    }
});

// KB: Get recent documents
ipcMain.handle('kb:getRecent', async (event, limit = 20) => {
    console.log('[Main] kb:getRecent:', limit);
    try {
        const results = await kbService.getRecent(limit);
        return { success: true, data: results };
    } catch (error) {
        console.error('[Main] kb:getRecent error:', error);
        return { success: false, error: error.message };
    }
});

// KB: Get source categories
ipcMain.handle('kb:getCategories', async () => {
    console.log('[Main] kb:getCategories');
    try {
        const results = await kbService.getSourceCategories();
        return { success: true, data: results };
    } catch (error) {
        console.error('[Main] kb:getCategories error:', error);
        return { success: false, error: error.message };
    }
});

// KB: Test connection
ipcMain.handle('kb:testConnection', async () => {
    console.log('[Main] kb:testConnection');
    try {
        const result = await kbService.testConnection();
        return { success: true, data: result };
    } catch (error) {
        console.error('[Main] kb:testConnection error:', error);
        return { success: false, error: error.message };
    }
});

console.log('Trajanus Enterprise Hub - Main process initialized');
