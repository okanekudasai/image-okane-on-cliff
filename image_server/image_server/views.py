from django.http import HttpResponse, JsonResponse
import os
from django.views.decorators.csrf import csrf_exempt
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup


if os.name == "nt":  # Windows
    SAVE_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "images")
else:  # Linux (Ubuntu)
    SAVE_DIR = "/var/www/html/file"

load_dotenv()
springUrl = os.getenv("API_HOST")
LOAD_DIR = os.getenv("LOAD_DIR")

def hello(request):
    print("hello")
    return HttpResponse("hello world!")

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
    headers = {
        'Cookie': f'access={accessToken}; refresh={refreshToken}'
    }
    try:
        # 스프링 서버로 요청 보내기
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
    print("왔음!")
    if request.method != "POST":
        return JsonResponse({"message": "잘못된 요청"}, status=400)
    
    isAdmin = checkAdmin(request.COOKIES.get("access"), request.COOKIES.get("refresh"))
    if isAdmin.msg == "success":
        folderName = isAdmin.docNumber
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

            savedFiles.append(os.path.join(LOAD_DIR, f"{index}.jpg"))
        return JsonResponse({"message": "이미지 저장 성공", "saved_files": savedFiles})
    elif isAdmin == "not_admin":
        return JsonResponse({"message": "권한 없음"})
    elif isAdmin == "request_fail":
        return JsonResponse({"message": "서버 실패"})

@csrf_exempt
def fetchArticle(request):
    if request.method != "POST":
        return JsonResponse({"message": "잘못된 요청"}, status=400)
    
    accessToken = request.COOKIES.get("access")
    refreshToken = request.COOKIES.get("refresh")
    
    title = request.POST.get("title")
    category = request.POST.get("category")
    html = request.POST.get("html")
    tags = request.POST.getlist("tags")
    content = request.POST.get("content")
    files = request.FILES.getlist("images")
    # 이 코드블록엔 도달할 수 없음 이미 클라이언트에서 image의 숫자를 판단하는 로직이 있음
    if len(files) == 0:
        return HttpResponse("잘못된 요청")
    
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'access={accessToken}; refresh={refreshToken}'
    }
    
    data = {
        "categoryId": category,
        "title": title,
        "tags": tags,
        "shortContent": content
    }

    try:
        response = requests.post(springUrl + "article/admin/doc", json=data, headers=headers)
        print(response.json())
        folderName = response.json()
    except:
        return JsonResponse({"message": "writing error"}, status=400)

    try:
        #이 코드블럭에는 도달 할 일이 없음
        if not folderName:
            return JsonResponse({"message": "doc not founded"}, status=400)
        
        saveDir = os.path.join(SAVE_DIR, str(folderName))
        os.makedirs(saveDir, exist_ok=True)
        savedFiles = []
        for index, file in enumerate(files):
            file_path = os.path.join(saveDir, f"{index}.jpg")

            # 파일을 디스크에 저장
            with open(file_path, "wb") as dest:
                for chunk in file.chunks():
                    dest.write(chunk)

            savedFiles.append(os.path.join(LOAD_DIR, str(folderName), f"{index}.jpg"))

        soup = BeautifulSoup(html, 'html.parser')
        img_tags = soup.find_all('img')
        image_index = 0
        for img_tag in enumerate(img_tags):
            if not img_tag[1]['src'].startswith("newData:image/"): continue
            if index < len(savedFiles):
                img_tag[1]['src'] = savedFiles[image_index]
                image_index += 1

        data = {
            "html": str(soup)
        }
        try:
            requests.post(springUrl + f"article/admin/doc/{folderName}", json=data, headers=headers)
        except:
            response = requests.delete(springUrl + f"article/admin/{folderName}", headers=headers)
            return JsonResponse({"message": "writing error"}, status=400)

    except:
        print("안됨!2")
        requests.delete(springUrl + f"article/admin/{folderName}", headers=headers)
        return JsonResponse({"message": "writing error"}, status=400)

    return JsonResponse({"message": "success"})