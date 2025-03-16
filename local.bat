@echo off

call venv\Scripts\activate
call venv\Scripts\python "%~dp0\image_server\manage.py" runserver 9300
deactivate

pause