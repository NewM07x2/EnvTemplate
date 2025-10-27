"""
リポジトリ層: データアクセスロジックを管理するモジュール。

このモジュールは、データベース操作を抽象化し、
サービス層や他のアプリケーションロジックから直接的なデータベース操作を分離します。
これにより、コードの再利用性が向上し、テストが容易になります。

主な内容:
- サンプルデータの取得、作成、更新、削除に関するメソッド。
- データベースクエリのカスタマイズ。

備考:
- `CategoryRepository`: カテゴリデータの取得や検索を行うためのリポジトリ。
  - `get_all`: すべてのカテゴリを取得。
  - `get_by_id`: IDでカテゴリを取得。
  - `get_by_slug`: スラッグでカテゴリを取得。

- `SampleRepository`: サンプルデータの取得、作成、更新、削除を行うリポジトリ。
  - `get_all_samples`: すべてのサンプルを取得。
  - `get_sample_by_id`: IDでサンプルを取得。
  - `create_sample`: 新しいサンプルを作成。
  - `update_sample`: サンプルを更新。
  - `delete_sample`: サンプルを削除。
  - `increment_views`: サンプルの閲覧数をインクリメント。
  - `search`: クエリ文字列に基づいてサンプルを検索。

- よく使用するアノテーション:
  - `@staticmethod`: クラスのインスタンスを必要としないメソッドを定義する際に使用。
  - `@classmethod`: クラス自体を引数として受け取るメソッドを定義する際に使用。
  - `@property`: メソッドを属性のようにアクセス可能にする際に使用。
  - `@transaction.atomic`: トランザクションを管理する際に使用。
  - `@cached_property`: 計算コストの高いプロパティをキャッシュする際に使用。

"""

from typing import List, Optional
from django.db.models import QuerySet, Q
from .models import Sample, Category


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
