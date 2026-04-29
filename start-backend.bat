@echo off
title Optimizar Backend
cd /d "%~dp0backend"
echo ============================
echo   Optimizar - Backend (FastAPI)
echo   http://localhost:8000
echo   Docs: http://localhost:8000/docs
echo ============================
echo.
echo Instalando dependencias...
pip install -r requirements.txt -q
echo.
echo Iniciando servidor...
python run.py
pause
