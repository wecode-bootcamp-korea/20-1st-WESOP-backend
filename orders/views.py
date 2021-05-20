from django.shortcuts import render

# Create your views here.
import json, re, bcrypt, jwt

from datetime     import datetime, timedelta

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
            status_id      = OrderStatus.objects.get(name='주문 전').id
            status_id_done = OrderStatus.objects.get(name='주문 후').id
            
            if (not Order.objects.filter(status_id=status_id, user_id=user.id)):
                raise Exception

            order          = Order.objects.get(status_id=status_id, user_id=user.id) 
            cartlists      = OrderList.objects.filter(order_id=order.id)

            result=[]
            total_price = 0

            for cartlist in cartlists:
                selection_id = cartlist.product_selection_id
                select       = ProductSelection.objects.get(id=selection_id)
                total        = select.price * cartlist.quantity
                total_price += total

                Order.objects.filter(status_id=status_id, user_id=user.id).update(
                        status_id    = status_id_done, 
                        address      = user.address,
                        memo         = '',
                        total_price  = total_price if (total_price >= 50000) else (total+3000), 
                        free_delivery= True if (total_price >= 50000) else False 
                    )
            
            OrderList.objects.filter(order_id=order.id).delete()

            return JsonResponse({'MESSAGE':"SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY ERROR'}, status=400)

        except Exception as e:
            return JsonResponse({'MESSAGE':'nothing in cart'}, status=400)

class OrderGetView(View):
    @Authorization_decorator
    def get(self, request):
        try:
            user        = request.user
            status_id_done = OrderStatus.objects.get(name='주문 후').id

            if (not Order.objects.filter(status_id=status_id_done, user_id=user.id)):
                raise Exception

            orders = Order.objects.filter(status_id=status_id_done, user_id=user.id) 
            result = []

            for order in orders:

                order_dict = {
                        'name'        : Product.objects.get(id=select.product_id).name,
                        'quantity'    : cartlist.quantity ,
                        'total_price' : Order.objects.get(id=cartlist.order_id).total_price,
                        'purchased_at': Order.objects.get(id=cartlist.order_id).purchased_at,
                        'address'     : User.objects.get(id=user.id).address
                    } 
                result.append(order_dict)

            return JsonResponse({'result':result}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY ERROR'}, status=400)

        except Exception as e:
            return JsonResponse({'MESSAGE':'NO ORDER HISTORY'}, status=400)