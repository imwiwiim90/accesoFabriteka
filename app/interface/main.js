  const {app, BrowserWindow, Menu, MenuItem, dialog} = require('electron')
  const url = require('url')
  const path = require('path')

  const exec = require('child_process').exec;
  const { spawn } = require('child_process');

  // Keep a global reference of the window object, if you don't, the window will
  // be closed automatically when the JavaScript object is garbage collected.
  let win
  
  function createWindow () {
    // Create the browser window.
    win = new BrowserWindow({width: 800, height: 600})
  
    // and load the index.html of the app.
    win.loadFile('index.html')
  
    // Open the DevTools.
    win.webContents.openDevTools()
  
    // Emitted when the window is closed.
    win.on('closed', () => {
      // Dereference the window object, usually you would store windows
      // in an array if your app supports multi windows, this is the time
      // when you should delete the corresponding element.
      win = null
    })
  }
  
  // This method will be called when Electron has finished
  // initialization and is ready to create browser windows.
  // Some APIs can only be used after this event occurs.
  app.on('ready', () => {
    setMainMenu();
    createWindow();
    activateAPI();
  })
  
  // Quit when all windows are closed.
  app.on('window-all-closed', () => {
    // On macOS it is common for applications and their menu bar
    // to stay active until the user quits explicitly with Cmd + Q
    if (process.platform !== 'darwin') {
      app.quit()
    }
  })
  
  app.on('activate', () => {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (win === null) {
      createWindow()
    }
  })
  
  // In this file you can include the rest of your app's specific main process
  // code. You can also put them in separate files and require them here. 



function setMainMenu() {
  const menuTemplate = [
    {
        label: "Electron",
        submenu: [{role: 'TODO'}]
    },
    {
      label: 'Archivo',
      submenu: [
        {
            label: 'Exportar',
            click: () => {
              dialog.showSaveDialog(function (fileName) {
                  const python_command = "python -c 'import sys; sys.path.insert(0,\"../python_logic/app/modules/\"); from accesoFabriteka import *; exportarDatos(\""+fileName+ ".xlsx" +"\")'"

                  const child = exec(python_command,
                    (error, stdout, stderr) => {
                        console.log(`stdout: ${stdout}`);
                        console.log(`stderr: ${stderr}`);
                        if (error !== null) {
                            console.log(`exec error: ${error}`);
                        }
                  });
              });
            }
        }
      ]
    },
    {
        label: "Empleados",
        submenu: [
          {
            label: 'Nuevo',
            click: () => {
              win.loadFile('new_employee.html')
            },
          },
          {
            label: 'Cambiar Tarjeta',
            click: () => {
              win.loadFile('employee_change_card.html')
            },
          },

        ]
    },
    {
        label: "Usuarios",
        submenu: [
          {
            label: 'Entrada',
            click: () => {
              win.loadFile('entrance.html')
            },
          },
          {
            label: 'Salida',
            click: () => {
              win.loadFile('exit.html')
            },
          },
          {
            label: 'Perdida',
            click: () => {
              win.loadFile('client_change_card.html')
            },
          },
        ]
    },
  ];
  Menu.setApplicationMenu(Menu.buildFromTemplate(menuTemplate));
}

function activateAPI() {
      const python_command = "export FLASK_APP=../python_logic/python_logic.py && flask run"
      const child = spawn('bash',['test.sh']);

      child.stdout.setEncoding('utf8');
      child.stdout.on('data',console.log);
      child.stderr.setEncoding('utf8');
      child.stderr.on('data',console.log);
      child.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
      });
     
}

