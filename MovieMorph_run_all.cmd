@echo off
:: MovieMorph_run_all.cmd
:: Recorrerá todos los archivos .mkv, .mp4, .avi en %USERPROFILE%\Downloads\Movies
:: y llamará a MovieMorph.py para procesarlos.

echo ===============================================
echo   MovieMorph - Postprocesado masivo
echo ===============================================
echo.

set "CARPETA_MOVIES=%USERPROFILE%\Downloads\Movies"

:: Se asegura que la carpeta Movies exista
if not exist "%CARPETA_MOVIES%" (
    echo Creando carpeta "%CARPETA_MOVIES%"...
    mkdir "%CARPETA_MOVIES%"
)

cd /d "%CARPETA_MOVIES%"

:: Recorre recursivamente los archivos de vídeo
for /r %%F in (*.mkv *.mp4 *.avi) do (
    echo Procesando: %%F
    python "C:\scripts\MovieMorph.py" "%%F"
)

echo.
echo ===============================================
echo   PROCESO MASIVO FINALIZADO
echo ===============================================
pause
