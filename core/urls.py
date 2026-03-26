from django.urls import path
from core.views import home

from core.apps import CoreConfig

app_name = CoreConfig.name

urlpatterns = [
    path("", home, name='home'),
]
