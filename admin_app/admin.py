from django.contrib import admin
import admin_app.models as admin_model 
# Register your models here.
admin.site.register(admin_model.User)
admin.site.register(admin_model.Cloth)
admin.site.register(admin_model.Rental)
admin.site.register(admin_model.Transaction)