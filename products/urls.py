from django.urls import path

from products.views import FilteringAtMenuView

urlpatterns = [
    path('/filter/<str:menuname>', FilteringAtMenuView.as_view())
]
