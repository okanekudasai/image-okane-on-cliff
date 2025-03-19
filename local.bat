@echo off

:: 가상 환경 활성화
call venv\Scripts\activate

:: 두 번째 서버 실행 (Python HTTP 서버) - 백그라운드 실행
start python -m http.server 8000 --directory "C:/Users/xpc/Desktop/images"

:: 첫 번째 서버 실행 (Django) - 순차적으로 실행
call venv\Scripts\python "%~dp0\image_server\manage.py" runserver 9300

:: 비활성화
deactivate

pause
