from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()


@admin.register(User)
class MyUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'created_at', 'last_login', 'is_active', 'is_staff', 'is_admin')
    readonly_fields = ('created_at', 'last_login')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    fieldsets = (
        (_('basic'), {'fields': ('username', 'first_name', 'last_name', 'email', 'phone')}),
        (_('Important dates'), {'fields': ('created_at', 'last_login')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_active', 'is_admin')}),
    )
    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
        ('created_at', admin.DateFieldListFilter),
    )

    add_fieldsets = (
        ('Required Fields', {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Optional Fields', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'phone', 'is_active', 'is_staff'),
        }),
    )

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()
        super().delete_queryset(request, queryset)
