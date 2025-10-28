"""
Sample アプリケーションの URL ルーティング。

このモジュールは、Django REST Framework のルーターを使用して、
サンプルデータやカテゴリデータにアクセスするためのエンドポイントを定義します。
これにより、API クライアントはこれらのデータを簡単に操作でき、
効率的なデータ管理と操作を可能にします。
ViewSetは複数のアクション（list、retrieve、create、updateなど）を1つのクラスにまとめるものです。

このファイルは、サンプルアプリケーション全体のルーティングを管理します。
新しいエンドポイントを追加する場合は、以下の手順に従ってください。

1. 新しい ViewSet を作成します。
2. 作成した ViewSet をこのファイルにインポートします。
3. ルーターに新しいエンドポイントを登録します。

例:
```python
from apps.sample.views import NewViewSet
router.register(r'new-endpoint', NewViewSet, basename='new')
```
"""
from apps.sample.views import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# 各viewsetをインポート
from apps.sample.views.about_views import AboutViewSet
from apps.sample.views.category_views import CategoryViewSet
from apps.sample.views.sample_views import SampleViewSet

# ルーターのインスタンスを作成
router = DefaultRouter()
# サンプル用のエンドポイントを登録
router.register(r'samples', SampleViewSet, basename='sample')
# カテゴリ用のエンドポイントを登録
router.register(r'categories', CategoryViewSet, basename='category')
# about用のエンドポイントを登録
router.register(r'about', AboutViewSet, basename='about')

# URL パターンを定義
urlpatterns = [
    # path('XXXX/', views.XXXX, name='XXXX'),  # 追加のエンドポイントがあればここに記述
    path('', include(router.urls())),
]
