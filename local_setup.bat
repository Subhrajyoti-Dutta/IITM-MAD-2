@echo off
REM Create a virtual environment
python -m venv .venv

REM Activate the virtual environment
call .venv\Scripts\activate

REM Upgrade pip and setuptools
python -m pip install --upgrade pip setuptools

REM Install the required packages
pip install -r requirements.txt

echo Virtual environment setup complete and packages installed.