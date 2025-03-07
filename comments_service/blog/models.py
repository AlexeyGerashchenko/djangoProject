from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    """Модель поста"""
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='Автор')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def likes_count(self):
        return self.likes.count()
    
    @property
    def comments_count(self):
        return self.comments.count()


class Comment(models.Model):
    """Модель комментария"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Пост')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор')
    content = models.TextField(verbose_name='Содержание')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Комментарий от {self.author.username} к посту "{self.post.title}"'
    
    @property
    def likes_count(self):
        return self.likes.count()


class PostLike(models.Model):
    """Модель лайка к посту"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', verbose_name='Пост')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes', verbose_name='Пользователь')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Лайк к посту'
        verbose_name_plural = 'Лайки к постам'
        unique_together = ('post', 'user')
    
    def __str__(self):
        return f'Лайк от {self.user.username} к посту "{self.post.title}"'


class CommentLike(models.Model):
    """Модель лайка к комментарию"""
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes', verbose_name='Комментарий')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_likes', verbose_name='Пользователь')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Лайк к комментарию'
        verbose_name_plural = 'Лайки к комментариям'
        unique_together = ('comment', 'user')
    
    def __str__(self):
        return f'Лайк от {self.user.username} к комментарию {self.comment.id}'


class UserProfile(models.Model):
    """Расширенная модель пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Пользователь')
    bio = models.TextField(blank=True, null=True, verbose_name='О себе')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
    
    def __str__(self):
        return f'Профиль пользователя {self.user.username}'
