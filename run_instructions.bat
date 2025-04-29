@echo off
REM Step 1: Create virtual environment
python -m venv venv

REM Step 2: Activate virtual environment
call venv\Scripts\activate.bat

REM Step 3: Upgrade pip
python -m pip install --upgrade pip

REM Step 4: Install dependencies
pip install -r requirements.txt

REM Step 5: Run FastAPI server
uvicorn app:app --reload
