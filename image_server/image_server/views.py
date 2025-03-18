from django.http import HttpResponse
import os

if os.name == "nt":  # Windows
    SAVE_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "images")
else:  # Linux (Ubuntu)
    SAVE_DIR = "/var/www/html/images"

def hello(request):
    return HttpResponse("hello world!!!@@@")

def sayOs(request):
    return HttpResponse(SAVE_DIR)