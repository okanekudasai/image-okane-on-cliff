@echo off

set "command=python"
call %command% "%~dp0\image_server\manage.py" runserver 9300

pause