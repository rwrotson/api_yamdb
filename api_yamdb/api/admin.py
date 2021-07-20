from django.contrib import admin

from .models import CustomUser, Review, Comment


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'username', 'bio',
                  'email', 'role')
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title_id', 'text', 'author', 'score', 'pub_date')
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'text', 'author', 'pub_date')
    empty_value_display = '-пусто-'


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
