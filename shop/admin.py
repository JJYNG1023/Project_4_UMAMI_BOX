from django.contrib import admin
from .models import Product, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'friendly_name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'friendly_name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'cooking_time',
        'spice_level',
        'is_available',
    )

    list_filter = (
        'category',
        'tag',
        'is_available',
        'spice_level',
    )

    search_fields = (
        'name',
        'description',
        'ingredients',
        'allergens',
    )

    ordering = (
        'category',
        'name',
    )

    filter_horizontal = (
        'tag',
    )
