from django.urls import path

from products.views import FilteringAtMenuView, FilteringAtCategoryView

urlpatterns = [
    path('/filter/menu/<str:menuname>', FilteringAtMenuView.as_view()),
    path('/filter/category/<str:categoryname>', FilteringAtCategoryView.as_view())
]
