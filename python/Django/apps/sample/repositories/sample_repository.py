from typing import Optional
from django.db.models import QuerySet, Q
from ..models import Sample

class SampleRepository:
    """
    サンプルデータにアクセスするためのリポジトリクラス。
    データベース操作をカプセル化し、サービス層に提供します。
    """

    @staticmethod
    def get_all_samples() -> QuerySet:
        """
        すべてのサンプルを取得します。

        戻り値:
        - QuerySet: サンプルのリスト。
        """
        return Sample.objects.all()

    @staticmethod
    def get_sample_by_id(sample_id: int) -> Optional[Sample]:
        """
        IDを指定して特定のサンプルを取得します。

        パラメータ:
        - sample_id: サンプルの一意の識別子。

        戻り値:
        - Sample: 該当するサンプルオブジェクト、またはNone。
        """
        return Sample.objects.filter(id=sample_id).first()

    @staticmethod
    def create_sample(author_id: int, **kwargs) -> Sample:
        """
        新しいサンプルを作成します。

        パラメータ:
        - author_id: 作成者の一意の識別子。
        - kwargs: サンプルのフィールドデータ。

        戻り値:
        - Sample: 作成されたサンプルオブジェクト。
        """
        return Sample.objects.create(author_id=author_id, **kwargs)

    @staticmethod
    def update_sample(sample_id: int, **kwargs) -> Sample:
        """
        特定のサンプルを更新します。

        パラメータ:
        - sample_id: 更新対象のサンプルの一意の識別子。
        - kwargs: 更新するフィールドデータ。

        戻り値:
        - Sample: 更新されたサンプルオブジェクト。
        """
        sample = Sample.objects.filter(id=sample_id).first()
        if sample:
            for key, value in kwargs.items():
                setattr(sample, key, value)
            sample.save()
        return sample

    @staticmethod
    def delete_sample(sample_id: int) -> bool:
        """
        特定のサンプルを削除します。

        パラメータ:
        - sample_id: 削除対象のサンプルの一意の識別子。

        戻り値:
        - bool: 削除が成功した場合はTrue。
        """
        sample = Sample.objects.filter(id=sample_id).first()
        if sample:
            sample.delete()
        return sample

    @staticmethod
    def increment_views(sample: Sample) -> Sample:
        """
        サンプルの閲覧数をインクリメントします。

        パラメータ:
        - sample: 対象のサンプルオブジェクト。

        戻り値:
        - Sample: 更新されたサンプルオブジェクト。
        """
        sample.views_count += 1
        sample.save()
        return sample

    @staticmethod
    def search(query: str) -> QuerySet:
        """
        クエリ文字列に基づいてサンプルを検索します。

        パラメータ:
        - query: 検索クエリ文字列。

        戻り値:
        - QuerySet: 一致するサンプルのリスト。
        """
        return Sample.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).select_related('author', 'category').all()