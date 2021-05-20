from django.shortcuts import render

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
            user           = request.user
            status_done = OrderStatus.objects.get(name='주문 후')
            
            cartlists      = OrderList.objects.filter(order__status__name='주문 전', order__user=user) 

            if not cartlists:
                return JsonResponse({'MESSAGE':'nothing in cart'}, status=400)

            total_price = 0

            for cartlist in cartlists:
                price        = cartlist.prduct_selection.price
                total        = price * cartlist.quantity
                total_price  = total_price + total
# Order.objects.filter(status_id=status_id, user_id=user.id)
            cartlists.order.update(
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
            orders         = Order.objects.filter(status_id=status_done.id, user_id=user.id) 

            if not orders:
                raise Exception

            result = []

            for order in orders:
                products = list(OrderList.objects.filter(order_id=order.id))

                for product in products:
                    selection = product.product_selection
                    select    = OrderList.objects.get(product_selection=selection)

                    order_dict = {
                            'name'        : select.product_selection.product.name,
                            'quantity'    : product.quantity,
                            'price'       : select.product_selection.price,               
                            'size'        : select.product_selection.size,
                            'date'        : product.purchased_at,
                            'product_id'  : select.product_selection.product.id
                        } 
                    result.append(order_dict)

            return JsonResponse({'result':result}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY ERROR'}, status=400)
        except Exception as e:
            return JsonResponse({'MESSAGE':'NO ORDER HISTORY'}, status=400)