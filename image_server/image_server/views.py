from django.http import HttpResponse, JsonResponse
import os
from django.views.decorators.csrf import csrf_exempt
import requests
from dotenv import load_dotenv

if os.name == "nt":  # Windows
    SAVE_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "images")
else:  # Linux (Ubuntu)
    SAVE_DIR = "/var/www/html/file"

def hello(request):
    return HttpResponse("hello world!!!@@@###")

def sayOs(request):
    return HttpResponse(SAVE_DIR)

def saveUploadedImage(image_file, filename):
    try:
        os.makedirs(SAVE_DIR, exist_ok=True)
        file_path = os.path.join(SAVE_DIR, filename)
        with open(file_path, "wb") as f:
                for chunk in image_file.chunks():
                    f.write(chunk)
        return file_path
    
    except Exception as e:
        print(f"이미지 저장 실패: {e}")
        return None
    
def checkAdmin(accessToken, refreshToken):
    print(accessToken)
    print(refreshToken)
    headers = {
        'Cookie': f'access={accessToken}; refresh={refreshToken}'
    }
    try:
        # 스프링 서버로 요청 보내기
        load_dotenv()
        springUrl = os.getenv("API_HOST")
        print(springUrl + "admin/test")
        response = requests.get(springUrl + "admin/test", headers=headers)

        if response.status_code == 200:
            return "success"
        else:
            return "not_admin"
    except requests.exceptions.RequestException as e:
        return "request_fail"

@csrf_exempt
def uploadImage(request):
    if request.method != "POST":
        return JsonResponse({"message": "잘못된 요청"}, status=400)
    
    isAdmin = checkAdmin(request.COOKIES.get("access"), request.COOKIES.get("refresh"))
    if isAdmin == "success":
        folderName = request.POST.get("folderName")
        if not folderName:
            return JsonResponse({"message": "폴더명이 필요합니다."}, status=400)
        saveDir = os.path.join(SAVE_DIR, folderName)
        os.makedirs(saveDir, exist_ok=True)
        files = request.FILES.getlist("images")
        if not files:
            return JsonResponse({"message": "이미지가 없습니다."}, status=400)
        savedFiles = []
        for index, file in enumerate(files, start=1):
            file_path = os.path.join(saveDir, f"{index}.jpg")

            # 파일을 디스크에 저장
            with open(file_path, "wb") as dest:
                for chunk in file.chunks():
                    dest.write(chunk)

            savedFiles.append(file_path)
        return JsonResponse({"message": "이미지 저장 성공", "saved_files": savedFiles})
    elif isAdmin == "not_admin":
        return JsonResponse({"message": "권한 없음"})
    elif isAdmin == "request_fail":
        return JsonResponse({"message": "서버 실패"})
