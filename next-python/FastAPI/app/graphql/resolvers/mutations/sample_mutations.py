import strawberry

# @strawberry.mutation について
# ----------------------
# StrawberryのGraphQLスキーマで「ミューテーション（データの追加・更新・削除など）」として公開したい関数に付与するデコレーターです。
# これを付けたメソッドや関数はGraphQLのmutationとしてクライアントから呼び出せるようになります。
#
# 【特徴・補足】
# - Pythonの型ヒント（例：name: str）はGraphQLスキーマの型として反映されます。
# - 戻り値の型ヒントもGraphQLスキーマに反映されます。
# - クラスのメソッドだけでなく、単独の関数にも付与できます。
# - 複数のmutationを1つのMutationクラスにまとめてschema.pyで統合できます。
# - 認証や権限チェックなどもPython側で柔軟に実装可能です。
#
# 例（クラス外の関数として定義）:
#   @strawberry.mutation
#   def toggle_flag(id: int, enabled: bool) -> bool:
#       return enabled
#
# 詳細は公式ドキュメントも参照: https://strawberry.rocks/docs/guides/mutations

# サンプル用のミューテーション例
@strawberry.type
class SampleMutations:
    # insert
    @strawberry.mutation
    def insert_sample(self, name: str, value: int) -> str:
        """サンプルデータを追加するミューテーション"""
        return f"Sample '{name}' with value {value} added."

    @strawberry.mutation
    def bulk_insert_samples(self, samples: list[str]) -> int:
        """複数サンプルデータを一括追加"""
        return len(samples)

    # update
    @strawberry.mutation
    def update_sample(self, id: int, name: str) -> str:
        """サンプルデータの名前を更新するミューテーション"""
        return f"Sample id={id} updated to name '{name}'."

    @strawberry.mutation
    def patch_sample(self, id: int, name: str = None, value: int = None) -> bool:
        """サンプルデータの一部フィールドのみ更新"""
        return True

    @strawberry.mutation
    def bulk_update_samples(self, updates: list[dict]) -> int:
        """複数サンプルデータを一括更新"""
        # updates: [{"id": 1, "name": "a"}, ...]
        return len(updates)

    # delete
    @strawberry.mutation
    def delete_sample(self, id: int) -> bool:
        """サンプルデータを削除するミューテーション"""
        return True

    @strawberry.mutation
    def delete_samples(self, ids: list[int]) -> int:
        """複数サンプルデータを一括削除"""
        return len(ids)

    @strawberry.mutation
    def soft_delete_sample(self, id: int) -> bool:
        """サンプルデータの論理削除（削除フラグON）"""
        return True

    @strawberry.mutation
    def restore_sample(self, id: int) -> bool:
        """論理削除されたサンプルデータの復元"""
        return True

# ---
# 使用例：
# from .sample_mutations import SampleMutations
# mutation = SampleMutations()
# mutation.insert_sample(name="test", value=123)
# mutation.bulk_insert_samples(samples=["a", "b"])
# mutation.update_sample(id=1, name="newname")
# mutation.patch_sample(id=1, name="patched")
# mutation.bulk_update_samples(updates=[{"id":1,"name":"a"}])
# mutation.delete_sample(id=1)
# mutation.delete_samples(ids=[1,2,3])
# mutation.soft_delete_sample(id=1)
# mutation.restore_sample(id=1)