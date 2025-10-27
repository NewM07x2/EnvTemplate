"""
Postモデルの管理画面設定。

このモジュールには、Django管理画面でのPostおよびCategoryモデルの表示方法をカスタマイズするクラスが含まれています。
"""

from django.contrib import admin
from .models import Post, Category


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


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Postモデルの管理画面設定。

    表示フィールド、検索フィールド、フィルタリングオプション、
    および詳細画面のフィールドセットを定義します。
    """
    
    list_display = [
        'title', 'author', 'category', 'is_published',
        'published_at', 'views_count', 'created_at'
    ]  # 一覧画面に表示するフィールド
    list_filter = ['is_published', 'category', 'created_at', 'published_at']  # フィルタリングオプション
    search_fields = ['title', 'content', 'excerpt']  # 検索可能なフィールド
    prepopulated_fields = {'slug': ('title',)}  # titleフィールドからslugを自動生成
    ordering = ['-created_at']  # デフォルトの並び順
    date_hierarchy = 'created_at'  # 日付ベースのナビゲーション
    
    fieldsets = (
        ('基本情報', {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('コンテンツ', {
            'fields': ('content', 'excerpt')
        }),
        ('公開設定', {
            'fields': ('is_published', 'published_at')
        }),
        ('統計情報', {
            'fields': ('views_count', 'likes_count'),
            'classes': ('collapse',)  # 折りたたみ可能
        }),
        ('タイムスタンプ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # 折りたたみ可能
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'views_count', 'likes_count']  # 読み取り専用フィールド
