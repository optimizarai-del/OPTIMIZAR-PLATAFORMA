@echo off
title Optimizar Frontend
cd /d "%~dp0frontend"
echo ============================
echo   Optimizar - Frontend (Vite + React)
echo   http://localhost:5173
echo ============================
echo.
echo Instalando dependencias...
call npm install
echo.
echo Iniciando servidor...
call npm run dev
pause
