const {app, BrowserWindow} = require("electron");

function ElectronMainMethod() {
    const launchWindow = new BrowserWindow({
        title: "App Processamento de Imagem",
        width: 777,
        height: 444,
    });

    const appURL = "http://localhost:8000";

    launchWindow.loadURL(appURL);

}

app.whenReady().then(ElectronMainMethod);