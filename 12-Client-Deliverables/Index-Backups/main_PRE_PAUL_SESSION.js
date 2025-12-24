const { app, BrowserWindow, ipcMain, shell } = require('electron');
const { exec } = require('child_process');
const path = require('path');

let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1800,
        height: 1000,
        backgroundColor: '#1f1410',
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            nodeIntegration: false
        },
        icon: path.join(__dirname, 'assets', 'icon.png') // Optional
    });

    mainWindow.loadFile('index.html');

    // Open DevTools in development
    mainWindow.webContents.openDevTools({ mode: 'right' });

    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

// App ready
app.whenReady().then(createWindow);

// Quit when all windows closed (except macOS)
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
// IPC HANDLERS - APP LAUNCHERS (PROVEN TO WORK)
// ============================================

ipcMain.handle('run-command', async (event, command) => {
    return new Promise((resolve, reject) => {
        exec(command, {
            shell: 'powershell.exe',
            cwd: 'G:\\My Drive\\00 - Trajanus USA\\00-Command-Center'
        }, (error, stdout, stderr) => {
            if (error) {
                console.error('Command error:', error);
                reject(error);
            } else {
                console.log('Command output:', stdout);
                resolve({ success: true, output: stdout });
            }
        });
    });
});

// Open external links in default browser
ipcMain.handle('open-external', async (event, url) => {
    await shell.openExternal(url);
    return { success: true };
});

// Get platform info
ipcMain.handle('get-platform', async () => {
    return {
        platform: process.platform,
        arch: process.arch,
        version: process.version
    };
});

// File picker
ipcMain.handle('pick-files', async (event, options) => {
    const { dialog } = require('electron');
    const result = await dialog.showOpenDialog(mainWindow, {
        properties: ['openFile', 'multiSelections'],
        filters: options?.filters || [
            { name: 'All Files', extensions: ['*'] },
            { name: 'Documents', extensions: ['pdf', 'docx', 'xlsx', 'pptx', 'txt', 'md'] }
        ]
    });

    if (!result.canceled && result.filePaths.length > 0) {
        return {
            success: true,
            files: result.filePaths.map(path => {
                const fs = require('fs');
                const stats = fs.statSync(path);
                return {
                    path: path,
                    name: require('path').basename(path),
                    size: stats.size,
                    modified: stats.mtime
                };
            })
        };
    }

    return { success: false, files: [] };
});

// List directory contents (NEW)
ipcMain.handle('list-directory', async (event, dirPath) => {
    const fs = require('fs');
    const pathModule = require('path');
    
    try {
        const items = fs.readdirSync(dirPath, { withFileTypes: true });
        const files = items.map(item => {
            const fullPath = pathModule.join(dirPath, item.name);
            let stats = null;
            try {
                stats = fs.statSync(fullPath);
            } catch (e) {
                // Skip files we can't stat
            }
            return {
                name: item.name,
                isDirectory: item.isDirectory(),
                path: fullPath,
                size: stats ? stats.size : 0,
                modified: stats ? stats.mtime : null
            };
        });
        return { success: true, files };
    } catch (error) {
        console.error('List directory error:', error);
        return { success: false, error: error.message, files: [] };
    }
});

console.log('Trajanus Enterprise Hub v2.0 - Electron main process ready');
