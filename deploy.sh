#!/bin/bash

VENV_PATH="./venv/bin/activate"

PID=$(lsof -t -i:9300)
if [ -n "$PID" ]; then
    echo "9300 포트에서 실행 중인 프로세스가 있습니다. PID: $PID"
    echo "프로세스를 종료합니다..."
    kill -9 $PID
else
    echo "9300 포트에서 실행 중인 프로세스가 없습니다."
fi

if [ -f "$VENV_PATH" ]; then
    echo "가상환경을 활성화합니다..."
    source "$VENV_PATH"
else
    echo "가상환경 파일이 존재하지 않습니다: $VENV_PATH"
    python3 -m venv myenv
    echo "가상환경을 활성화합니다..."
    source "$VENV_PATH"
fi

echo "의존성을 설치합니다..."
pip install -r requirements.txt

SCRIPT_DIR=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
echo "배포를 시작합니다..."
echo $SCRIPT_DIR
gunicorn --bind 0.0.0.0:8000 $SCRIPT_DIR/image_server.wsgi:application

if [ -f "$VENV_PATH" ]; then
    echo "가상환경을 비활성화합니다..."
    deactivate
fi