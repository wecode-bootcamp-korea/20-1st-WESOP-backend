import json

from django.http     import JsonResponse
from django.views    import View

from products.models import FeatureCategory, Menu, Category, Product, ProductSelection

class OpenView(View):
    def get(self, request):
        menus = Menu.objects.all()
        categories = Category.objects.all()

        results = [{"menu_name":menu.name} for menu in menus] + \
                [{
                    "menu_name" : Menu.objects.get(id=category.menu_id).name,
                    "category_name" : category.name,
                    "description_title" : category.description_title,
                    "description" : category.description
                } if category.description_title else {
                    "menu_name" : Menu.objects.get(id=category.menu_id).name,
                    "category_name" : category.name,
                    "description_title" : category.description_title,
                    "description" : category.description
                } for category in categories ]

        return JsonResponse({'result': results}, status=200)

class OpenAllCategoryView(View):
    def get(self, request):
        menu_id = request.GET.get('menu_id', None)
        menu = Menu.objects.get(id=menu_id)
        categories = Category.objects.filter(menu_id=menu.id)
        total_results = []

        for category in categories:
            results = []
            if category.description_title:
                results.append(
                {
                    "menu_name" : Menu.objects.get(id=category.menu_id).name,
                    "category_name" : category.name,
                    "description_title" : category.description_title,
                    "description" : category.description
                }
            )
            else:
                results.append(
                {
                    "menu_name" : Menu.objects.get(id=category.menu_id).name,
                    "category_name" : category.name
                }
            )
            products = Product.objects.filter(category_id=category.id)
            for product in products:
                product_name = product.name
                category = product.category
                menu = category.menu

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

                ingredient_result = []
                ingredients = product.ingredient.all()
                for ingredient in ingredients:
                    ingredient_result.append(ingredient.name)

                product_selection_result = []
                product_selections = ProductSelection.objects.filter(product_id=product.id)
                for product_selection in product_selections:
                    product_selection_result.append(
                        {
                            "product_name" : product_name,
                            "size" : product_selection.size,
                            "price" : product_selection.price,
                            "image_url" : product_selection.image_url
                        }
                    )

                results.append(
                    {
                        "menu_name" : menu.name,
                        "category_name" : category.name,
                        "product_name" : product_name,
                        "description" : product.description,
                        "feature" : feature_result,
                        "ingredient" : ingredient_result,
                        "content" : product.content,
                        "content_image_url" : product.content_image_url,
                        "product_selections" : product_selection_result
                    }
                )

            total_results.append(results)

        return JsonResponse({'result': total_results}, status=200)

class OpenCategoryView(View):
    def get(self, request):
        category_id = request.GET.get('category_id', None)
        category = Category.objects.get(id=category_id)
        products = Product.objects.filter(category_id=category.id)
        results = []

        if category.description_title:
            results.append(
            {
                "menu_name" : Menu.objects.get(id=category.menu_id).name,
                "category_name" : category.name,
                "description_title" : category.description_title,
                "description" : category.description
            }
        )
        else:
            results.append(
            {
                "menu_name" : Menu.objects.get(id=category.menu_id).name,
                "category_name" : category.name
            }
        )

        for product in products:
            product_name = product.name
            category = product.category
            menu = category.menu

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

            ingredient_result = []
            ingredients = product.ingredient.all()
            for ingredient in ingredients:
                ingredient_result.append(ingredient.name)

            product_selection_result = []
            product_selections = ProductSelection.objects.filter(product_id=product.id)
            for product_selection in product_selections:
                product_selection_result.append(
                    {
                        "product_name" : product_name,
                        "size" : product_selection.size,
                        "price" : product_selection.price,
                        "image_url" : product_selection.image_url
                    }
                )

            results.append(
                {
                    "menu_name" : menu.name,
                    "category_name" : category.name,
                    "product_name" : product_name,
                    "description" : product.description,
                    "feature" : feature_result,
                    "ingredient" : ingredient_result,
                    "content" : product.content,
                    "content_image_url" : product.content_image_url,
                    "product_selections" : product_selection_result
                }
            )

        return JsonResponse({'result': results}, status=200)

class DetailProductView(View):
    def get(self, request):
        product_id = request.GET.get('product_id', None)
        product = Product.objects.get(id=product_id)
        category = product.category
        menu = category.menu
        product.count += 1
        # product.save()

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

        ingredient_result = []
        ingredients = product.ingredient.all()
        for ingredient in ingredients:
            ingredient_result.append(ingredient.name)

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

        results = []
        results.append(
            {
                "menu_name" : menu.name,
                "category_name" : category.name,
                "product_name" : product.name,
                "description" : product.description,
                "feature" : feature_result,
                "ingredient" : ingredient_result,
                "content" : product.content,
                "content_image_url" : product.content_image_url,
                "product_selections" : product_selection_result
            }
        )

        return JsonResponse({'result': results}, status=200)

# class FeatureFilteringView(View):
#     def get(self, request):
#         menu = Menu.objects.get(id=1) # url 처리
#         categories = Category.objects.filter(menu_id=menu.id)
#         products = []

#         for category in categories:
#             if Product.objects.filter(category_id=category.id):
#                 products.append(Product.objects.filter(category_id=category.id))
#     def get(self, request):

#         products = Product.objects.filter(feature=1)
