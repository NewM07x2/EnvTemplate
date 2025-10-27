# GraphQL ガイド

## 概要

GraphQLは、APIのためのクエリ言語であり、既存のデータを使用してこれらのクエリを実行するためのランタイムです。REST APIの代替として、より柔軟で効率的な方法を提供し、クライアントが必要なデータのみをリクエストできるようにします。

このプロジェクトでは、`graphene-django`を使用してDjangoとGraphQLを統合し、スキーマ、クエリ、ミューテーションを定義してバックエンドとやり取りできるようにしています。

---

## インストール

以下の依存関係が`requirements.txt`にインストールされていることを確認してください：

```plaintext
# GraphQL
graphene-django>=3.2.0
graphql-core>=3.2.0
```

まだインストールされていない場合は、これらを追加して以下を実行してください：

```bash
pip install -r requirements.txt
```

---

## DjangoでのGraphQL設定

1. **`graphene_django`をインストール済みアプリに追加**：

   `settings.py`に以下を追加します：

   ```python
   INSTALLED_APPS = [
       ...
       'graphene_django',
   ]
   ```

2. **GraphQLエンドポイントを設定**：

   `urls.py`に以下を追加します：

   ```python
   from django.urls import path
   from graphene_django.views import GraphQLView

   urlpatterns = [
       ...
       path("graphql/", GraphQLView.as_view(graphiql=True)),
   ]
   ```

   これにより、クエリをテストするためのGraphiQLインターフェースを備えた`/graphql/`エンドポイントが設定されます。

---

## スキーマの定義

1. **GraphQLタイプを作成**：

   `DjangoObjectType`を使用してモデルのタイプを定義します：

   ```python
   from graphene_django import DjangoObjectType
   from .models import Sample

   class SampleType(DjangoObjectType):
       class Meta:
           model = Sample
           fields = ("id", "title", "content")
   ```

2. **クエリを定義**：

   データを取得するためのクエリクラスを作成します：

   ```python
   import graphene

   class Query(graphene.ObjectType):
       samples = graphene.List(SampleType)

       def resolve_samples(self, info):
           return Sample.objects.all()
   ```

3. **ミューテーションを定義**：

   データを作成または更新するためのミューテーションを追加します：

   ```python
   class CreateSample(graphene.Mutation):
       class Arguments:
           title = graphene.String(required=True)
           content = graphene.String(required=True)

       sample = graphene.Field(SampleType)

       def mutate(self, info, title, content):
           sample = Sample.objects.create(title=title, content=content)
           return CreateSample(sample=sample)

   class Mutation(graphene.ObjectType):
       create_sample = CreateSample.Field()
   ```

4. **スキーマを統合**：

   クエリとミューテーションをスキーマに統合します：

   ```python
   schema = graphene.Schema(query=Query, mutation=Mutation)
   ```

---

## GraphQLのテスト

1. **GraphiQLを使用**：

   ブラウザで`/graphql/`にアクセスしてGraphiQLインターフェースを開き、クエリやミューテーションをテストできます。

2. **クエリの例**：

   ```graphql
   query {
       samples {
           id
           title
           content
       }
   }
   ```

3. **ミューテーションの例**：

   ```graphql
   mutation {
       createSample(title: "New Sample", content: "Sample Content") {
           sample {
               id
               title
           }
       }
   }
   ```

---

## コード生成

フロントエンド用のGraphQLコードを生成するには、Apollo CodegenやRelay Compilerなどのツールを使用できます。これらのツールは、GraphQLスキーマとクエリを解析して型安全なコードを生成します。

### Apollo Codegen

Apollo Codegenは、GraphQLスキーマとクエリから型定義を生成するためのツールです。TypeScriptやFlowなど、さまざまなターゲットに対応しています。

1. **インストール**:

   ```bash
   npm install -g @apollo/cli
   ```

2. **コード生成の実行**:

   ```bash
   apollo client:codegen --target=typescript --endpoint=http://localhost:8000/graphql/
   ```

   - `--target`: 出力形式を指定します（例: `typescript`, `flow`）。
   - `--endpoint`: GraphQLエンドポイントのURLを指定します。

3. **出力例**:
   クエリに基づいて型定義が生成されます。

   ```typescript
   export type SampleQuery = {
       samples: Array<{
           id: string;
           title: string;
           content: string;
       }>;
   };
   ```

### Relay Compiler

Relay Compilerは、Facebookが開発したGraphQLクエリのコンパイルツールで、Reactアプリケーションでの使用に最適化されています。

1. **インストール**:

   ```bash
   npm install -g relay-compiler
   ```

2. **コード生成の実行**:

   ```bash
   relay-compiler --src ./src --schema ./schema.graphql
   ```

   - `--src`: ソースコードのディレクトリを指定します。
   - `--schema`: GraphQLスキーマファイルを指定します。

3. **出力例**:
   Relay用のフラグメントやクエリが生成されます。

   ```javascript
   graphql`
       query SampleQuery {
           samples {
               id
               title
               content
           }
       }
   `;
   ```

### その他のツール

- **GraphQL Code Generator**:
  - より柔軟でカスタマイズ可能なコード生成ツール。
  - TypeScript、React、Angularなど、さまざまなフレームワークに対応。
  - [公式ドキュメント](https://www.graphql-code-generator.com/)を参照してください。

- **Introspection Query**:
  - GraphQLスキーマを取得するためのクエリ。
  - スキーマをJSON形式でエクスポートし、他のツールで使用できます。

  ```bash
  curl -X POST -H "Content-Type: application/json" \
       --data '{"query": "{ __schema { types { name } } }"}' \
       http://localhost:8000/graphql/
  ```

---

コード生成ツールを使用することで、フロントエンドとバックエンド間の整合性を保ちながら、開発効率を向上させることができます。

---

## ベストプラクティス

- **わかりやすいフィールド名を使用**：スキーマフィールドが直感的で説明的であることを確認してください。
- **大規模なクエリをページネーションする**：`skip`や`limit`のような引数を使用して結果をページネーションします。
- **ミューテーションを安全に**：機密操作を実行する前にユーザーの権限を検証します。
- **スキーマを文書化**：コメントやGraphiQLのようなツールを使用してスキーマを適切に文書化します。

---

このガイドは、DjangoプロジェクトでGraphQLを設定および使用するための包括的な概要を提供します。詳細については、公式の[Graphene-Djangoドキュメント](https://docs.graphene-python.org/projects/django/en/latest/)を参照してください。