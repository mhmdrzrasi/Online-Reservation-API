from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.TrainCreateView.as_view()),  # +
    path('update/<int:pk>/', views.TrainUpdateView.as_view()),  # +
    path('delete/<int:pk>/', views.TrainDeleteView.as_view()),  # +
    path('get/<int:pk>/', views.TrainGetView.as_view()),  # +
    path('list/', views.TrainListView.as_view()),  # +

    path('invoice/create/', views.InvoiceCreateView.as_view()),  # +
    path('invoice/update/<int:pk>/', views.InvoiceUpdateView.as_view()),  # +
    path('invoice/delete/<int:pk>/', views.InvoiceDeleteView.as_view()),  # +
    path('invoice/get/<int:pk>/', views.InvoiceGetView.as_view()),  # +
    path('invoice/list/', views.InvoiceListView.as_view()),  # +

    path('filter/', views.FilterView.as_view()),  # +
]

# create/
# {
#     "train_number": "123",
#     "coupe_number": "321",
#     "features": "khoraki hay ziad",
#     "capacity": 200,
#     "starting_city": "tehran",
#     "destination_city": "esfehan",
#     "departure_date": "2023-07-05",
#     "return_date": "2023-07-06"
# }

# update/
# {
#     "starting_city": "tehran",
#     "destination_city": "mashhad"
# }
