
from django.urls    import path
from orders.views   import OrderCheckView



urlpatterns = [
            path('/order', OrderCheckView.as_view())
]