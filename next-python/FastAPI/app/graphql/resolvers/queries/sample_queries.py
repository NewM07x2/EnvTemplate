# このファイルはサンプルデータ取得用のGraphQLクエリ（queries）をまとめたものです。
# Strawberryの@strawberry.type/@strawberry.fieldアノテーションを使って、
# データ取得系のGraphQLエンドポイントを定義します。
#
# 【よく使うStrawberryのアノテーション】
# - @strawberry.type: GraphQLの型（Type）を定義。レスポンス型やクエリ・ミューテーションの型に使う。
# - @strawberry.field: クエリやミューテーションのフィールド（関数）を定義。@strawberry.typeのクラス内で使う。
# - @strawberry.input: Input型（複雑な入力値をまとめて渡す場合）を定義。
# - @strawberry.enum: Enum型（列挙型）を定義。
# - @strawberry.interface: インターフェース型（共通フィールドを持つ型）を定義。
# - @strawberry.union: Union型（複数型のいずれかを返す場合）を定義。
#
# 【使用方法】
# - Sample型やUser型など、取得したいデータの型を@strawberry.typeで定義します。
# - SampleQueriesクラスに@strawberry.typeを付与し、各取得用メソッドに@strawberry.fieldを付与します。
# - @strawberry.fieldを付けたメソッドはGraphQLのqueryとしてクライアントから呼び出せます。
# - 引数や戻り値の型ヒントはGraphQLスキーマに自動反映されます。
#
# 例：
#   @strawberry.field
#   def get_sample(self, id: int) -> Optional[Sample]:
#       ...
#
# 詳細は公式ドキュメントも参照: https://strawberry.rocks/docs/guides/queries

import strawberry
from typing import List, Optional

# --- 追加サンプル: Enum, Union, Interface, Relay風ページネーション、複雑なフィルタ ---
import enum

# Enum型の定義例
@strawberry.enum
class SampleStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

# Interface型の定義例
@strawberry.interface
class Node:
    id: int

# Union型の定義例
@strawberry.type
class ErrorResult:
    message: str

SampleOrError = strawberry.union("SampleOrError", (Sample, ErrorResult))

# Relay風ページネーション用の型
@strawberry.type
class SampleEdge:
    node: Sample
    cursor: str

@strawberry.type
class PageInfo:
    has_next_page: bool
    has_previous_page: bool
    start_cursor: Optional[str]
    end_cursor: Optional[str]

@strawberry.type
class SampleConnection:
    edges: List[SampleEdge]
    page_info: PageInfo

# サンプルデータ型の定義
@strawberry.type
class User:
    id: int
    name: str

@strawberry.type
class Sample:
    id: int
    name: str
    value: int
    user: Optional[User] = None

@strawberry.type
class SampleStats:
    total: int
    average: float

# サンプル用のクエリ凡例
@strawberry.type
class SampleQueries:
    # 単一取得
    @strawberry.field
    def get_sample(self, id: int) -> Optional[Sample]:
        """IDでサンプルデータを1件取得"""
        return Sample(id=id, name="sample", value=100)

    # Union型の返却例
    @strawberry.field
    def get_sample_or_error(self, id: int) -> SampleOrError:
        """IDが1ならSample, それ以外はエラーを返すUnion型サンプル"""
        if id == 1:
            return Sample(id=1, name="sample", value=100)
        return ErrorResult(message="Not found")

    # Enum型の利用例
    @strawberry.field
    def get_sample_status(self, id: int) -> SampleStatus:
        """サンプルの状態をEnum型で返す"""
        return SampleStatus.ACTIVE if id == 1 else SampleStatus.INACTIVE

    # Interface型の返却例
    @strawberry.field
    def get_node(self, id: int) -> Node:
        """Nodeインターフェース型の返却例（SampleはNodeを継承していると仮定）"""
        return Sample(id=id, name="sample", value=100)

    # Relay風ページネーション
    @strawberry.field
    def relay_samples(self, first: int = 2, after: Optional[str] = None) -> SampleConnection:
        """Relay仕様風のページネーション例"""
        samples = [Sample(id=i, name=f"sample{i}", value=i*10) for i in range(1, 6)]
        edges = [SampleEdge(node=s, cursor=str(s.id)) for s in samples[:first]]
        page_info = PageInfo(
            has_next_page=len(samples) > first,
            has_previous_page=False,
            start_cursor=edges[0].cursor if edges else None,
            end_cursor=edges[-1].cursor if edges else None,
        )
        return SampleConnection(edges=edges, page_info=page_info)

    # 複雑なフィルタ例
    @strawberry.field
    def filter_samples_advanced(self, name_contains: Optional[str] = None, min_value: Optional[int] = None) -> List[Sample]:
        """複数条件でサンプルデータをフィルタ"""
        all_samples = [Sample(id=1, name="alpha", value=10), Sample(id=2, name="beta", value=20), Sample(id=3, name="gamma", value=30)]
        result = all_samples
        if name_contains:
            result = [s for s in result if name_contains in s.name]
        if min_value is not None:
            result = [s for s in result if s.value >= min_value]
        return result

    # ネストしたリスト返却例
    @strawberry.field
    def nested_samples(self) -> List[List[Sample]]:
        """サンプルデータの2次元リストを返す例"""
        return [
            [Sample(id=1, name="a", value=10), Sample(id=2, name="b", value=20)],
            [Sample(id=3, name="c", value=30)]
        ]

    @strawberry.field
    def get_samples_by_ids(self, ids: List[int]) -> List[Sample]:
        """複数IDでサンプルデータを一括取得"""
        return [Sample(id=i, name=f"sample{i}", value=i*10) for i in ids]

    # リスト・検索・ページング
    @strawberry.field
    def list_samples(self) -> List[Sample]:
        """全サンプルデータをリスト取得"""
        return [Sample(id=1, name="a", value=10), Sample(id=2, name="b", value=20)]

    @strawberry.field
    def search_samples(self, keyword: str) -> List[Sample]:
        """キーワードでサンプルデータを検索"""
        return [Sample(id=1, name=keyword, value=999)]

    @strawberry.field
    def paginated_samples(self, offset: int = 0, limit: int = 10) -> List[Sample]:
        """ページネーション付きでサンプルデータを取得"""
        return [Sample(id=i, name=f"sample{i}", value=i*10) for i in range(offset+1, offset+limit+1)]

    @strawberry.field
    def list_samples_sorted(self, order_by: str = "id") -> List[Sample]:
        """指定フィールドでソートして取得"""
        return [Sample(id=1, name="a", value=10), Sample(id=2, name="b", value=20)]

    @strawberry.field
    def filter_samples(self, min_value: int = 0, max_value: int = 100) -> List[Sample]:
        """値の範囲でサンプルデータをフィルタ"""
        return [Sample(id=1, name="a", value=50)]

    # 関連・集計
    @strawberry.field
    def get_sample_with_user(self, id: int) -> Sample:
        """サンプルデータと紐づくユーザー情報を取得"""
        return Sample(id=id, name="sample", value=100, user=User(id=1, name="user"))

    @strawberry.field
    def sample_stats(self) -> SampleStats:
        """サンプルデータの合計・平均などの集計情報を返す"""
        return SampleStats(total=100, average=50.0)

    # 件数・存在チェック
    @strawberry.field
    def count_samples(self) -> int:
        """サンプルデータの件数を取得"""
        return 42

    @strawberry.field
    def exists_sample(self, id: int) -> bool:
        """指定IDのサンプルデータが存在するか判定"""
        return id == 1

# ---
# 使用例：
# from .sample_queries import SampleQueries
# query = SampleQueries()
# query.get_sample(id=1)
# query.get_samples_by_ids(ids=[1,2,3])
# query.list_samples()
# query.search_samples(keyword="test")
# query.paginated_samples(offset=0, limit=5)
# query.list_samples_sorted(order_by="name")
# query.filter_samples(min_value=10, max_value=100)
# query.get_sample_with_user(id=1)
# query.sample_stats()
# query.count_samples()
# query.exists_sample(id=1)
# query.get_sample_or_error(id=1)
# query.get_sample_status(id=1)
# query.get_node(id=1)
# query.relay_samples(first=2)
# query.filter_samples_advanced(name_contains="a", min_value=10)
# query.nested_samples()