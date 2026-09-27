from django.contrib import admin
from .models import Tag, Promise


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "group", "slug")
    list_filter = ("group",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Promise)
class PromiseAdmin(admin.ModelAdmin):
    list_display = ("verse_ref", "version", "created_at")
    search_fields = ("verse_ref", "verse_text")
    filter_horizontal = ("tags",)
