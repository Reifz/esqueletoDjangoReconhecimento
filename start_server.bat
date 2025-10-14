@echo off
echo ==================================================
echo    INICIANDO SERVIDOR DJANGO COM WAITRESS
echo ==================================================
echo.
echo    Projeto: sistemaAmbiental
echo    Porta: 8000
echo.
echo    Pressione CTRL+C na janela do servidor para parar.
echo.

REM Inicia o servidor Waitress em segundo plano
start "" cmd /c "waitress-serve --host=127.0.0.1 --port=8000 sistemaAmbiental.wsgi:application"

REM Aguarda 2 segundos para garantir que o servidor subiu
timeout /t 2 /nobreak > nul

REM Abre o navegador padrão com a URL do servidor
start "" "http://127.0.0.1:8000/"

echo Servidor iniciado. Feche esta janela para parar.
pause