from api_yamdb.settings import VALUE_DISPLAY
from django.contrib import admin

from reviews.models import Category, Comments, Genre, Review, Title, User


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'title', 'text', 'score', 'pub_date',)
    search_fields = ('author', 'title', 'text',)
    list_filter = ('score', 'text',)
    list_editable = ('author', 'title', 'text', 'score',)
    empty_value_display = VALUE_DISPLAY


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'review', 'text', 'pub_date',)
    search_fields = ('author', 'text', 'pub_date',)
    list_filter = ('author',)
    list_editable = ('author', 'review', 'text',)
    empty_value_display = VALUE_DISPLAY


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description', 'category',)
    search_fields = ('name', 'description',)
    list_filter = ('year', 'genre', 'category',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'role', 'username', 'email',
                    'bio', 'first_name', 'last_name',)
