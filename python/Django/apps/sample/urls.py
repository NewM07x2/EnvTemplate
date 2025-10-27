"""
PostアプリケーションのURLルーティング。

このモジュールは、Django REST Frameworkのルーターを使用して、
サンプルデータとカテゴリデータにアクセスするためのエンドポイントを定義します。
これにより、APIクライアントはサンプルデータとカテゴリデータを簡単に操作でき、
効率的なデータ管理と操作を可能にします。
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CategoryViewSet

# ルーターのインスタンスを作成
router = DefaultRouter()
# サンプル用のエンドポイントを登録
router.register(r'samples', PostViewSet, basename='sample')  # サンプルデータにアクセスするためのエンドポイント
# カテゴリ用のエンドポイントを登録
router.register(r'categories', CategoryViewSet, basename='category')  # カテゴリデータにアクセスするためのエンドポイント

# URLパターンを定義
urlpatterns = [
    path('', include(router.urls)),  # ルーターで定義されたエンドポイントを含める
]
