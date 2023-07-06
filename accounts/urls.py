from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view()),
    path('account/', views.UserGetView.as_view()),
    path('update/', views.UserUpdateView.as_view()),
    path('delete/', views.UserDeleteView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
