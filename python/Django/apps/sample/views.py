"""
サンプルのビュー (コントローラー) を提供するREST API。

目的:
このモジュールは、Django REST Frameworkを使用して、
サンプルとカテゴリのデータを管理および操作するためのViewSetを実装しています。
これにより、CRUD操作やカスタムアクションを通じて、
効率的なデータ管理と柔軟なAPIエンドポイントの提供を可能にします。

使用用途:
- サンプルデータの作成、取得、更新、削除 (CRUD操作)
- カテゴリデータの取得 (読み取り専用)
- カスタムアクションを通じた高度なデータ操作 (例: 検索、著者別フィルタリング)

備考:
- ViewSet: Django REST Frameworkのコンポーネントで、モデルに基づくCRUD操作を簡単に実装するためのクラス。
- @extend_schema_view: drf-spectacularを使用して、各エンドポイントのスキーマ情報をカスタマイズするためのデコレータ。
- よく使用されるアノテーション:
  - @action: ViewSetにカスタムアクションを追加。
  - @extend_schema: エンドポイントのスキーマをカスタマイズ。
  - @extend_schema_view: ViewSet全体のスキーマを一括カスタマイズ。
  - @extend_schema_field: シリアライザフィールドのスキーマをカスタマイズ。
  - @api_view: 関数ベースのビューに使用。
  - @permission_classes: エンドポイントごとに認可クラスを適用。
  - @throttle_classes: スロットリングを適用。
  - @renderer_classes: カスタムレンダラーを適用。
  
補足:
※drf-spectacular は、Django REST Framework (DRF) 用のスキーマ生成ツールです。このツールは、OpenAPI 3.0 スキーマを自動的に生成し、API ドキュメントを簡単に作成するために使用されます。

"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Sample, Category
from .serializers import (
    SampleSerializer,
    SampleCreateSerializer,
    SampleUpdateSerializer,
    CategorySerializer
)
from .services import SampleService, CategoryService


@extend_schema_view(
    list=extend_schema(summary="すべてのサンプルを一覧表示", tags=["samples"]),
    retrieve=extend_schema(summary="IDでサンプルを取得", tags=["samples"]),
    create=extend_schema(summary="新しいサンプルを作成", tags=["samples"]),
    update=extend_schema(summary="サンプルを更新", tags=["samples"]),
    partial_update=extend_schema(summary="サンプルを部分的に更新", tags=["samples"]),
    destroy=extend_schema(summary="サンプルを削除", tags=["samples"]),
)
class SampleViewSet(viewsets.ModelViewSet):
    """
    サンプル操作を管理するためのViewSet。

    このViewSetは、Sampleモデルに対するCRUD操作を提供します。
    また、フィルタリングや検索のためのカスタムアクションも含まれています。
    """

    # Sampleオブジェクトを取得するためのクエリセットを定義
    queryset = Sample.objects.all()
    # 認証済みユーザーは変更可能、それ以外は読み取り専用
    permission_classes = [IsAuthenticatedOrReadOnly]
    # ビジネスロジックをカプセル化するサービス層を使用
    service = SampleService()

    def get_serializer_class(self):
        """
        アクションに応じた適切なシリアライザクラスを返します。

        - 'create': 入力検証のためにSampleCreateSerializerを使用。
        - 'update' または 'partial_update': 更新のためにSampleUpdateSerializerを使用。
        - デフォルト: 読み取り操作のためにSampleSerializerを使用。
        """
        if self.action == 'create':
            return SampleCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return SampleUpdateSerializer
        return SampleSerializer

    def list(self, request, *args, **kwargs):
        """
        サンプルを一覧表示し、オプションでページネーションやフィルタリングを行います。

        クエリパラメータ:
        - skip: スキップするレコード数 (デフォルト: 0)。
        - limit: 返すレコードの最大数 (デフォルト: 100)。
        - published: 公開ステータスでフィルタリング (デフォルト: false)。

        戻り値:
        - サンプルのリストを含むJSONレスポンス。
        """
        skip = int(request.query_params.get('skip', 0))
        limit = int(request.query_params.get('limit', 100))
        published_only = request.query_params.get('published', 'false').lower() == 'true'

        # サービス層を使用してサンプルを取得
        samples = self.service.get_samples(skip=skip, limit=limit, published_only=published_only)
        serializer = self.get_serializer(samples, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        IDで単一のサンプルを取得し、そのビュー数を増加させます。

        パラメータ:
        - pk: 取得するサンプルの主キー。

        戻り値:
        - サンプルの詳細を含むJSONレスポンス。
        """
        sample = self.service.get_sample(sample_id=int(pk))

        # ユーザーが著者でない場合、ビュー数を増加
        if not request.user.is_authenticated or request.user.id != sample.author_id:
            self.service.increment_views(sample_id=int(pk))

        serializer = self.get_serializer(sample)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        新しいサンプルを作成します。

        リクエストボディ:
        - サンプルデータを含むJSONペイロード。

        戻り値:
        - 作成されたサンプルの詳細とHTTP 201ステータスを含むJSONレスポンス。
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # サービス層を使用して新しいサンプルを作成
        sample = self.service.create_sample(
            author_id=request.user.id,
            **serializer.validated_data
        )
        output_serializer = SampleSerializer(sample)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        """
        既存のサンプルを更新します。

        パラメータ:
        - pk: 更新するサンプルの主キー。

        リクエストボディ:
        - 更新されたサンプルデータを含むJSONペイロード。

        戻り値:
        - 更新されたサンプルの詳細を含むJSONレスポンス。
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # サービス層を使用してサンプルを更新
        sample = self.service.update_sample(
            sample_id=int(pk),
            user_id=request.user.id,
            is_staff=request.user.is_staff,
            **serializer.validated_data
        )
        output_serializer = SampleSerializer(sample)

        return Response(output_serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        """
        IDでサンプルを削除します。

        パラメータ:
        - pk: 削除するサンプルの主キー。

        戻り値:
        - 成功メッセージとHTTP 204ステータスを含むJSONレスポンス。
        """
        self.service.delete_sample(
            sample_id=int(pk),
            user_id=request.user.id,
            is_staff=request.user.is_staff
        )
        return Response(
            {'message': 'サンプルが正常に削除されました'},
            status=status.HTTP_204_NO_CONTENT
        )

    @extend_schema(
        summary="著者によるサンプルの取得",
        tags=["samples"],
    )
    @action(detail=False, methods=['get'])
    def by_author(self, request):
        """
        特定の著者によって作成されたサンプルを取得します。

        クエリパラメータ:
        - author_id: 著者のID。
        - skip: スキップするレコード数 (デフォルト: 0)。
        - limit: 返すレコードの最大数 (デフォルト: 100)。

        戻り値:
        - 著者によるサンプルのリストを含むJSONレスポンス。
        """
        author_id = int(request.query_params.get('author_id'))
        skip = int(request.query_params.get('skip', 0))
        limit = int(request.query_params.get('limit', 100))

        # サービス層を使用して著者によるサンプルを取得
        samples = self.service.get_samples_by_author(
            author_id=author_id,
            skip=skip,
            limit=limit
        )
        serializer = SampleSerializer(samples, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="サンプルの検索",
        tags=["samples"],
    )
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        クエリ文字列に基づいてサンプルを検索します。

        クエリパラメータ:
        - q: 検索クエリ文字列。

        戻り値:
        - 一致するサンプルのリストを含むJSONレスポンス。
        """
        query = request.query_params.get('q', '')
        samples = self.service.search_samples(query=query)
        serializer = SampleSerializer(samples, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(summary="すべてのカテゴリを一覧表示", tags=["categories"]),
    retrieve=extend_schema(summary="IDでカテゴリを取得", tags=["categories"]),
)
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    カテゴリ操作を管理するためのViewSet (読み取り専用)。

    このViewSetは、Categoryモデルに対する読み取り専用操作を提供します。
    """

    # Categoryオブジェクトを取得するためのクエリセットを定義
    queryset = Category.objects.all()
    # すべての操作に単一のシリアライザクラスを使用
    serializer_class = CategorySerializer
    # 認証済みユーザーは読み取り可能、それ以外は閲覧のみ
    permission_classes = [IsAuthenticatedOrReadOnly]
    # ビジネスロジックをカプセル化するサービス層を使用
    service = CategoryService()

    def list(self, request, *args, **kwargs):
        """
        すべてのカテゴリを一覧表示します。

        戻り値:
        - カテゴリのリストを含むJSONレスポンス。
        """
        categories = self.service.get_all_categories()
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        IDで単一のカテゴリを取得します。

        パラメータ:
        - pk: 取得するカテゴリの主キー。

        戻り値:
        - カテゴリの詳細を含むJSONレスポンス。
        """
        category = self.service.get_category(category_id=int(pk))
        serializer = self.get_serializer(category)
        return Response(serializer.data)
