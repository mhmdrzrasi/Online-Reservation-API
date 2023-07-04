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

# {
#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4OTE2MzYwNiwiaWF0IjoxNjg4NDcyNDA2LCJqdGkiOiI2MTE4MWFhMDI3ZjU0MDdhOTIyMmQ4MDE5ZjkzNGU2YyIsInVzZXJfaWQiOjR9.FjLS_CYKCrSLDBsQWg7adBsWRl85XUb9zTy6hX-ARWQ",
#     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg5MDc3MjA2LCJpYXQiOjE2ODg0NzI0MDYsImp0aSI6IjBmOTQ3NDJhZmM5MjQ1Y2FiZTI0NGYwZTdhNzQxMGQ1IiwidXNlcl9pZCI6NH0.bjgNd6cVF9ljY5clZxrP62Abh_FBzdcwzUtYX70R22U"
# }