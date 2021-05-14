from django.urls import path

from products.views import OpenMenuView

urlpatterns = [
    path('/menu/<str:menuname>', OpenMenuView.as_view())
]