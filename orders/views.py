from django.shortcuts       import render

# Create your views here.
import json, re, bcrypt, jwt

from datetime               import datetime, timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.http            import JsonResponse
from django.views           import View

from my_settings            import SECRET
from orders.models          import WishList, OrderList, Order, PaymentMethod, OrderStatus
from products.models        import Product, ProductSelection
from users.models           import User
from users.utils            import Authorization_decorator

class OrderCheckView(View):
    @Authorization_decorator
    def get(self, request):
        try:
            user        = request.user
            status_done = OrderStatus.objects.get(name='주문 후')
            
            cartlists   = OrderList.objects.filter(order__status__name='주문 전', order__user=user) 

            if not cartlists:
                return JsonResponse({'MESSAGE':'nothing in cart'}, status=400)

            total_price = 0
            for cartlist in cartlists:
                price        = cartlist.product_selection.price
                total        = price * cartlist.quantity
                total_price  = total_price + total

            Order.objects.filter(status__name='주문 전', user=user).update(
                    status_id    = status_done.id, 
                    address      = user.address,
                    memo         = '',
                    total_price  = total_price if (total_price >= 50000) else (total+3000), 
                    free_delivery= True if (total_price >= 50000) else False 
                )
            return JsonResponse({'MESSAGE':"SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY ERROR'}, status=400)

class OrderGetView(View):
    @Authorization_decorator
    def get(self, request):
        try:
            user           = request.user
            status_done    = OrderStatus.objects.get(name='주문 후')
            products       = OrderList.objects.filter(order__status__name='주문 후', order__user=user) 

            if not products:
                return JsonResponse({'MESSAGE':'NO ORDER HISTORY'}, status=400)
            result = []

            for product in products:
                
                order_dict = {
                        'name'        : product.product_selection.product.name,
                        'quantity'    : product.quantity,
                        'price'       : product.product_selection.price,               
                        'size'        : product.product_selection.size,
                        'date'        : product.order.purchased_at,
                        'product_id'  : product.product_selection.product.id
                    } 
                result.append(order_dict)

            return JsonResponse({'result':result}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY ERROR'}, status=400)