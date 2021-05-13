from django.urls import path

from products.views import OpenView, OpenAllCategoryView, OpenCategoryView, DetailProductView

urlpatterns = [
    path('/open', OpenView.as_view()),
    path('/opencategory', OpenCategoryView.as_view()),
    path('/openallcategory', OpenAllCategoryView.as_view()),
    path('/detailproduct', DetailProductView.as_view()),
]