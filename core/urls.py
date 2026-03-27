from django.urls import path
from core.views import index, shop

from core.apps import CoreConfig

app_name = CoreConfig.name

urlpatterns = [
    path("", index, name='index'),
    path("shop.html", shop, name='shop'),
]
