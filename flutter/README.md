# Flutter アプリケーションテンプレート

このフォルダには、新規 Flutter アプリケーションを素早く作成するためのテンプレートが含まれています。

## 📁 構成

```
flutter/
├── setup_new_app.ps1           # 新規アプリセットアップスクリプト (Windows)
├── flutter_application_sample/  # テンプレートプロジェクト
└── README.md                    # このファイル
```

## 🚀 新規アプリの作成方法

### Windows (PowerShell)

```powershell
# flutterフォルダに移動
cd c:\Users\masato.nitta\mnitta\my-devlop\EnvTemplate\flutter

# セットアップスクリプトを実行
.\setup_new_app.ps1 -AppName "my_new_app" -DisplayName "My New App" -PackageId "com.example.mynewapp"
```

### パラメータ説明

- **AppName**: プロジェクト名 (スネークケース推奨: `my_app`)
- **DisplayName**: アプリの表示名 (日本語可: `私のアプリ`)
- **PackageId**: パッケージ ID/バンドル ID (例: `com.company.appname`)

### 例

```powershell
# シンプルなアプリ
.\setup_new_app.ps1 -AppName "todo_app" -DisplayName "Todo App" -PackageId "com.mycompany.todoapp"

# 日本語表示名のアプリ
.\setup_new_app.ps1 -AppName "shopping_list" -DisplayName "買い物リスト" -PackageId "jp.mycompany.shopping"
```

## 📝 セットアップ後の手順

```bash
# 1. 新しいアプリフォルダに移動
cd my_new_app

# 2. 依存関係をインストール
flutter pub get

# 3. アプリを実行
flutter run
```

## 🔧 テンプレートの特徴

### 含まれているもの

- ✅ 基本的な Material アプリ構造
- ✅ マルチプラットフォーム対応 (Android, iOS, Web, Windows, macOS, Linux)
- ✅ 基本的なウィジェットテスト
- ✅ Linter 設定 (flutter_lints)
- ✅ Prisma スキーマの基本構造

### プラットフォーム別の設定

#### Android

- Kotlin 対応
- Java 11 準拠
- Gradle KTS (Kotlin DSL)

#### iOS

- Swift 対応
- Info.plist 設定済み

## ⚠️ 注意事項

### iOS バンドル ID の手動確認が必要な場合

スクリプトはほとんどの設定を自動で変更しますが、以下のファイルは手動確認を推奨します:

```
ios/Runner.xcodeproj/project.pbxproj
```

Xcode で開いて、`PRODUCT_BUNDLE_IDENTIFIER`を確認してください。

### リリースビルド前の確認事項

1. **Android 署名設定**: `android/app/build.gradle.kts`の署名設定を本番用に変更
2. **アプリアイコン**: デフォルトアイコンを独自のものに変更
3. **スプラッシュスクリーン**: 必要に応じてカスタマイズ

## 📚 推奨される次のステップ

1. **状態管理の追加**: Provider, Riverpod, Bloc など
2. **ルーティング**: go_router の導入
3. **API 連携**: dio, http パッケージの追加
4. **データベース**: sqflite, hive の導入
5. **テスト**: integration_test の追加

## 🔄 テンプレートの更新

テンプレート自体を更新する場合は、`flutter_application_sample`フォルダを編集してください。

```bash
cd flutter_application_sample
flutter pub upgrade
flutter pub outdated
```

## 📖 関連ドキュメント

- [Flutter 公式ドキュメント](https://flutter.dev/docs)
- [Dart 公式ドキュメント](https://dart.dev/guides)
- [Flutter パッケージ](https://pub.dev/)
