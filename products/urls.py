from django.urls import path

from products.views import OpenCategoryView

urlpatterns = [
    path('/category/<str:categoryname>', OpenCategoryView.as_view())
]