from django.contrib.auth import admin as auth_admin
from django.contrib import admin

from .models import User
# Register your models here.

admin.site.site_title = "数据库后台管理"
admin.site.site_header = "数据库管理界面"

@admin.register(User)
class UserModelAdmin(auth_admin.UserAdmin):
    search_fields = ("id", "username", "full_name", "email", "phone")
    sortable_by = ("id", "last_login", "date_joined")
    list_display = ("id", "username", "full_name", "email", "phone", "last_login", "is_superuser", "is_active", "date_joined")
    list_display_links = ("id", "username", "full_name", "email", "phone")
    fieldsets = list(auth_admin.UserAdmin.fieldsets)   # 转换为可以修改的列表
    fieldsets[1] = ("个人信息", {"fields": ("full_name", "email", "phone")})
    fieldsets[2] = ("账户权限", {"fields": ("is_superuser", "is_active")})
    readonly_fields = ("last_login", "date_joined")
