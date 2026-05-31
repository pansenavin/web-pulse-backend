from django.contrib import admin
from .models import User, Role

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'name', 'role', 'is_staff', 'is_superuser')
    search_fields = ('email', 'name', 'username')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

admin.site.register(Role)
