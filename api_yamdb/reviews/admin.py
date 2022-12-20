from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Category, Genre, GenreTitle, Title, User


class GenreResource(resources.ModelResource):
    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')


@admin.register(Genre)
class GenreAdmin(ImportExportModelAdmin):
    resource_classes = (GenreResource,)
    list_display = ('name', 'slug')


class TitleResource(resources.ModelResource):
    class Meta:
        model = Title
        fields = ('id',
                  'name',
                  'year',
                  'rating',
                  'description',
                  'category'
                  )


@admin.register(Title)
class TitleAdmin(ImportExportModelAdmin):
    resource_classes = (TitleResource,)
    list_display = ('name',
                    'year',
                    'rating',
                    'description',
                    'category'
                    )


class GenreTitleResource(resources.ModelResource):
    class Meta:
        model = GenreTitle
        fields = ('id',
                  'genre_id',
                  'title_id')


@admin.register(GenreTitle)
class GenreTitleAdmin(ImportExportModelAdmin):
    resource_classes = (GenreTitleResource,)
    list_display = ('genre_id',
                    'title_id'
                    )


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_classes = (CategoryResource,)
    list_display = ('name', 'slug')


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "username",
        "role",
    )
    list_filter = ("role",)
    empty_value_display = "-пусто-"


admin.site.register(User, UserAdmin)
