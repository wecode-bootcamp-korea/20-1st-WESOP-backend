from django.urls import path

from products.views import DetailProductView

urlpatterns = [
    path('/detailproduct', DetailProductView.as_view())
]