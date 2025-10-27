from django.contrib import admin
from ..models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Categoryモデルの管理画面設定。

    表示フィールド、検索フィールド、フィルタリングオプションなどを定義します。
    """
    
    list_display = ['name', 'slug', 'created_at']  # 一覧画面に表示するフィールド
    list_filter = ['created_at']  # サイドバーでのフィルタリングオプション
    search_fields = ['name', 'slug', 'description']  # 検索可能なフィールド
    prepopulated_fields = {'slug': ('name',)}  # nameフィールドからslugを自動生成
    ordering = ['name']  # デフォルトの並び順