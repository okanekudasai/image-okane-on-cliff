from django.http import HttpResponse, JsonResponse
import os
from django.views.decorators.csrf import csrf_exempt

if os.name == "nt":  # Windows
    SAVE_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "images")
else:  # Linux (Ubuntu)
    SAVE_DIR = "/var/www/html/file"

def hello(request):
    return HttpResponse("hello world!!!@@@")

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
    
@csrf_exempt
def uploadImage(request):
    if request.method != "POST":
        return JsonResponse({"message": "잘못된 요청"}, status=400)
    
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
    # if request.method == "POST" and request.FILES.get("image"):
    #     image_file = request.FILES["image"]
    #     file_path = saveUploadedImage(image_file, image_file.name)
    #     if file_path:
    #         return JsonResponse({"message": "이미지 저장 성공", "file_path": file_path})
    #     else:
    #         return JsonResponse({"message": "이미지 저장 실패"}, status=500)
    
    # return JsonResponse({"message": "잘못된 요청"}, status=400)