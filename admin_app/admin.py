from django.contrib import admin
import admin_app.models as admin_model 
# Register your models here.
# admin.site.register(admin_model.User)
admin.site.register(admin_model.Cloth)
admin.site.register(admin_model.Rental)
# admin.site.register(admin_model.Transaction)

@admin.register(admin_model.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'rental', 'amount', 'status', 'payment_date')
    readonly_fields = ('transaction_id', 'payment_date')  # So it can't be edited manually

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User

    # Fields to display in the admin list view
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")

    # Fieldsets for user editing in admin panel
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Roles", {"fields": ("role",)}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),

    )

    # Fields for user creation in admin panel
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "role", "is_staff", "is_active")}
        ),
    )

    search_fields = ("username", "email")
    ordering = ("username",)

# Register the custom User model
admin.site.register(User, CustomUserAdmin)
