# Flutter新規アプリセットアップスクリプト
# 使用方法: .\setup_new_app.ps1 -AppName "your_app_name" -DisplayName "Your App Name" -PackageId "com.yourcompany.yourapp"

param(
    [Parameter(Mandatory=$true)]
    [string]$AppName,
    
    [Parameter(Mandatory=$true)]
    [string]$DisplayName,
    
    [Parameter(Mandatory=$true)]
    [string]$PackageId
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Flutter新規アプリセットアップ" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "アプリ名: $AppName" -ForegroundColor Green
Write-Host "表示名: $DisplayName" -ForegroundColor Green
Write-Host "パッケージID: $PackageId" -ForegroundColor Green
Write-Host ""

# 現在のディレクトリを取得
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$templatePath = Join-Path $scriptPath "flutter_application_sample"
$newAppPath = Join-Path $scriptPath $AppName

# テンプレートフォルダの存在確認
if (-not (Test-Path $templatePath)) {
    Write-Host "エラー: テンプレートフォルダが見つかりません: $templatePath" -ForegroundColor Red
    exit 1
}

# 新しいアプリフォルダが既に存在する場合は警告
if (Test-Path $newAppPath) {
    Write-Host "警告: フォルダが既に存在します: $newAppPath" -ForegroundColor Yellow
    $response = Read-Host "上書きしますか? (y/N)"
    if ($response -ne "y") {
        Write-Host "セットアップをキャンセルしました。" -ForegroundColor Yellow
        exit 0
    }
    Remove-Item -Path $newAppPath -Recurse -Force
}

Write-Host ""
Write-Host "ステップ 1/4: テンプレートをコピー中..." -ForegroundColor Cyan
Copy-Item -Path $templatePath -Destination $newAppPath -Recurse

Write-Host "ステップ 2/4: pubspec.yamlを更新中..." -ForegroundColor Cyan
$pubspecPath = Join-Path $newAppPath "pubspec.yaml"
(Get-Content $pubspecPath) -replace 'name: flutter_application_sample', "name: $AppName" | Set-Content $pubspecPath

Write-Host "ステップ 3/4: Androidの設定を更新中..." -ForegroundColor Cyan
$buildGradlePath = Join-Path $newAppPath "android\app\build.gradle.kts"
(Get-Content $buildGradlePath) -replace 'namespace = "com.example.flutter_application_sample"', "namespace = `"$PackageId`"" | Set-Content $buildGradlePath
(Get-Content $buildGradlePath) -replace 'applicationId = "com.example.flutter_application_sample"', "applicationId = `"$PackageId`"" | Set-Content $buildGradlePath

Write-Host "ステップ 4/4: iOSの設定を更新中..." -ForegroundColor Cyan
$infoPlistPath = Join-Path $newAppPath "ios\Runner\Info.plist"
(Get-Content $infoPlistPath) -replace '<string>Flutter Application Sample</string>', "<string>$DisplayName</string>" | Set-Content $infoPlistPath
(Get-Content $infoPlistPath) -replace '<string>flutter_application_sample</string>', "<string>$AppName</string>" | Set-Content $infoPlistPath

Write-Host "ステップ 5/5: テストファイルを更新中..." -ForegroundColor Cyan
$testPath = Join-Path $newAppPath "test\widget_test.dart"
(Get-Content $testPath) -replace "import 'package:flutter_application_sample/main.dart';", "import 'package:$AppName/main.dart';" | Set-Content $testPath

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "セットアップ完了!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "次のステップ:" -ForegroundColor Yellow
Write-Host "1. cd $AppName" -ForegroundColor White
Write-Host "2. flutter pub get" -ForegroundColor White
Write-Host "3. flutter run" -ForegroundColor White
Write-Host ""
Write-Host "注意: iOSのバンドルIDは手動で確認・変更が必要な場合があります。" -ForegroundColor Yellow
Write-Host "ios/Runner.xcodeproj/project.pbxproj を確認してください。" -ForegroundColor Yellow
Write-Host ""
