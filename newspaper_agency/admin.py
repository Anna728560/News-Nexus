from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count
from django.utils.safestring import mark_safe

from newspaper_agency.models import (
    Topic,
    Redactor,
    Newspaper,
    Commentary
)


@admin.register(Redactor)
class RedactorAdmin(admin.ModelAdmin):
    list_display = UserAdmin.list_display + (
        "years_of_experience", "get_article_count"
    )
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("years_of_experience",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "years_of_experience",
                    )
                },
            ),
        )
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(article_count=Count("newspapers"))
        return queryset

    def get_article_count(self, obj):
        return obj.article_count

    get_article_count.short_description = "Number of Articles"


@admin.register(Topic)
class CarAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "topic",
        "published_date",
        "publisher_name",
        "get_photo"
    )
    list_filter = (
        "title",
        "published_date",
    )
    fields = (
        "title",
        "topic",
        "content",
        "published_date",
        "publisher_name",
        "photo",
        "get_photo",
    )
    readonly_fields = (
        "published_date",
        "publisher_name",
        "get_photo",
    )

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width='75'>")
        return "-"

    get_photo.short_description = "Photo"

    def publisher_name(self, obj):
        return obj.publishers.first().username if obj.publishers.exists() else "-"

    publisher_name.short_description = "Publisher Name"


@admin.register(Commentary)
class CommentaryAdmin(admin.ModelAdmin):
    list_display = ("user", "content", "created_time")
