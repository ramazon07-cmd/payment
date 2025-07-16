from django.urls import path
from .views import fake_click, fake_payme

urlpatterns = [
    path("click/", fake_click),
    path("payme/", fake_payme),
]
