"""
ビジネスロジックのためのサンプルサービス層。

このモジュールには、リポジトリを使用してビジネスロジックを実装するクラスが含まれています。

サービス層の目的:
- ビジネスロジックを集約し、ビューやコントローラーから分離する。
- データベース操作をリポジトリに委譲し、コードの再利用性を向上させる。
- アプリケーションのルールや制約を実装する。

使用用途:
- データの取得、作成、更新、削除などの操作を一元管理する。
- 入力データの検証や、関連するデータの整合性を確保する。
- 複数のリポジトリや外部サービスを統合して処理を行う。
- ビジネスルールに基づいたエラーハンドリングを実装する。
- データの状態に応じた追加処理 (例: 公開日時の自動設定、閲覧数のインクリメント) を行う。

このモジュールに含まれるクラス:
- `SampleService`: サンプルデータに関するビジネスロジックを管理。
- `CategoryService`: カテゴリデータに関するビジネスロジックを管理。
"""

from typing import List, Optional
from django.utils import timezone
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from .models import Sample, Category
from .repositories import SampleRepository, CategoryRepository


class SampleService:
    """
    サンプル関連のビジネスロジックを管理するサービス。

    このクラスは、リポジトリを使用してデータベース操作を行い、
    アプリケーションのビジネスルールを実装します。
    """
    
    def __init__(self):
        self.repository = SampleRepository()
        self.category_repository = CategoryRepository()
    
    def get_samples(self, skip: int = 0, limit: int = 100, published_only: bool = False) -> List[Sample]:
        """
        ページネーションを使用してすべてのサンプルを取得します。

        パラメータ:
        - skip: スキップするレコード数。
        - limit: 取得するレコードの最大数。
        - published_only: 公開済みのサンプルのみを取得するかどうか。

        戻り値:
        - List[Sample]: サンプルのリスト。
        """
        if skip < 0 or limit < 1:
            raise ValidationError("Invalid pagination parameters.")
        
        if published_only:
            return list(self.repository.get_published(skip, limit))
        return list(self.repository.get_all(skip, limit))
    
    def get_sample(self, sample_id: int) -> Sample:
        """
        IDでサンプルを取得します。

        パラメータ:
        - sample_id: サンプルの一意の識別子。

        戻り値:
        - Sample: 該当するサンプルオブジェクト。

        例外:
        - NotFound: サンプルが見つからない場合。
        """
        sample = self.repository.get_by_id(sample_id)
        if not sample:
            raise NotFound("Sample not found.")
        return sample
    
    def get_sample_by_slug(self, slug: str) -> Sample:
        """Get sample by slug."""
        sample = self.repository.get_by_slug(slug)
        if not sample:
            raise NotFound(f'Sample with slug {slug} not found')
        return sample
    
    def get_samples_by_author(self, author_id: int, skip: int = 0, limit: int = 100) -> List[Sample]:
        """Get samples by author."""
        return list(self.repository.get_by_author(author_id, skip, limit))
    
    def get_samples_by_category(self, category_id: int, skip: int = 0, limit: int = 100) -> List[Sample]:
        """Get samples by category."""
        return list(self.repository.get_by_category(category_id, skip, limit))
    
    def create_sample(self, author_id: int, **kwargs) -> Sample:
        """
        新しいサンプルを作成します。

        パラメータ:
        - author_id: 作成者の一意の識別子。
        - kwargs: サンプルのフィールドデータ。

        戻り値:
        - Sample: 作成されたサンプルオブジェクト。
        """
        # Validate category if provided
        category_id = kwargs.get('category_id')
        if category_id:
            category = self.category_repository.get_by_id(category_id)
            if not category:
                raise ValidationError({'category': f'Category with id {category_id} not found'})
        
        # Set published_at if publishing
        if kwargs.get('is_published') and not kwargs.get('published_at'):
            kwargs['published_at'] = timezone.now()
        
        sample = self.repository.create(author_id=author_id, **kwargs)
        return sample
    
    def update_sample(self, sample_id: int, user_id: int, is_staff: bool = False, **kwargs) -> Sample:
        """
        既存のサンプルを更新します。

        パラメータ:
        - sample_id: 更新対象のサンプルID。
        - user_id: 更新を試みるユーザーのID。
        - is_staff: ユーザーがスタッフ権限を持つかどうか。
        - kwargs: 更新するフィールドデータ。

        戻り値:
        - Sample: 更新されたサンプルオブジェクト。

        例外:
        - PermissionDenied: ユーザーが更新権限を持たない場合。
        - NotFound: サンプルが見つからない場合。
        """
        sample = self.get_sample(sample_id)
        
        # Check permissions
        if sample.author_id != user_id and not is_staff:
            raise PermissionDenied("You do not have permission to update this sample.")
        
        # Validate category if being updated
        category_id = kwargs.get('category_id')
        if category_id:
            category = self.category_repository.get_by_id(category_id)
            if not category:
                raise ValidationError({'category': f'Category with id {category_id} not found'})
        
        # Set published_at when publishing for the first time
        if kwargs.get('is_published') and not sample.is_published:
            kwargs['published_at'] = timezone.now()
        
        sample = self.repository.update(sample, **kwargs)
        return sample
    
    def delete_sample(self, sample_id: int, user_id: int, is_staff: bool = False) -> bool:
        """
        サンプルを削除します。

        パラメータ:
        - sample_id: 削除対象のサンプルID。
        - user_id: 削除を試みるユーザーのID。
        - is_staff: ユーザーがスタッフ権限を持つかどうか。

        戻り値:
        - bool: 削除が成功した場合はTrue。

        例外:
        - PermissionDenied: ユーザーが削除権限を持たない場合。
        - NotFound: サンプルが見つからない場合。
        """
        sample = self.get_sample(sample_id)
        
        # Check permissions
        if sample.author_id != user_id and not is_staff:
            raise PermissionDenied("You do not have permission to delete this sample.")
        
        return self.repository.delete(sample)
    
    def increment_views(self, sample_id: int) -> Sample:
        """
        サンプルの閲覧数をインクリメントします。

        パラメータ:
        - sample_id: 対象のサンプルID。

        戻り値:
        - Sample: 更新されたサンプルオブジェクト。
        """
        sample = self.get_sample(sample_id)
        return self.repository.increment_views(sample)
    
    def search_samples(self, query: str) -> List[Sample]:
        """
        クエリ文字列に基づいてサンプルを検索します。

        パラメータ:
        - query: 検索クエリ文字列。

        戻り値:
        - List[Sample]: 一致するサンプルのリスト。
        """
        return list(self.repository.search(query))


class CategoryService:
    """
    カテゴリ関連のビジネスロジックを管理するサービス。

    このクラスは、カテゴリデータの取得や操作を行います。
    """
    
    def __init__(self):
        self.repository = CategoryRepository()
    
    def get_categories(self) -> List[Category]:
        """
        すべてのカテゴリを取得します。

        戻り値:
        - List[Category]: カテゴリのリスト。
        """
        return list(self.repository.get_all())
    
    def get_category(self, category_id: int) -> Category:
        """
        IDでカテゴリを取得します。

        パラメータ:
        - category_id: カテゴリの一意の識別子。

        戻り値:
        - Category: 該当するカテゴリオブジェクト。

        例外:
        - NotFound: カテゴリが見つからない場合。
        """
        category = self.repository.get_by_id(category_id)
        if not category:
            raise NotFound("Category not found.")
        return category
