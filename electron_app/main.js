// Electron 진입점 

// index.html을 데스크탑 창에 띄워주는 역할

// Electron에서 제공하는 모듈을 가져옴
// app: Electron 앱 전체의 수명 관리(시작/종료 등)
// BrowserWindow: 실제로 사용자에게 보여지는 window 객체를 만드는 클래스
const {app, BrowserWindow} = require('electron')

// createWindow()는 새 창을 만들고 index.html라는 웹페이지를 그 안에 띄워준다.
const createWindow = () => {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
    })

    win.loadFile('index.html')
}

// app.on(...) => 이벤트 리스너

app.whenReady().then(() => {
    // Electron 앱이 완전히 준비되면 createWindow() 실행.
    createWindow()

    // 그리고 Mac에서는 창이 닫혔다가 아이콘 클릭해서 다시 열면 다시 띄워주게 함.
    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) createWindow()
    })
})

// windows나 linux에선 모든 창이 닫히면 앱 종료
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit()
})