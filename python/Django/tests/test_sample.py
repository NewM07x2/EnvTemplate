"""Sample tests for Django application.

These tests can be copied and modified for your own test cases.
"""

import pytest
from django.contrib.auth import get_user_model
# from apps.sample.models import Sample, Category

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    """Test User model."""
    
    def test_create_user(self):
        """Test creating a user."""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        assert user.email == 'test@example.com'
        assert user.username == 'testuser'
        assert user.check_password('testpass123')
        assert user.full_name == 'Test User'
    
    def test_user_str(self):
        """Test user string representation."""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        assert str(user) == 'test@example.com'


@pytest.mark.django_db
class TestCategoryModel:
    """Test Category model."""
    
    def test_create_category(self):
        """Test creating a category."""
        category = Category.objects.create(
            name='Technology',
            slug='technology',
            description='Tech articles'
        )
        assert category.name == 'Technology'
        assert category.slug == 'technology'
        assert str(category) == 'Technology'


@pytest.mark.django_db
class TestPostModel:
    """Test Post model."""
    
    @pytest.fixture
    def user(self):
        """Create a test user."""
        return User.objects.create_user(
            email='author@example.com',
            username='author',
            password='testpass123'
        )
    
    @pytest.fixture
    def category(self):
        """Create a test category."""
        return Category.objects.create(
            name='Technology',
            slug='technology'
        )
    
    def test_create_post(self, user, category):
        """Test creating a post."""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is a test post',
            excerpt='Test excerpt',
            author=user,
            category=category,
            is_published=True
        )
        assert post.title == 'Test Post'
        assert post.slug == 'test-post'
        assert post.author == user
        assert post.category == category
        assert post.is_published is True
        assert str(post) == 'Test Post'
    
    def test_post_views_count(self, user):
        """Test post views count."""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='Content',
            author=user
        )
        assert post.views_count == 0
        
        post.views_count += 1
        post.save()
        assert post.views_count == 1


@pytest.mark.django_db
class TestUserAPI:
    """Test User API endpoints."""
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get('/health/')
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'healthy'
    
    def test_ping(self, client):
        """Test ping endpoint."""
        response = client.get('/health/ping/')
        assert response.status_code == 200
        data = response.json()
        assert data['message'] == 'pong'
