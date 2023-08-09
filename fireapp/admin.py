from django.contrib import admin
from .models import Crackers,carosel,similarCrackers,CartItem,Address,Orders,Delivered
# Register your models here.
admin.site.register(Crackers)
admin.site.register(carosel)
admin.site.register(similarCrackers)
admin.site.register(CartItem)
admin.site.register(Address)
admin.site.register(Orders)
admin.site.register(Delivered)