from django.urls    import path

from products.views import MetaView, ProductListView

urlpatterns = [
    path('/meta', MetaView.as_view()),
    path('', ProductListView.as_view()),
]