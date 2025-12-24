const { app, BrowserWindow, ipcMain, shell, dialog } = require('electron');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

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

console.log('Trajanus Enterprise Hub - Main process initialized');
