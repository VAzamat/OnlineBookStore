from django.urls import path
from core.views import index, shop, single_product, blog, blog_with_sidebar, blog_single_post
from core.views import contacts, about_us, cart, my_account, checkout, classes, class_detail
from core.views import pricing, wishlist, faqs, author
from core.apps import CoreConfig

app_name = CoreConfig.name

urlpatterns = [
    path("", index, name='index'),
    path("shop.html", shop, name='shop'),
    path("single_product.html", single_product, name='single_product'),
    path("blog.html", blog, name='blog'),
    path("blog_with_sidebar.html", blog_with_sidebar, name='blog_with_sidebar'),
    path("single_post.html", blog_single_post, name='single_post'),
    path("contacts.html", contacts, name='contacts'),
    path("about_us.html", about_us, name='about_us'),
    path("cart.html", cart, name='cart'),
    path("my_account.html", my_account, name='my_account'),
    path("checkout.html", checkout, name='checkout'),
    path("classes.html", classes, name='classes'),
    path("class_detail.html", class_detail, name='class_detail'),
    path("pricing.html", pricing, name='pricing'),
    path("wishlist.html", wishlist, name='wishlist'),
    path("faqs.html", faqs, name='faqs'),
    path("author.html", author, name='author'),
]
