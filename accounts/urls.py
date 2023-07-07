from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view()),  # +
    path('token/', TokenObtainPairView.as_view()),  # +
    path('token/refresh/', TokenRefreshView.as_view()),  # +
    path('account/', views.UserGetView.as_view()),  # +
    path('update/', views.UserUpdateView.as_view()),  # +
    path('delete/', views.UserDeleteView.as_view()),  # +
]
#  TEST :

# register/
# {
#     "email": "mhmdrzrasi@gmail.com",
#     "phone_number": "09152286659",
#     "password": "123",
#     "c_password": "123"
# }

# token/
# {
#     "phone_number": "09152286659",
#     "password": "42574257"
# }

# token/refresh/
# {
#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4OTMzMTM3NSwiaWF0IjoxNjg4NjQwMTc1LCJqdGkiOiIwNmRmYWE1MjNmMTM0NjQ3YTc4YTY1OTMyYjVmYWZlNiIsInVzZXJfaWQiOjExfQ.NaCBY9Jl7cvqNmpiSVJULSxfrC1Nbec9n79SAIA2F8M"
# }

# account/
# GET

# update/
# {
#     "full_name": "mohammadreza rasi",
#     "address": "Mashhad",
#     "birthday": "2002-09-04"
# }

# delete/
# DELETE
