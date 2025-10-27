from typing import Optional
from django.db.models import QuerySet
from ..models import Category

class CategoryRepository:
    """
    Categoryモデルの操作を管理するリポジトリ。

    このクラスは、カテゴリデータの取得や検索を行うためのメソッドを提供します。
    """

    @staticmethod
    def get_all() -> QuerySet:
        """
        すべてのカテゴリを取得します。

        戻り値:
        - QuerySet: カテゴリのリスト。
        """
        return Category.objects.all()

    @staticmethod
    def get_by_id(category_id: int) -> Optional[Category]:
        """
        IDでカテゴリを取得します。

        パラメータ:
        - category_id: カテゴリの一意の識別子。

        戻り値:
        - Category: 該当するカテゴリオブジェクト、またはNone。
        """
        try:
            return Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return None

    @staticmethod
    def get_by_slug(slug: str) -> Optional[Category]:
        """
        スラッグでカテゴリを取得します。

        パラメータ:
        - slug: カテゴリのスラッグ。

        戻り値:
        - Category: 該当するカテゴリオブジェクト、またはNone。
        """
        try:
            return Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return None