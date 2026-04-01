from django.urls import path
from bookshelf.views import single_product
from bookshelf.apps import BookshelfConfig

app_name = BookshelfConfig.name

urlpatterns = [
    path("<slug:product_slug>/", single_product, name='single_product'),
]
