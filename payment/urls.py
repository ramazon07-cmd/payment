from django.urls import path
from .views import FakeClickAPIView, FakePaymeAPIView

urlpatterns = [
    path("click/", FakeClickAPIView.as_view(), name="fake-click"),
    path("payme/", FakePaymeAPIView.as_view(), name="fake-payme"),
]
