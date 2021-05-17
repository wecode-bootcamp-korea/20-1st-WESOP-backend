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
            categories = Category.objects.filter(menu_id=menu_id)
        elif category_id and Category.objects.filter(id=category_id):
            q = Q(category_id=category_id)
            categories = Category.objects.filter(id=category_id)
        else:
            return JsonResponse({'MESSAGE':'INVALID_PATH'}, status=404)
        
        products = Product.objects.filter(q)
        total_results = []

        for category in categories:
            category_results = [
                {
                    "menu_name"         : Menu.objects.get(id=category.menu_id).name,
                    "category_name"     : category.name,
                    "description_title" : category.description_title if category.description_title else None,
                    "description"       : category.description if category.description else None
                }
            ]

            products = Product.objects.filter(category_id=category.id)
            for product in products:
                category           = product.category
                menu               = category.menu
                ingredients        = product.ingredient.all()
                product_selections = ProductSelection.objects.filter(product_id=product.id)

                product_results = {
                                "menu_name"                : menu.name,
                                "category_name"            : category.name,
                                "product_name"             : product.name,
                                "description"              : product.description,
                                "content"                  : product.content,
                                "content_image_url"        : product.content_image_url,
                                "ingredient_result"        : [ingredient.name for ingredient in ingredients],
                                "product_selection_result" : [
                                    {
                                        "size"      : product_selection.size,
                                        "price"     : product_selection.price,
                                        "image_url" : product_selection.image_url
                                    } for product_selection in product_selections 
                                ]
                }

                features            = product.feature.all()
                feature_category_id = set([feature.feature_category_id for feature in features])
                feature_result      = []
                for id in feature_category_id:
                    feature_category_name = FeatureCategory.objects.get(id=id).name
                    feature_detail_result = [i.name for i in features.filter(feature_category_id=id)]
                    feature_result.append(
                        {
                            "feature_category_name" : feature_category_name,
                            "features" : feature_detail_result
                        }
                    )
                product_results["feature"] = feature_result

                category_results.append(product_results)

            total_results.append(category_results)

        return JsonResponse({'result': total_results}, status=200)