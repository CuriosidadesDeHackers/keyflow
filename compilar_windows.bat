@echo off
REM Script para compilar Keyflow en Windows (.exe)
REM Uso: doble clic o ejecutar en CMD

setlocal EnableDelayedExpansion

REM Habilitar colores ANSI en Windows 10+
for /F %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"

REM Definir colores
set "RESET=%ESC%[0m"
set "BOLD=%ESC%[1m"
set "RED=%ESC%[91m"
set "GREEN=%ESC%[92m"
set "YELLOW=%ESC%[93m"
set "BLUE=%ESC%[94m"
set "MAGENTA=%ESC%[95m"
set "CYAN=%ESC%[96m"
set "WHITE=%ESC%[97m"
set "BG_BLUE=%ESC%[44m"
set "BG_GREEN=%ESC%[42m"
set "BG_RED=%ESC%[41m"

REM Limpiar pantalla
cls

echo.
echo %BG_BLUE%%WHITE%%BOLD%  ========================================  %RESET%
echo %BG_BLUE%%WHITE%%BOLD%     Keyflow - Compilador Windows (.exe)    %RESET%
echo %BG_BLUE%%WHITE%%BOLD%  ========================================  %RESET%
echo.

REM Configurar variables
set "EXE_NAME=keyflow.exe"
set "DIST_FOLDER=dist"
set "BUILD_FOLDER=build"
set "SPEC_FILE=keyflow.spec"

REM Limpiar builds anteriores
echo %CYAN%[INFO]%RESET% Limpiando archivos temporales...
if exist "%DIST_FOLDER%" rmdir /s /q "%DIST_FOLDER%"
if exist "%BUILD_FOLDER%" rmdir /s /q "%BUILD_FOLDER%"
if exist "%SPEC_FILE%" del /q "%SPEC_FILE%"
echo %GREEN%  [OK]%RESET% Limpieza completada
echo.

REM Verificar dependencias
echo %MAGENTA%%BOLD%[1/3]%RESET% %WHITE%Verificando dependencias...%RESET%
pip show PySide6-Essentials cryptography pykeepass >nul 2>&1
if %errorlevel% neq 0 (
    echo %YELLOW%  [!]%RESET% Faltan dependencias, instalando...
    pip install -r requirements.txt
) else (
    echo %GREEN%  [OK]%RESET% Dependencias ya instaladas
)

REM Instalar PyInstaller si no esta presente
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo %YELLOW%  [!]%RESET% Instalando PyInstaller...
    pip install pyinstaller
)
echo.

REM Compilar ejecutable
echo %MAGENTA%%BOLD%[2/3]%RESET% %WHITE%Compilando ejecutable con PyInstaller...%RESET%
echo %CYAN%      Esto puede tardar unos minutos...%RESET%
echo.
pyinstaller --onefile --windowed --icon=assets\logo.png --name=keyflow --clean main.py
if %errorlevel% neq 0 (
    echo.
    echo %BG_RED%%WHITE%%BOLD%  [ERROR]  %RESET% %RED%La compilacion fallo. Revisa los mensajes anteriores.%RESET%
    pause
    exit /b 1
)
echo.

REM Verificar resultado
echo %MAGENTA%%BOLD%[3/3]%RESET% %WHITE%Verificando resultado...%RESET%
if exist "%DIST_FOLDER%\%EXE_NAME%" (
    echo %GREEN%  [OK]%RESET% Ejecutable creado exitosamente
    echo.
    echo %BG_GREEN%%WHITE%%BOLD%  ========================================  %RESET%
    echo %BG_GREEN%%WHITE%%BOLD%            COMPILACION EXITOSA             %RESET%
    echo %BG_GREEN%%WHITE%%BOLD%  ========================================  %RESET%
    echo.
    echo %CYAN%  Ejecutable:%RESET% %WHITE%%BOLD%%DIST_FOLDER%\%EXE_NAME%%RESET%
    
    REM Calcular tamano con formato legible
    for %%I in ("%DIST_FOLDER%\%EXE_NAME%") do (
        set "size=%%~zI"
        set /a "sizeMB=%%~zI / 1024 / 1024"
        echo %CYAN%  Tamano:%RESET%     %GREEN%!sizeMB! MB%RESET% ^(!size! bytes^)
    )
    echo.
    echo %YELLOW%  Para ejecutar:%RESET%
    echo     %WHITE%%DIST_FOLDER%\%EXE_NAME%%RESET%
    echo.
    echo %YELLOW%  Para distribuir, incluye:%RESET%
    echo     %WHITE%- %DIST_FOLDER%\%EXE_NAME%%RESET%
    echo.
    echo %CYAN%  NOTA:%RESET% Si el icono no aparece, reinicia el explorador.
    echo.
    
    REM Preguntar si quiere abrir la carpeta
    echo %MAGENTA%  Quieres abrir la carpeta dist? ^(S/N^)%RESET%
    set /p "openFolder="
    if /i "!openFolder!"=="S" (
        explorer "%DIST_FOLDER%"
    )
) else (
    echo.
    echo %BG_RED%%WHITE%%BOLD%  ==========================================  %RESET%
    echo %BG_RED%%WHITE%%BOLD%              ERROR CRITICO                   %RESET%
    echo %BG_RED%%WHITE%%BOLD%  ==========================================  %RESET%
    echo.
    echo %RED%  No se encontro el ejecutable final en:%RESET%
    echo %WHITE%    %DIST_FOLDER%\%EXE_NAME%%RESET%
    echo.
    echo %YELLOW%  Revisa los logs de PyInstaller para mas detalles.%RESET%
    pause
    exit /b 1
)

echo.
echo %GREEN%%BOLD%  Proceso completado!%RESET%
echo.
endlocal
pause