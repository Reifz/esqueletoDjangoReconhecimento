@echo off
echo ==================================================
echo    TENTANDO PARAR O SERVIDOR NA PORTA 8000
echo ==================================================
echo.

for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do (
    echo Encontrado processo com PID %%a na porta 8000.
    echo Encerrando processo...
    taskkill /F /PID %%a
)

echo.
echo Verificacao concluida.
echo ==================================================
pause
