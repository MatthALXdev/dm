from django.urls import path
from .views import health, hello, home, root

urlpatterns = [
    path("", root, name="root"),
    path("home/", home, name="home"),
    path("health", health, name="health"),
    path("hello", hello, name="hello"),
]