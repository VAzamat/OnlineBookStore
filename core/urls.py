from django.urls import path
from core.views import index, shop, single_product, blog, blog_with_sidebar

from core.apps import CoreConfig

app_name = CoreConfig.name

urlpatterns = [
    path("", index, name='index'),
    path("shop.html", shop, name='shop'),
    path("single_product.html", single_product, name='single_product'),
    path("blog.html", blog, name='blog'),
    path("blog_with_sidebar.html", blog_with_sidebar),
]
