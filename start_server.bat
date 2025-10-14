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

waitress-serve --port=8000 sistemaAmbiental.wsgi:application

echo Servidor encerrado.
pause