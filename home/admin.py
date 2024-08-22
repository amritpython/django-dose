from django.contrib import admin

from home.models import *
# Register your models here.
from shopify_app.models import Shop

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(ShopifyUser)
admin.site.register(Form)
admin.site.register(Question)
admin.site.register(Shop)
admin.site.register(Extra)
