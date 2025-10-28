from rest_framework import serializers
from ..models.about_model import About

class AboutSerializer(serializers.ModelSerializer):
    """
    Aboutモデル用のシリアライザ。

    このシリアライザは、カテゴリデータをJSON形式に変換します。
    主に読み取り操作で使用されます。

    フィールド:
    - id: カテゴリの一意の識別子 (読み取り専用)。
    - context: カテゴリ名。
    - created_at: カテゴリの作成日時 (読み取り専用)。
    - updated_at: カテゴリの更新日時 (読み取り専用)。
    """
    
    class Meta:
        model = About
        fields = ['id', 'context', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']