from django.urls import path
from core.views import index, shop, single_product, blog, blog_with_sidebar, blog_single_post

from core.apps import CoreConfig

app_name = CoreConfig.name

urlpatterns = [
    path("", index, name='index'),
    path("shop.html", shop, name='shop'),
    path("single_product.html", single_product, name='single_product'),
    path("blog.html", blog, name='blog'),
    path("blog_with_sidebar.html", blog_with_sidebar, name='blog_with_sidebar'),
    path("single_post.html", blog_single_post, name='single_post'),
]
