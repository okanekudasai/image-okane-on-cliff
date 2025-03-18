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
    
    

    save_dir = os.path.join(SAVE_DIR, request.POST.get("folderName"))
    return HttpResponse(save_dir)
    # if request.method == "POST" and request.FILES.get("image"):
    #     image_file = request.FILES["image"]
    #     file_path = saveUploadedImage(image_file, image_file.name)
    #     if file_path:
    #         return JsonResponse({"message": "이미지 저장 성공", "file_path": file_path})
    #     else:
    #         return JsonResponse({"message": "이미지 저장 실패"}, status=500)
    
    # return JsonResponse({"message": "잘못된 요청"}, status=400)