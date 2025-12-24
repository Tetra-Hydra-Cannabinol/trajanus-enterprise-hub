const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

// Keep a global reference of the window object
let mainWindow;

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
        // Nice window styling
        backgroundColor: '#1a365d',
        show: false // Don't show until ready
    });

    mainWindow.loadFile('index.html');
    
    // Show when ready to prevent white flash
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
        const workingDir = 'G:\\My Drive\\00 - Trajanus USA\\00-Command-Center';
        const scriptPath = path.join(workingDir, scriptName);
        
        // Quote the script path to handle spaces in directory names
        const python = spawn('python', [`"${scriptPath}"`, ...args], {
            cwd: workingDir,
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
        defaultPath: 'G:\\My Drive\\00 - Trajanus USA\\00-Command-Center'
    });
    return result.filePaths;
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
