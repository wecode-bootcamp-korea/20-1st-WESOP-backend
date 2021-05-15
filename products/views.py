import json

from django.http         import JsonResponse
from django.views        import View
from django.db.models    import Q

from products.models     import Product, ProductSelection, FeatureCategory

class FilteringView(View):
    def get(self, request):
        # feature_id    = request.GET.get('feature_id', None)
        # ingredient_id = request.GET.get('ingredient_id', None)

        # q = Q(feature=feature_id)
        # q.add(Q(ingredient=ingredient_id), q.AND)
        
        # products = Product.objects.filter(q)

        first_id  = request.GET.get('first_id', None)
        second_id = request.GET.get('second_id', None)
        third_id  = request.GET.get('third_id', None)

        first_products = Product.objects.filter(feature=first_id)
        first_filter_products  = [product for product in first_products]

        second_products = Product.objects.filter(feature=second_id)
        second_filter_products = [product for product in second_products if product in first_filter_products]

        third_products = Product.objects.filter(feature=third_id)
        third_filter_products  = [product for product in third_products if product in second_filter_products]

        results = []

        for product in third_filter_products:
            product_name = product.name
            category     = product.category
            menu         = category.menu

            features            = product.feature.all()
            feature_category_id = set([feature.feature_category_id for feature in features])

            feature_result = []
            for id in feature_category_id:
                feature_category_name = FeatureCategory.objects.get(id=id).name
                feature_detail_result = [i.name for i in features.filter(feature_category_id=id)]
                feature_result.append(
                    {
                        "feature_category_name" : feature_category_name,
                        "features"              : feature_detail_result
                    }
                )

            ingredients       = product.ingredient.all()
            ingredient_result = [ingredient.name for ingredient in ingredients]

            product_selections       = ProductSelection.objects.filter(product_id=product.id)
            product_selection_result = [{
                                            "size"      : product_selection.size,
                                            "price"     : product_selection.price,
                                            "image_url" : product_selection.image_url
                                        } for product_selection in product_selections]

            results.append(
                {
                    "menu_name"          : menu.name,
                    "category_name"      : category.name,
                    "product_name"       : product_name,
                    "description"        : product.description,
                    "feature"            : feature_result,
                    "ingredient"         : ingredient_result,
                    "content"            : product.content,
                    "content_image_url"  : product.content_image_url,
                    "product_selections" : product_selection_result
                }
            )

        return JsonResponse({'result':results}, status=200)