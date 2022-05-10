from django.urls import path

from addresses.views import AddressView

urlpatterns = [
    path('address/', AddressView.as_view())
]