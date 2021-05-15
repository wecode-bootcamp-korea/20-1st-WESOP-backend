import json

from django.http     import JsonResponse
from django.views    import View

from products.models import FeatureCategory, Menu, Category, Product, ProductSelection

class OpenCategoryView(View):
    def get(self, request, categoryname):
        is_categoryname = True if Category.objects.filter(name=categoryname).exists() else False

        if is_categoryname:
            category = Category.objects.get(name=categoryname)
            results  = self.ShowCategory(category)
        else:
            return JsonResponse({'MESSAGE':'INVALID_PATH'}, status=404)
        return JsonResponse({'result':results}, status=200)

    def ShowCategory(self, category):
        products = Product.objects.filter(category_id=category.id)
        results  = [{
                        "menu_name"         : Menu.objects.get(id=category.menu_id).name,
                        "category_name"     : category.name,
                        "description_title" : category.description_title if category.description_title else None,
                        "description"       : category.description if category.description else None
                    }]

        for product in products:
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

        return results
