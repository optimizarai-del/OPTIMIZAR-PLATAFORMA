@echo off
title Optimizar Seed
cd /d "%~dp0backend"
echo ============================
echo   Optimizar - Seed de datos demo
echo ============================
echo.
python -m app.seed
echo.
echo Seed completado. Podés cerrar esta ventana.
pause
