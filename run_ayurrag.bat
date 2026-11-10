@echo off
title AyurRAG - Cross-Textual Ayurvedic Knowledge Retrieval
echo ======================================================================
echo   AyurRAG: Cross-Textual Ayurvedic Knowledge Retrieval System
echo   CMR College of Engineering & Technology - CSE Department
echo   B.Tech Major Project Phase-I
echo ======================================================================
echo.

set PROJECT_ROOT=%~dp0
cd /d "%PROJECT_ROOT%"

echo [1/2] Starting AyurRAG FastAPI Backend on http://127.0.0.1:8000 ...
start "AyurRAG Backend" cmd /k "cd /d %PROJECT_ROOT% && .\venv\Scripts\python.exe backend\run.py"

echo [2/2] Starting AyurRAG React/Vite Frontend on http://localhost:5173 ...
start "AyurRAG Frontend" cmd /k "cd /d %PROJECT_ROOT%\frontend && npm run dev"

echo.
echo ======================================================================
echo   AyurRAG is launching!
echo   Frontend: http://localhost:5173
echo   Backend Docs: http://127.0.0.1:8000/docs
echo ======================================================================
echo.
pause
