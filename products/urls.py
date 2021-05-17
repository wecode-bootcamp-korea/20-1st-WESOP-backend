from django.urls    import path

from products.views import MetaView, DetailProductView

urlpatterns = [
    path('/meta', MetaView.as_view()),
    path('/product', DetailProductView.as_view())
]