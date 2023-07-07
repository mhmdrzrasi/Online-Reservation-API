from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.PlaneCreateView.as_view()),  # +
    path('update/<int:pk>/', views.PlaneUpdateView.as_view()),  # +
    path('delete/<int:pk>/', views.PlaneDeleteView.as_view()),  # +
    path('get/<int:pk>/', views.PlaneGetView.as_view()),  # +
    path('list/', views.PlaneListView.as_view()),  # +

    path('invoice/create/', views.InvoiceCreateView.as_view()),  # +
    path('invoice/update/<int:pk>/', views.InvoiceUpdateView.as_view()),  # +
    path('invoice/delete/<int:pk>/', views.InvoiceDeleteView.as_view()),  # +
    path('invoice/get/<int:pk>/', views.InvoiceGetView.as_view()),  # +
    path('invoice/list/', views.InvoiceListView.as_view()),  # +

    path('filter/', views.FilterView.as_view()),  # +
]

#  create/plane/
# {
#     "flight_number": "123",
#     "flight_terminal": "321",
#     "amount_of_load": 30,
#     "features": "khoraki hay ziad",
#     "capacity": 200,
#     "starting_city": "tehran",
#     "destination_city": "esfehan",
#     "departure_date": "2023-07-05",
#     "return_date": "2023-07-06"
# }

# create/invoice/
# {
#     "plane": "123",
#     "passengers": [
#         {
#             "firstname": "mhmd",
#             "lastname": "rasi",
#             "national_id": "1234567890",
#             "birthday": "2002-09-04",
#             "gender": "M"
#         }
#     ]
# }
