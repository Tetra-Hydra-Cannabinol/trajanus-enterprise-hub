const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

// Keep a global reference of the window object
let mainWindow;

// Working directory for Python scripts
const SCRIPTS_DIR = 'G:\\My Drive\\00 - Trajanus USA\\00-Command-Center';

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1400,
        height: 900,
        minWidth: 1000,
        minHeight: 700,
        title: 'Trajanus Command Center',
        icon: path.join(__dirname, 'assets', 'icon.png'),
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            nodeIntegration: false
        },
        backgroundColor: '#1a365d',
        show: false
    });

    mainWindow.loadFile('index.html');
    
    mainWindow.once('ready-to-show', () => {
        mainWindow.show();
    });

    // Open DevTools in development (comment out for production)
    // mainWindow.webContents.openDevTools();

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
// IPC HANDLERS - Communication with renderer
// ============================================

// Run a Python script and stream output back
ipcMain.handle('run-python-script', async (event, scriptName, args = []) => {
    return new Promise((resolve, reject) => {
        const scriptPath = path.join(SCRIPTS_DIR, scriptName);
        
        // Build the command with properly quoted paths
        // Quote the script path and each argument to handle spaces
        const quotedArgs = args.map(arg => `"${arg}"`);
        const fullCommand = `python "${scriptPath}" ${quotedArgs.join(' ')}`;
        
        console.log(`Running: ${fullCommand}`);
        
        const python = spawn(fullCommand, [], {
            cwd: SCRIPTS_DIR,
            shell: true
        });

        let output = '';
        let errorOutput = '';

        python.stdout.on('data', (data) => {
            const text = data.toString();
            output += text;
            // Send real-time output to renderer
            mainWindow.webContents.send('script-output', text);
        });

        python.stderr.on('data', (data) => {
            const text = data.toString();
            errorOutput += text;
            mainWindow.webContents.send('script-output', `ERROR: ${text}`);
        });

        python.on('close', (code) => {
            if (code === 0) {
                resolve({ success: true, output });
            } else {
                resolve({ success: false, output, error: errorOutput, code });
            }
        });

        python.on('error', (err) => {
            reject(err);
        });
    });
});

// File picker dialog
ipcMain.handle('select-files', async (event, options) => {
    const result = await dialog.showOpenDialog(mainWindow, {
        properties: ['openFile', 'multiSelections'],
        filters: options.filters || [
            { name: 'Markdown Files', extensions: ['md'] },
            { name: 'All Files', extensions: ['*'] }
        ],
        defaultPath: SCRIPTS_DIR
    });
    return result.filePaths;
});

// Folder picker dialog
ipcMain.handle('select-folder', async (event, options) => {
    const result = await dialog.showOpenDialog(mainWindow, {
        properties: ['openDirectory'],
        defaultPath: options.defaultPath || SCRIPTS_DIR
    });
    return result.filePaths[0] || null;
});

// Open external URL
ipcMain.handle('open-external', async (event, url) => {
    const { shell } = require('electron');
    await shell.openExternal(url);
});

// Get working directory contents
ipcMain.handle('get-directory-contents', async (event, dirPath) => {
    const fs = require('fs').promises;
    try {
        const files = await fs.readdir(dirPath);
        return files;
    } catch (err) {
        return [];
    }
});

// Save file dialog
ipcMain.handle('save-file', async (event, options) => {
    const result = await dialog.showSaveDialog(mainWindow, {
        defaultPath: options.defaultPath || SCRIPTS_DIR,
        filters: options.filters || [
            { name: 'All Files', extensions: ['*'] }
        ]
    });
    return result.filePath || null;
});
