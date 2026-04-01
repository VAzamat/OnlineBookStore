from django.shortcuts import render, get_object_or_404
from .models import Book
from django.conf import settings

used_skin = settings.USED_SKIN


def single_product(request, product_slug):
    # Ищем товар по полю slug, которое мы заполнили через pytils
    book = get_object_or_404(Book, slug=product_slug)
    return render(request, f'{used_skin}/single_product.html',
    {'product': book}
    )
