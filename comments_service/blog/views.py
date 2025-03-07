from django.shortcuts import render
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from .models import Post, Comment, PostLike, CommentLike, UserProfile
from .serializers import (
    UserSerializer, UserDetailSerializer, PostSerializer, PostDetailSerializer,
    CommentSerializer, PostLikeSerializer, CommentLikeSerializer,
    UserProfileSerializer, UserProfileDetailSerializer
)
from .permissions import IsOwnerOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    """
    API для работы с пользователями
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # По умолчанию разрешаем всем
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'me']:
            return [permissions.IsAuthenticated(), IsOwnerOrReadOnly()]
        return [permissions.AllowAny()]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Получить информацию о текущем пользователе"""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """Регистрация нового пользователя"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API для работы с профилями пользователей
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserProfileDetailSerializer
        return UserProfileSerializer
    
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """Получить профиль текущего пользователя"""
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileDetailSerializer(profile)
        return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    """
    API для работы с постами
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Поставить/убрать лайк посту"""
        post = self.get_object()
        user = request.user
        
        like, created = PostLike.objects.get_or_create(post=post, user=user)
        
        if not created:
            like.delete()
            return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
        
        serializer = PostLikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None):
        """Получить список лайков поста"""
        post = self.get_object()
        likes = post.likes.all()
        serializer = PostLikeSerializer(likes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Получить список популярных постов (по количеству лайков)"""
        posts = Post.objects.annotate(likes_count_db=Count('likes')).order_by('-likes_count_db')[:10]
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my(self, request):
        """Получить список постов текущего пользователя"""
        posts = Post.objects.filter(author=request.user)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """
    API для работы с комментариями
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['post', 'author']
    search_fields = ['content']
    ordering_fields = ['created_at', 'updated_at']
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Поставить/убрать лайк комментарию"""
        comment = self.get_object()
        user = request.user
        
        like, created = CommentLike.objects.get_or_create(comment=comment, user=user)
        
        if not created:
            like.delete()
            return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
        
        serializer = CommentLikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None):
        """Получить список лайков комментария"""
        comment = self.get_object()
        likes = comment.likes.all()
        serializer = CommentLikeSerializer(likes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Получить список популярных комментариев (по количеству лайков)"""
        comments = Comment.objects.annotate(likes_count_db=Count('likes')).order_by('-likes_count_db')[:10]
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my(self, request):
        """Получить список комментариев текущего пользователя"""
        comments = Comment.objects.filter(author=request.user)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)
