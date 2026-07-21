const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  fs: {
    readDir: (dirPath) => ipcRenderer.invoke('fs:readDir', dirPath),
    readFile: (filePath) => ipcRenderer.invoke('fs:readFile', filePath),
    writeFile: (filePath, content) => ipcRenderer.invoke('fs:writeFile', filePath, content),
    exists: (filePath) => ipcRenderer.invoke('fs:exists', filePath),
    getHomeDir: () => ipcRenderer.invoke('fs:getHomeDir'),
    getTempPath: (relativePath) => ipcRenderer.invoke('fs:getTempPath', relativePath)
  },
  system: {
    getMetrics: () => ipcRenderer.invoke('system:metrics'),
    execute: (executablePath) => ipcRenderer.invoke('sys:exec', executablePath)
  },
  terminal: {
    init: () => ipcRenderer.send('terminal:init'),
    write: (data) => ipcRenderer.send('terminal:write', data),
    onIncoming: (callback) => {
      const wrappedCallback = (event, data) => callback(data);
      ipcRenderer.on('terminal:incoming', wrappedCallback);
      return () => ipcRenderer.removeListener('terminal:incoming', wrappedCallback);
    }
  }
});
