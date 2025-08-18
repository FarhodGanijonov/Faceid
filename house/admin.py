from django.contrib import admin, messages
from django.utils.html import format_html

from .models import House, House_image, District, Region, Comment


class HouseImageInline(admin.TabularInline):  # yoki StackedInline
    model = House_image
    extra = 1  # Qo‘shimcha 1 ta bo‘sh forma ko‘rsatadi


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = (
        "id", "title", "price", "district",
        "room_count", "owner", "created_at", "status", 'status_icon'
    )
    list_filter = ("status", "region", "district", "created_at")
    inlines = [HouseImageInline]  # House_image modelini Inline teared qo‘shish

    def status_icon(self, obj):
        if obj.status == "pending":
            color = "orange"
            icon = "⏳"  # kutilmoqda
        elif obj.status == "active":
            color = "green"
            icon = "✅"  # faol
        elif obj.status == "deactive":
            color = "red"
            icon = "❌"  # nofaol
        else:
            color = "black"
            icon = ""
        return format_html('<span style="color: {};">{} {}</span>', color, icon, obj.status)

    status_icon.short_description = "Status"
    search_fields = (
        "title",
        "owner__phone",      # ✅ qidiruv telefon raqam bo‘yicha
        "owner__full_name",  # ✅ qidiruv ism bo‘yicha
    )
    ordering = ("-created_at",)

    def get_readonly_fields(self, request, obj=None):
        # Faqat superuser statusni o‘zgartira oladi
        if not request.user.is_superuser:
            return ['status']
        return []

    @admin.action(description='✅ E’lonni tasdiqlash (active)')
    def approve_houses(self, request, queryset):
        updated = queryset.update(status='active', is_active=True)
        self.message_user(request, f"{updated} ta e’lon faol holatga o‘tkazildi.", messages.SUCCESS)

    @admin.action(description='🚫 E’lonni rad etish (deactive)')
    def reject_houses(self, request, queryset):
        updated = queryset.update(status='deactive', is_active=False)
        self.message_user(request, f"{updated} ta e’lon rad etildi.", messages.WARNING)


admin.site.register(District)


class DistrictInline(admin.TabularInline):  # yoki admin.StackedInline
    model = District
    extra = 1


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    inlines = [DistrictInline]


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "house_title",
        "house_owner_name",
        "house_owner_phone",
        "comment_user_name",
        "comment_user_phone",
        "text",
        "created_at",
    )
    search_fields = ("house__title", "user__full_name", "user__phone")
    list_filter = ("created_at", "house__title")
    ordering = ("-created_at",)
    list_select_related = ("house", "house__owner", "user")  # SQL querylarni kamaytiradi

    def house_title(self, obj):
        return obj.house.title
    house_title.short_description = "House Title"

    def house_owner_name(self, obj):
        return obj.house.owner.full_name if hasattr(obj.house.owner, "full_name") else "—"
    house_owner_name.short_description = "House Owner"

    def house_owner_phone(self, obj):
        return obj.house.owner.phone if hasattr(obj.house.owner, "phone") else "—"
    house_owner_phone.short_description = "Owner Phone"

    def comment_user_name(self, obj):
        return obj.user.full_name if hasattr(obj.user, "full_name") else "—"
    comment_user_name.short_description = "Comment User"

    def comment_user_phone(self, obj):
        return obj.user.phone if hasattr(obj.user, "phone") else "—"
    comment_user_phone.short_description = "Comment User Phone"


admin.site.register(Comment, CommentAdmin)