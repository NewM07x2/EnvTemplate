from ..models.about_model import About

class AboutService:
    """
    サンプルデータに関するビジネスロジックを提供するサービスクラス。
    """

    def get_abouts(self, skip=0, limit=100, published_only=False):
        """
        サンプルデータを取得します。
        """
        queryset = About.objects.all()
        if published_only:
            queryset = queryset.filter(is_published=True)
        return queryset[skip:skip + limit]

    def get_about(self, about_id):
        """
        IDで特定のサンプルを取得します。
        """
        return About.objects.get(id=about_id)

    def create_about(self, author_id, **data):
        """
        新しいサンプルを作成します。
        """
        return About.objects.create(author_id=author_id, **data)

    def update_about(self, about_id, user_id, is_staff, **data):
        """
        サンプルを更新します。
        """
        about = About.objects.get(id=about_id)
        if about.author_id != user_id and not is_staff:
            raise PermissionError("You do not have permission to update this about.")
        for key, value in data.items():
            setattr(about, key, value)
        about.save()
        return about

    def delete_about(self, about_id, user_id, is_staff):
        """
        サンプルを削除します。
        """
        about = About.objects.get(id=about_id)
        if about.author_id != user_id and not is_staff:
            raise PermissionError("You do not have permission to delete this about.")
        about.delete()

    def increment_views(self, about_id):
        """
        サンプルのビュー数を増加させます。
        """
        about = About.objects.get(id=about_id)
        about.views += 1
        about.save()