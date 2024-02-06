from django.urls import path
from home import views
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("register/", views.Registration.as_view(), name='registration'),
    path("login/", views.MyTokenObtainPairView.as_view(),name='login'),
    path('profile/', views.ProfileManagerView.as_view(),name='profile'),
    # path('profile/<int:pk>/', views.ProfileManagerView.as_view(),name='profile'),
    path("doctorlist/",views.DoctorView.as_view(),name='doctorlist'),
    path('userlist/',views.AdminView.as_view(),name='userlist'),
    path('userlist/<int:pk>/',views.AdminView.as_view(),name='userlist'),
]
