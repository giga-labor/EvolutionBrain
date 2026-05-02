@echo off
setlocal
cd /d "%~dp0"
if not exist .venv (
  py -m venv .venv
)
call .venv\Scripts\activate
python -m pip install --upgrade pip >nul
if exist requirements.txt (
  pip install -r requirements.txt
) else (
  pip install -e .
)
echo Starting EvoBrain Zero backend on http://127.0.0.1:8000
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
endlocal
