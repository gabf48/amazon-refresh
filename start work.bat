@echo off
cd /d F:\amazon\amazon-refresh\script
call ..\.venv\Scripts\activate
python test_script.py
pause