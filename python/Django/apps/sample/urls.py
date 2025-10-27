"""
Sample アプリケーションの URL ルーティング。

このモジュールは、Django REST Framework のルーターを使用して、
サンプルデータやカテゴリデータにアクセスするためのエンドポイントを定義します。
これにより、API クライアントはこれらのデータを簡単に操作でき、
効率的なデータ管理と操作を可能にします。

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

from django.urls import path, include
from rest_framework.routers import DefaultRouter

# ルーターのインスタンスを作成
router = DefaultRouter()
# サンプル用のエンドポイントを登録
# router.register(r'samples', PostViewSet, basename='sample')
# カテゴリ用のエンドポイントを登録
# router.register(r'categories', CategoryViewSet, basename='category')

# URL パターンを定義
urlpatterns = [
    path('', include(router.urls)),  # ルーターで定義されたエンドポイントを含める
]
