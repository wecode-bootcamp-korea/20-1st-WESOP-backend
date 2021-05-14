import json

from django.http     import JsonResponse
from django.views    import View

from products.models import FeatureCategory, Product, ProductSelection

class DetailProductView(View):
    def get(self, request):
        product_id = request.GET.get('product_id', None)
        product = Product.objects.get(id=product_id)
        category = product.category
        menu = category.menu
        product.count += 1
        # product.save() 프로젝트 완성되면 카운트 쌓을 예정입니다 :)

        results = {
                "menu_name" : menu.name,
                "category_name" : category.name,
                "product_name" : product.name,
                "description" : product.description,
                "content" : product.content,
                "content_image_url" : product.content_image_url
        }
        
        feature_category_id = []
        features = product.feature.all()
        for feature in features:
            if feature.feature_category_id not in feature_category_id:
                feature_category_id.append(feature.feature_category_id)

        feature_result = []
        for id in feature_category_id:
            feature_category_name = FeatureCategory.objects.get(id=id).name
            feature_detail_result = []
            for i in features.filter(feature_category_id=id):
                feature_detail_result.append(i.name)
            feature_result.append(
                {
                    "feature_category_name" :feature_category_name,
                    "features" : feature_detail_result
                }
            )

        results["feature"] = feature_result

        ingredient_result = []
        ingredients = product.ingredient.all()
        for ingredient in ingredients:
            ingredient_result.append(ingredient.name)
            
        results["ingredient"] = ingredient_result

        product_selection_result = []
        product_selections = ProductSelection.objects.filter(product_id=product.id)
        for product_selection in product_selections:
            product_selection_result.append(
                {
                    "product_name" : product.name,
                    "size" : product_selection.size,
                    "price" : product_selection.price,
                    "image_url" : product_selection.image_url
                }
            )

        results["product_selection"] = product_selection_result

        return JsonResponse({'result': results}, status=200)
