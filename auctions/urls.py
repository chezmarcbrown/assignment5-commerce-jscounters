from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("hacks", views.HackFormView.as_view(), name="hacks"),
    path("api/get_counters", views.api_get_counters, name="api-get=counters"),
]
