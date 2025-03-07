from django.contrib import admin
from .models import Post, Comment, PostLike, CommentLike, UserProfile


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at', 'likes_count', 'comments_count')
    list_filter = ('created_at', 'author')
    search_fields = ('title', 'content', 'author__username')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'created_at', 'likes_count')
    list_filter = ('created_at', 'author', 'post')
    search_fields = ('content', 'author__username', 'post__title')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('post__title', 'user__username')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'user', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('comment__content', 'user__username')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'bio')
    list_filter = ('user',)
    search_fields = ('user__username', 'bio')
