from ..models import Category

class CategoryService:
    """
    カテゴリデータに関するビジネスロジックを提供するサービスクラス。
    """

    def get_all_categories(self):
        """
        すべてのカテゴリを取得します。
        """
        return Category.objects.all()

    def get_category(self, category_id):
        """
        IDで特定のカテゴリを取得します。
        """
        return Category.objects.get(id=category_id)