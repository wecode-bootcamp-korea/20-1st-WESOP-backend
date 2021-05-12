import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wesop.settings")
django.setup()

from products.models import *

CSV_PATH_PRODUCTS = './wesop.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        menu_name = row[0]
        menu_id = Menu.objects.get(name=menu_name).id

        Category.objects.create(menu_id=menu_id, name=row[1])
