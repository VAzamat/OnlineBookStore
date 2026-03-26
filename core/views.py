from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'test_home.html')

def index(request):
    return render(request, 'skin1/index.html')
