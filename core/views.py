from django.shortcuts import render, get_object_or_404
from django.conf import settings

from bookshelf.models import Product, Book

used_skin = settings.USED_SKIN



# Create your views here.
def home(request):
    return render(request, 'test_home.html')

def index(request):
    products_best_selling = Product.objects.get_best_sellers(max_count=10)
    product_new_arrivals = Product.objects.get_new_arrivals(max_count=4)
    product_recommendations = Product.objects.get_random_featured(max_count=4)

    return render(request, f'{used_skin}/index.html',
                  {'products_best_selling': products_best_selling,
                   'product_new_arrivals': product_new_arrivals,
                   'product_recommendations': product_recommendations}
                  )


def shop(request):
    return render(request, f'{used_skin}/shop.html')

def single_product(request, product_slug):
    # Ищем товар по полю slug, которое мы заполнили через pytils
    product = get_object_or_404(Product, slug=product_slug)
    related_products = Product.objects.get_related(current_slug=product_slug, max_count=4)
    featured_books = Product.objects.get_random_featured(max_count=3)
    return render(request, f'{used_skin}/single_product.html',
    {'product': product, 'products_related': related_products }
    )


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

def faqs(request):
    return render(request, f'{used_skin}/faqs.html')

def author(request):
    return render(request, f'{used_skin}/author.html')

def styles(request):
    return render(request, f'{used_skin}/styles.html')

def thanks(request):
    return render(request, f'{used_skin}/thanks.html')

def comming_soon(request):
    return render(request, f'{used_skin}/comming_soon.html')

def error_page(request):
    return render(request, f'{used_skin}/error_page.html')

def order_tracking(request):
    return render(request, f'{used_skin}/order_tracking.html')
