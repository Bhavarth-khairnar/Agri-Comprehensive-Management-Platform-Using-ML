from django.contrib import admin
from app.models import Crop_Details,fert_Details,images_data,image_data

# Register your models here.
admin.site.register(Crop_Details)
admin.site.register(fert_Details)
admin.site.register(images_data)
admin.site.register(image_data)