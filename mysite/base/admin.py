from django.contrib import admin
from .models import User, products_names, Cart
# Register your models here.

admin.site.register(User)
admin.site.register(products_names)
admin.site.register(Cart)