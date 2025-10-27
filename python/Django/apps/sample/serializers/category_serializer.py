from rest_framework import serializers
from ..models import Category

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