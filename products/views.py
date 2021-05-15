import json

from django.http         import JsonResponse
from django.views        import View
from django.db.models    import Q
from django.forms.models import model_to_dict

from products.models     import Menu, Category, Product, ProductSelection, FeatureCategory

class FilteringView(View):
    def get(self, request):
        products = Product.objects.all()
        
        if request.query_params:
            feature_skin    = request.GET.get('skin_id', None)
            feature_feeling = request.GET.get('feeling_id', None)
            feature_scent   = request.GET.get('scent_id', None)
