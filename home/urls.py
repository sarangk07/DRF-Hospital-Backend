from django.urls import path
from home import views

urlpatterns = [
    path("register/", views.Registration.as_view(), name='registration'),
]