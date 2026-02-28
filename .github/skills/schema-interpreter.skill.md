# SKILL: schema-interpreter (DB定義読解スキル)

## 🎯 目的
リポジトリ内の物理的なDB定義（DDL, Entity, SQL）を正確に読み取り、ビジネスロジックと物理構造の間に「解釈の乖離」が生じないようにする。

## 🛠️ 実行手順 (Standard Operating Procedure)

### Step 1: 真実の源泉の特定
まず、以下の優先順位で対象テーブルの定義ファイルを探し出し、内容を読み取れ。
1. `src/main/resources/db/migration/` または `schema.sql` (DDL)
2. `facility-design-doc/table_definition/`(yaml)
3. `src/main/java/.../entity/` (JPA/MyBatis Entityクラス)
4. `src/main/resources/.../mapper/` (既存のMyBatis XML)

### Step 2: メタデータの抽出
特定したソースから、以下の情報をリストアップせよ。
- **カラム名と型:** 物理名、データ型、長さ。
- **制約:** Primary Key, Foreign Key, Unique, Not Null。
- **リレーション:** どのテーブルとどのカラムで紐付いているか。
- **論理名:** コメント（COMMENT ON）等から、そのカラムが業務上何を意味するか。

### Step 3: インパクト整合性チェック
今回の仕様（Spec）に対し、以下の観点で矛盾がないか確認せよ。
- **型不一致:** Java側で扱う型とDBの型に変換不可能な乖離はないか？
- **制約違反:** 仕様上Nullを許容するが、DB側がNot Nullになっていないか？
- **欠落情報:** 仕様を実現するために必要なカラムが、既存テーブルに不足していないか？

## 📋 出力フォーマット (Schema Context Report)
調査結果は、思考プロセス内または回答の冒頭で以下の形式で提示せよ。

> ### 📊 Schema Analysis Report
> - **Target Table:** `TABLE_NAME`
> - **Key Columns:** `COL_A (TYPE, PK)`, `COL_B (TYPE, FK -> TBL_C)`
> - **Observations:** (例：`tower_height`は物理的には`DECIMAL(10,2)`で管理されているため、Java側も`BigDecimal`で扱う必要がある)

## 🔴 禁止事項
- **記憶による推測:** 過去のチャット履歴や一般的な常識からカラム名を捏造してはならない。必ず `@workspace` でファイルを確認すること。
- **曖昧なマッピング:** 物理名と業務上の名称が一致しない場合、勝手に紐付けず、必ず `steering/domain/` を参照するかユーザーに確認せよ。