from django.urls    import path
from orders.views   import OrderCheckView, OrderGetView

urlpatterns = [
            path('', OrderCheckView.as_view()),
            path('/log', OrderGetView.as_view())
]