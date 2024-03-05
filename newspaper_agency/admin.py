from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from newspaper_agency.models import Topic, Redactor, Newspaper


@admin.register(Redactor)
class RedactorAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("years_of_experience", )
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("years_of_experience", )}),)
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


@admin.register(Topic)
class CarAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = ("title", "topic", "content", "published_date", "photo", )
    list_filter = ("title", "published_date")
