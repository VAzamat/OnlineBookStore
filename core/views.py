from django.shortcuts import render
from django.conf import settings

used_skin = settings.USED_SKIN

# Create your views here.
def home(request):
    return render(request, 'test_home.html')

def index(request):
    return render(request, f'{used_skin}/index.html')

def shop(request):
    return render(request, f'{used_skin}/shop.html')

def single_product(request):
    return render(request, f'{used_skin}/single_product.html')
