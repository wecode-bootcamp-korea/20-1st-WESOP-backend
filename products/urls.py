from django.urls import path

from products.views import DetailProductView

urlpatterns = [
    path('/product', DetailProductView.as_view())
]