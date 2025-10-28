from rest_framework import serializers
from ..models.sample_model import Sample
from ..models.category_model import Category
from ..models.sample_model import Sample
from ...users.serializer import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    """
    カテゴリモデル用のシリアライザ。

    このシリアライザは、カテゴリデータをJSON形式に変換します。
    主に読み取り操作で使用されます。

    フィールド:
    - id: カテゴリの一意の識別子 (読み取り専用)。
    - name: カテゴリ名。
    - slug: URLフレンドリーな一意の識別子。
    - description: カテゴリの説明。
    - created_at: カテゴリの作成日時 (読み取り専用)。
    - updated_at: カテゴリの更新日時 (読み取り専用)。
    """
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class SampleSerializer(serializers.ModelSerializer):
    """
    サンプルモデルの読み取り操作用シリアライザ。

    このシリアライザは、サンプルデータをJSON形式に変換します。
    主にクライアントにデータを返す際に使用されます。

    フィールド:
    - id: サンプルの一意の識別子 (読み取り専用)。
    - title: サンプルのタイトル。
    - slug: URLフレンドリーな一意の識別子。
    - content: サンプルの本文。
    - excerpt: サンプルの要約。
    - author: サンプルの作成者 (読み取り専用)。
    - category: サンプルのカテゴリ (読み取り専用)。
    - is_published: 公開ステータス。
    - published_at: 公開日時。
    - views_count: 閲覧数 (読み取り専用)。
    - likes_count: いいね数 (読み取り専用)。
    - created_at: サンプルの作成日時 (読み取り専用)。
    - updated_at: サンプルの更新日時 (読み取り専用)。
    """
    
    author = UserSerializer(read_only=True)  # 作成者情報をネストされた形式で表示
    category = CategorySerializer(read_only=True)  # カテゴリ情報をネストされた形式で表示
    
    class Meta:
        model = Sample
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt',
            'author', 'category', 'is_published', 'published_at',
            'views_count', 'likes_count', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'author', 'views_count', 'likes_count',
            'created_at', 'updated_at'
        ]

class SampleCreateSerializer(serializers.ModelSerializer):
    """
    サンプルモデルの作成操作用シリアライザ。

    このシリアライザは、新しいサンプルを作成する際に使用されます。
    クライアントからの入力データを検証し、データベースに保存可能な形式に変換します。

    フィールド:
    - title: サンプルのタイトル (必須)。
    - slug: URLフレンドリーな一意の識別子 (必須)。
    - content: サンプルの本文 (必須)。
    - excerpt: サンプルの要約 (任意)。
    - category: サンプルのカテゴリ (任意)。
    - is_published: 公開ステータス (デフォルト: False)。
    - published_at: 公開日時 (任意)。
    """
    
    class Meta:
        model = Sample
        fields = [
            'title', 'slug', 'content', 'excerpt',
            'category', 'is_published', 'published_at'
        ]

class SampleUpdateSerializer(serializers.ModelSerializer):
    """
    サンプルモデルの更新操作用シリアライザ。

    このシリアライザは、既存のサンプルを更新する際に使用されます。
    クライアントからの入力データを検証し、更新可能な形式に変換します。

    フィールド:
    - title: サンプルのタイトル (任意)。
    - slug: URLフレンドリーな一意の識別子 (任意)。
    - content: サンプルの本文 (任意)。
    - excerpt: サンプルの要約 (任意)。
    - category: サンプルのカテゴリ (任意)。
    - is_published: 公開ステータス (任意)。
    - published_at: 公開日時 (任意)。
    """
    
    class Meta:
        model = Sample
        fields = [
            'title', 'slug', 'content', 'excerpt',
            'category', 'is_published', 'published_at'
        ]