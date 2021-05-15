from django.urls import path

from products.views import FilteringView

urlpatterns = [
    path('/filter', FilteringView.as_view())
]
