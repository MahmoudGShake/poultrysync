from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Company, CustomUser, Product, Order

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'company', 'role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Company Info', {'fields': ('company', 'role')}),
    )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'price', 'stock', 'is_active', 'created_at']
    list_filter = ['company', 'is_active']
    actions = ['mark_inactive']

    def mark_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} product(s) marked as inactive.")
    mark_inactive.short_description = "Mark selected products as inactive"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'quantity', 'status', 'company', 'created_by', 'created_at']
