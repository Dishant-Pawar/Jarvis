const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');

function createWindow() {
  const win = new BrowserWindow({
    width: 1440,
    height: 900,
    frame: false,         // Borderless window
    transparent: true,   // Transparent backdrop
    alwaysOnTop: true,   // Keeps HUD floating on top of other apps
    resizable: true,
    hasShadow: false,
    webPreferences: {
      preload: path.join(__dirname, 'preload.cjs'),
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  // Load Vite dev server URL
  win.loadURL('http://localhost:5173');

  // Minimize app IPC Handler
  ipcMain.on('minimize-app', () => {
    win.minimize();
  });

  // Maximize app IPC Handler
  ipcMain.on('maximize-app', () => {
    if (win.isMaximized()) {
      win.unmaximize();
    } else {
      win.maximize();
    }
  });

  // Close app IPC Handler
  ipcMain.on('close-app', () => {
    app.quit();
  });
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
