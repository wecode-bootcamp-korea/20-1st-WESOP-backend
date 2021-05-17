import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from products.models  import Menu, Category, Product, ProductSelection, FeatureCategory

class ProductListView(View):
    def get(self, request):
        menu_id     = request.GET.get('menu_id', None)
        category_id = request.GET.get('category_id', None)

        q = Q()

        if menu_id and Menu.objects.filter(id=menu_id).exists():
            q = Q(category__menu_id=menu_id)
        elif category_id and Category.objects.filter(id=category_id):
            q = Q(category_id=category_id)
        else:
            return JsonResponse({'MESSAGE':'INVALID_PATH'}, status=404)
        
        products      = Product.objects.filter(q)
        total_results = []

        for product in products:
            category           = product.category
            menu               = category.menu
            ingredients        = product.ingredient.all()
            product_selections = ProductSelection.objects.filter(product_id=product.id)

            features            = product.feature.all()
            feature_category_id = set([feature.feature_category_id for feature in features])
            feature_result      = []
            for id in feature_category_id:
                feature_category_name = FeatureCategory.objects.get(id=id).name
                feature_detail_result = [i.name for i in features.filter(feature_category_id=id)]
                feature_result.append(
                    {
                        "feature_category_name" : feature_category_name,
                        "features"              : feature_detail_result
                    }
                )
            results = [
                {
                    "menu_name"                  : menu.name,
                    "menu_id"                    : menu.id,
                    "category_name"              : category.name,
                    "category_id"                : category.id,
                    "category_description_title" : category.description_title,
                    "category_description"       : category.description,
                    "product_name"               : product.name,
                    "product_id"                 : product.id,
                    "description"                : product.description,
                    "feature"                    : feature_result,
                    "content"                    : product.content,
                    "content_image_url"          : product.content_image_url,
                    "ingredient_result"          : [ingredient.name for ingredient in ingredients],
                    "product_selection_result"   : [
                        {
                            "size"      : product_selection.size,
                            "price"     : product_selection.price,
                            "image_url" : product_selection.image_url
                        } for product_selection in product_selections 
                    ]
                }
            ]

            total_results.append(results)

        return JsonResponse({'result': total_results}, status=200)