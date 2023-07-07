from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.HotelCreateView.as_view()),  # +
    path('update/<int:pk>/', views.HotelUpdateView.as_view()),  # +
    path('delete/<int:pk>/', views.HotelDeleteView.as_view()),  # +
    path('get/<int:pk>/', views.HotelGetView.as_view()),  # +
    path('list/', views.HotelListView.as_view()),  # +

    path('invoice/create/', views.InvoiceCreateView.as_view()),  # +
    path('invoice/update/<int:pk>/', views.InvoiceUpdateView.as_view()),  # +
    path('invoice/delete/<int:pk>/', views.InvoiceDeleteView.as_view()),  # +
    path('invoice/get/<int:pk>/', views.InvoiceGetView.as_view()),  # +
    path('invoice/list/', views.InvoiceListView.as_view()),  # +

    path('image/create/', views.ImageCreateView.as_view()),  # +
    path('image/delete/<int:pk>/', views.ImageDeleteView.as_view()),  # +

    path('filter/', views.FilterView.as_view()),  # +
]
#  TEST :

# create/
# {
#     "name": "aban",
#     "address": "pirozi",
#     "city": "Mashhad",
#     "stars": "4",
#     "features": "good hotel",
#     "rooms": [
#         {
#             "number_of_rooms": "20",
#             "beds": "4"
#         },
#         {
#             "number_of_rooms": "10",
#             "beds": "1"
#         }
#     ]
# }

# update/
# {
#     "name" : "aban"
# }

# delete/
# DELETE

# get/
# GET

# list/
# GET

# invoice/create/
# {
#     "entry_date": "2023-07-07",
#     "leave_date": "2023-07-10",
#     "hotel": "korosh",
#     "passengers": [
#         {
#             "firstname": "mohammad",
#             "lastname": "rasi",
#             "national_id": "0926302566",
#             "phone_number": "09152286659",
#             "gender": "M"
#         },
#         {
#             "firstname": "mohammadreza",
#             "lastname": "rasi",
#             "national_id": "0926302566",
#             "phone_number": "09152286659",
#             "gender": "M"
#         }
#     ]
# }

# invoice/update/
# {
#     "hotel": "aban"
# }

# invoice/delete/
# DELETE

# invoice/get/
# GET

# invoice/list/
# GET

# extra :
# image/create/
# form-data :
# hotel and image

# image/delete/
# DELETE
