from django.urls import path

from .views import HotelCreateRetrieveView, InvoiceCreateView, InvoiceRetrieveView, ImageCreateView

urlpatterns = [
    path('images/create/', ImageCreateView.as_view()),
    path('hotels/', HotelCreateRetrieveView.as_view()),
    path('invoices/', InvoiceCreateView.as_view()),
    path('invoices/<int:invoice_id>/', InvoiceRetrieveView.as_view()),
]
