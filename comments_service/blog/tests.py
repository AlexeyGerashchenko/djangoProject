from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Post, Comment, PostLike, CommentLike, UserProfile
from django.urls import reverse

User = get_user_model()

class UserTests(APITestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('user-list')

    def tearDown(self):
        User.objects.all().delete()

    def test_create_user(self):
        """Тест создания пользователя"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_update_user(self):
        """Тест обновления информации о пользователе"""
        data = {
            'username': 'updateduser',
            'email': 'updated@example.com'
        }
        response = self.client.patch(reverse('user-detail', args=[self.user.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updated@example.com')

class PostTests(APITestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('post-list')

    def tearDown(self):
        Post.objects.all().delete()
        PostLike.objects.all().delete()

    def test_create_post(self):
        """Тест создания поста"""
        data = {
            'title': 'Test Post',
            'content': 'Test Content'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)

    def test_delete_post(self):
        """Тест удаления поста"""
        post = Post.objects.create(
            title='Test Post',
            content='Test Content',
            author=self.user
        )
        response = self.client.delete(reverse('post-detail', args=[post.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_like_post(self):
        """Тест лайка поста"""
        post = Post.objects.create(
            title='Test Post',
            content='Test Content',
            author=self.user
        )
        response = self.client.post(reverse('post-like', args=[post.id]))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PostLike.objects.count(), 1)

class CommentTests(APITestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Создаем тестовый пост
        self.post = Post.objects.create(
            title='Test Post',
            content='Test Content',
            author=self.user
        )
        self.url = reverse('comment-list')

    def tearDown(self):
        Comment.objects.all().delete()
        CommentLike.objects.all().delete()

    def test_create_comment(self):
        """Тест создания комментария"""
        data = {
            'content': 'Test Comment',
            'post': self.post.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)

    def test_delete_comment(self):
        """Тест удаления комментария"""
        comment = Comment.objects.create(
            content='Test Comment',
            post=self.post,
            author=self.user
        )
        response = self.client.delete(reverse('comment-detail', args=[comment.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

    def test_like_comment(self):
        """Тест лайка комментария"""
        comment = Comment.objects.create(
            content='Test Comment',
            post=self.post,
            author=self.user
        )
        response = self.client.post(reverse('comment-like', args=[comment.id]))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CommentLike.objects.count(), 1)
