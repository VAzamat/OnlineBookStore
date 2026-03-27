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

def blog(request):
    return render(request, f'{used_skin}/blog.html')

def blog_with_sidebar(request):
    return render(request, f'{used_skin}/blog_with_sidebar.html')

def blog_single_post(request):
    return render(request, f'{used_skin}/single_post.html')

def contacts(request):
    return render(request, f'{used_skin}/contact.html')

def about_us(request):
    return render(request, f'{used_skin}/about_us.html')

def my_account(request):
    return render(request, f'{used_skin}/my_account.html')

def cart(request):
    return render(request, f'{used_skin}/cart.html')

def checkout(request):
    return render(request, f'{used_skin}/checkout.html')

def classes(request):
    return render(request, f'{used_skin}/class.html')

def class_detail(request):
    return render(request, f'{used_skin}/class_detail.html')

def pricing(request):
    return render(request, f'{used_skin}/pricing.html')

def wishlist(request):
    return render(request, f'{used_skin}/wishlist.html')
