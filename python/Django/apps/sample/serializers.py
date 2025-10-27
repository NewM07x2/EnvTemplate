"""
REST API用のサンプルシリアライザ。

このモジュールには、Django REST Frameworkを使用して、
サンプルとカテゴリのデータをシリアライズおよびデシリアライズするためのクラスが含まれています。

シリアライザの目的:
- モデルインスタンスをJSON形式に変換してクライアントに返す (シリアライズ)。
- クライアントから送信されたJSONデータを検証し、モデルインスタンスに変換する (デシリアライズ)。

使用用途:
- APIのエンドポイントでデータの入出力を管理する。
- データの検証ロジックを簡潔に記述する。
- ネストされたデータ構造を扱いやすくする。
- クライアントから送信されたデータのバリデーションチェックを行う。
  - 必須フィールドの確認。
  - データ型や値の範囲の検証。
  - カスタムバリデーションロジックの実装。
- データの整形:
  - クライアントに返すデータを整形し、必要な情報のみを含める。
  - ネストされたデータ構造を簡単に扱えるようにする。
- データの変換:
  - モデルインスタンスをシリアライズしてJSON形式に変換。
  - クライアントから送信されたJSONデータをデシリアライズしてモデルインスタンスに変換。
- エラーメッセージの提供:
  - バリデーションエラーが発生した場合、詳細なエラーメッセージをクライアントに返す。
- APIの一貫性の確保:
  - データの入出力形式を統一し、APIの一貫性を保つ。

各シリアライザの役割:
- `CategorySerializer`: カテゴリデータの読み取り専用シリアライザ。
- `SampleSerializer`: サンプルデータの読み取り専用シリアライザ。
- `SampleCreateSerializer`: サンプルデータの作成用シリアライザ。
- `SampleUpdateSerializer`: サンプルデータの更新用シリアライザ。
"""

from rest_framework import serializers
from .models import Sample, Category
from apps.users.serializers import UserSerializer


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
