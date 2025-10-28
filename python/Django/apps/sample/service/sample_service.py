from ..models.sample_model import Sample

class SampleService:
    """
    サンプルデータに関するビジネスロジックを提供するサービスクラス。
    """

    def get_samples(self, skip=0, limit=100, published_only=False):
        """
        サンプルデータを取得します。
        """
        queryset = Sample.objects.all()
        if published_only:
            queryset = queryset.filter(is_published=True)
        return queryset[skip:skip + limit]

    def get_sample(self, sample_id):
        """
        IDで特定のサンプルを取得します。
        """
        return Sample.objects.get(id=sample_id)

    def create_sample(self, author_id, **data):
        """
        新しいサンプルを作成します。
        """
        return Sample.objects.create(author_id=author_id, **data)

    def update_sample(self, sample_id, user_id, is_staff, **data):
        """
        サンプルを更新します。
        """
        sample = Sample.objects.get(id=sample_id)
        if sample.author_id != user_id and not is_staff:
            raise PermissionError("You do not have permission to update this sample.")
        for key, value in data.items():
            setattr(sample, key, value)
        sample.save()
        return sample

    def delete_sample(self, sample_id, user_id, is_staff):
        """
        サンプルを削除します。
        """
        sample = Sample.objects.get(id=sample_id)
        if sample.author_id != user_id and not is_staff:
            raise PermissionError("You do not have permission to delete this sample.")
        sample.delete()

    def increment_views(self, sample_id):
        """
        サンプルのビュー数を増加させます。
        """
        sample = Sample.objects.get(id=sample_id)
        sample.views += 1
        sample.save()