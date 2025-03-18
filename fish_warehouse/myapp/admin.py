from django.contrib import admin
from .models import FishDetails,Orders


from .models import *
# Register your models here.


admin.site.register(User)
admin.site.register(FishDetails)
admin.site.register(Orders)