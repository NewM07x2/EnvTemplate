# GoJS API リファレンス

> **対象者**: GoJS の API を逆引きしたい開発者  
> **形式**: 「やりたいこと → API」の逆引き辞典

---

## 📚 目次

1. [Diagram クラス](#1-diagram-クラス)
2. [Model クラス](#2-model-クラス)
3. [Node / Link / Group](#3-node--link--group)
4. [GraphObject 階層](#4-graphobject-階層)
5. [Shape の Figure 一覧](#5-shape-の-figure-一覧)
6. [Binding（データバインディング）](#6-bindingデータバインディング)
7. [トランザクション](#7-トランザクション)
8. [CommandHandler](#8-commandhandler)
9. [Tool クラス](#9-tool-クラス)
10. [Geometry（カスタムシェイプ）](#10-geometryカスタムシェイプ)
11. [逆引きリファレンス](#11-逆引きリファレンス)

---

## 1. Diagram クラス

ダイアグラム全体を管理するルートクラスです。

### 1.1 コンストラクタ

```typescript
const diagram = new go.Diagram(divId: string, init?: DiagramInitOptions);
```

### 1.2 主要プロパティ

| プロパティ | 型 | 説明 |
|---|---|---|
| `model` | `Model` | データモデル |
| `nodeTemplate` | `Node` | デフォルトのノードテンプレート |
| `nodeTemplateMap` | `Map<string, Node>` | カテゴリ別ノードテンプレート |
| `linkTemplate` | `Link` | デフォルトのリンクテンプレート |
| `linkTemplateMap` | `Map<string, Link>` | カテゴリ別リンクテンプレート |
| `groupTemplate` | `Group` | デフォルトのグループテンプレート |
| `layout` | `Layout` | レイアウトアルゴリズム |
| `selection` | `Set<Part>` | 選択中のパーツ集合（読み取り専用） |
| `scale` | `number` | ズーム倍率 |
| `minScale` | `number` | 最小ズーム |
| `maxScale` | `number` | 最大ズーム |
| `position` | `Point` | ビューポート位置 |
| `padding` | `Margin` | ダイアグラムのパディング |
| `autoScrollRegion` | `Margin` | 自動スクロール領域 |
| `allowCopy` | `boolean` | コピー許可 |
| `allowDelete` | `boolean` | 削除許可 |
| `allowDrop` | `boolean` | ドロップ許可 |
| `allowInsert` | `boolean` | 挿入許可 |
| `allowMove` | `boolean` | 移動許可 |
| `allowRelink` | `boolean` | リンク付替え許可 |
| `allowReshape` | `boolean` | 形状変更許可 |
| `allowResize` | `boolean` | リサイズ許可 |
| `allowRotate` | `boolean` | 回転許可 |
| `allowSelect` | `boolean` | 選択許可 |
| `allowTextEdit` | `boolean` | テキスト編集許可 |
| `allowUndo` | `boolean` | Undo許可 |
| `allowZoom` | `boolean` | ズーム許可 |
| `isReadOnly` | `boolean` | 読み取り専用（全操作無効） |
| `isModified` | `boolean` | 変更があったか |
| `animationManager` | `AnimationManager` | アニメーション管理 |
| `commandHandler` | `CommandHandler` | コマンドハンドラ |
| `toolManager` | `ToolManager` | ツール管理 |
| `undoManager` | `UndoManager` | Undo 管理（`model.undoManager` と共有） |
| `div` | `HTMLDivElement` | DOM 要素 |

### 1.3 主要メソッド

| メソッド | 引数 | 戻り値 | 説明 |
|---|---|---|---|
| `findNodeForKey(key)` | `any` | `Node \| null` | キーからノードを検索 |
| `findLinkForData(data)` | `ObjectData` | `Link \| null` | リンクデータからリンクを検索 |
| `findPartAt(point)` | `Point` | `Part \| null` | 座標のパーツを検索 |
| `findObjectAt(point)` | `Point` | `GraphObject \| null` | 座標のオブジェクトを検索 |
| `select(part)` | `Part` | `void` | パーツを選択 |
| `selectCollection(parts)` | `Iterable<Part>` | `void` | 複数パーツを選択 |
| `clearSelection()` | — | `void` | 選択を解除 |
| `scroll(unit, dir)` | `string, string` | `void` | スクロール |
| `scrollToRect(rect)` | `Rect` | `void` | 矩形が見える位置にスクロール |
| `centerRect(rect)` | `Rect` | `void` | 矩形を中央に表示 |
| `zoomToFit()` | — | `void` | 全体が見えるようにズーム |
| `zoomToRect(rect)` | `Rect` | `void` | 矩形に合わせてズーム |
| `layoutDiagram(invalidateAll)` | `boolean` | `void` | レイアウトを再計算 |
| `makeSvg(options)` | `object` | `SVGElement` | SVG を生成 |
| `makeImage(options)` | `object` | `HTMLImageElement` | 画像を生成 |
| `makeImageData(options)` | `object` | `string \| Blob` | 画像データを生成 |
| `addDiagramListener(name, fn)` | `string, Function` | `void` | イベントリスナー登録 |
| `removeDiagramListener(name, fn)` | `string, Function` | `void` | イベントリスナー解除 |
| `startTransaction(name)` | `string` | `boolean` | トランザクション開始 |
| `commitTransaction(name)` | `string` | `boolean` | トランザクション確定 |
| `rollbackTransaction()` | — | `boolean` | トランザクションをロールバック |

---

## 2. Model クラス

### 2.1 Model の種類

| クラス | 用途 | リンクの表現方式 |
|---|---|---|
| `go.Model` | ノードのみ（リンクなし） | — |
| `go.GraphLinksModel` | 任意のグラフ | 別配列 (`linkDataArray`) |
| `go.TreeModel` | ツリー構造 | 親キー (`nodeParentKeyProperty`) |

### 2.2 共通プロパティ

| プロパティ | 型 | 説明 |
|---|---|---|
| `nodeDataArray` | `ObjectData[]` | ノードデータの配列 |
| `nodeKeyProperty` | `string` | キープロパティ名（デフォルト: `"key"`） |
| `nodeCategoryProperty` | `string` | カテゴリプロパティ名（デフォルト: `"category"`） |
| `undoManager` | `UndoManager` | Undo管理 |

### 2.3 GraphLinksModel 固有プロパティ

| プロパティ | 型 | 説明 |
|---|---|---|
| `linkDataArray` | `ObjectData[]` | リンクデータの配列 |
| `linkFromKeyProperty` | `string` | リンク元キー名（デフォルト: `"from"`） |
| `linkToKeyProperty` | `string` | リンク先キー名（デフォルト: `"to"`） |
| `linkFromPortIdProperty` | `string` | リンク元ポートID名 |
| `linkToPortIdProperty` | `string` | リンク先ポートID名 |
| `linkKeyProperty` | `string` | リンクキー名 |

### 2.4 TreeModel 固有プロパティ

| プロパティ | 型 | 説明 |
|---|---|---|
| `nodeParentKeyProperty` | `string` | 親キープロパティ名（デフォルト: `"parent"`） |

### 2.5 主要メソッド

| メソッド | 説明 |
|---|---|
| `addNodeData(data)` | ノードデータを追加 |
| `removeNodeData(data)` | ノードデータを削除 |
| `findNodeDataForKey(key)` | キーからノードデータを検索 |
| `set(data, propName, value)` | プロパティを安全に更新 |
| `addLinkData(data)` | リンクデータを追加 ※GraphLinksModel |
| `removeLinkData(data)` | リンクデータを削除 ※GraphLinksModel |
| `toJson()` | JSON 文字列にシリアライズ |
| `Model.fromJson(json)` | JSON から Model を復元（静的メソッド） |
| `addChangedListener(fn)` | 変更リスナーを登録 |
| `removeChangedListener(fn)` | 変更リスナーを解除 |

---

## 3. Node / Link / Group

### 3.1 Part（共通基底クラス）

| プロパティ / メソッド | 型 | 説明 |
|---|---|---|
| `data` | `ObjectData` | バインドされたデータ |
| `key` | `any` | ノードキー |
| `category` | `string` | テンプレートカテゴリ |
| `isSelected` | `boolean` | 選択状態 |
| `location` | `Point` | 位置 |
| `actualBounds` | `Rect` | 実際の矩形領域 |
| `diagram` | `Diagram` | 所属するダイアグラム |
| `findObject(name)` | `GraphObject \| null` | 名前付きオブジェクトを検索 |
| `isVisible()` | `boolean` | 可視状態か |

### 3.2 Node 固有

| プロパティ / メソッド | 説明 |
|---|---|
| `findLinksConnected()` | 接続されている全リンクを取得 |
| `findLinksOutOf()` | 出ていくリンクを取得 |
| `findLinksInto()` | 入ってくるリンクを取得 |
| `findLinksTo(otherNode)` | 特定ノードへのリンクを取得 |
| `findNodesConnected()` | 接続されている全ノードを取得 |
| `findTreeRoot()` | ツリーのルートノードを取得 |
| `findTreeChildrenNodes()` | 子ノードを取得 |
| `findTreeParentNode()` | 親ノードを取得 |
| `isTreeExpanded` | ツリー展開状態 |
| `wasTreeExpanded` | 折りたたみ前の展開状態 |
| `port` | デフォルトポート |

### 3.3 Link 固有

| プロパティ / メソッド | 説明 |
|---|---|
| `fromNode` | リンク元ノード |
| `toNode` | リンク先ノード |
| `fromPort` | リンク元ポート |
| `toPort` | リンク先ポート |
| `points` | リンクの経由点リスト |
| `routing` | ルーティング方式 |
| `curve` | 曲線タイプ |
| `corner` | 角丸半径 |

### 3.4 Group 固有

| プロパティ / メソッド | 説明 |
|---|---|
| `memberParts` | グループ内のパーツ一覧 |
| `layout` | グループ内レイアウト |
| `placeholder` | Placeholder オブジェクト |
| `isSubGraphExpanded` | サブグラフの展開状態 |
| `findSubGraphParts()` | サブグラフの全パーツを取得 |

---

## 4. GraphObject 階層

```
GraphObject
├── Panel
│   ├── Part
│   │   ├── Node
│   │   │   └── Group
│   │   ├── Link
│   │   └── Adornment
│   └── (Auto / Horizontal / Vertical / Spot / Table / Grid ...)
├── Shape
├── TextBlock
├── Picture
└── Placeholder
```

### 4.1 GraphObject 共通プロパティ

| プロパティ | 型 | 説明 |
|---|---|---|
| `name` | `string` | 名前（`findObject()` で検索用） |
| `visible` | `boolean` | 可視性 |
| `opacity` | `number` | 不透明度 (0〜1) |
| `angle` | `number` | 回転角度 |
| `scale` | `number` | 拡大率 |
| `desiredSize` | `Size` | 希望サイズ |
| `minSize` | `Size` | 最小サイズ |
| `maxSize` | `Size` | 最大サイズ |
| `actualBounds` | `Rect` | 実際の矩形（読み取り専用） |
| `margin` | `Margin` | 外側余白 |
| `alignment` | `Spot` | Panel 内での配置位置 |
| `stretch` | `Stretch` | 引き伸ばし方式 |
| `cursor` | `string` | マウスカーソル |
| `background` | `string` | 背景色 |
| `part` | `Part` | 所属する Part |
| `panel` | `Panel` | 親 Panel |
| `diagram` | `Diagram` | 所属する Diagram |
| `click` | `Function` | クリックハンドラ |
| `doubleClick` | `Function` | ダブルクリックハンドラ |
| `contextClick` | `Function` | 右クリックハンドラ |
| `mouseEnter` | `Function` | マウス侵入ハンドラ |
| `mouseLeave` | `Function` | マウス退出ハンドラ |
| `toolTip` | `Adornment` | ツールチップ |
| `contextMenu` | `Adornment` | コンテキストメニュー |

### 4.2 Picture

```typescript
// 画像表示
new go.Picture({
  source: "https://example.com/icon.png",
  desiredSize: new go.Size(50, 50),
  imageStretch: go.ImageStretch.Uniform,
}).bind("source", "imageUrl")
```

| プロパティ | 型 | 説明 |
|---|---|---|
| `source` | `string` | 画像URL |
| `imageStretch` | `ImageStretch` | 画像の引き伸ばし |
| `imageAlignment` | `Spot` | 画像の配置位置 |
| `errorFunction` | `Function` | 読み込みエラー時の処理 |

---

## 5. Shape の Figure 一覧

### 基本図形

| Figure 名 | 形状 |
|---|---|
| `"Rectangle"` | 四角形 |
| `"RoundedRectangle"` | 角丸四角形 |
| `"Circle"` | 円 |
| `"Ellipse"` | 楕円 |
| `"Diamond"` | ひし形 |
| `"Triangle"` | 上向き三角形 |
| `"TriangleRight"` | 右向き三角形 |
| `"TriangleDown"` | 下向き三角形 |
| `"TriangleLeft"` | 左向き三角形 |
| `"Pentagon"` | 五角形 |
| `"Hexagon"` | 六角形 |
| `"Octagon"` | 八角形 |

### フローチャート図形

| Figure 名 | 形状 |
|---|---|
| `"Parallelogram1"` | 平行四辺形 |
| `"Trapezoid"` | 台形 |
| `"Cylinder1"` | シリンダー（DB） |
| `"Document"` | 書類 |
| `"ManualOperation"` | 手動操作 |
| `"Terminator"` | 端子（カプセル型） |
| `"Procedure"` | 定義済み処理 |
| `"Collate"` | 照合 |
| `"InternalStorage"` | 内部記憶 |

### 装飾図形

| Figure 名 | 形状 |
|---|---|
| `"Star"` | 星形 |
| `"Cloud"` | 雲 |
| `"Heart"` | ハート |
| `"Lightning"` | 稲妻 |
| `"Arrow"` | 矢印 |
| `"Gear"` | 歯車 |
| `"Ring"` | リング |
| `"FivePointedStar"` | 五芒星 |
| `"Burst"` | 爆発 |

### 矢印（リンク用）

| toArrow / fromArrow | 形状 |
|---|---|
| `"Standard"` | ▶ 三角矢印 |
| `"OpenTriangle"` | △ 開き三角 |
| `"BackwardOpenTriangle"` | ◁ 逆向き開き三角 |
| `"Circle"` | ● 丸 |
| `"Diamond"` | ◆ ダイヤ |
| `"StretchedDiamond"` | ◇ 横長ダイヤ |
| `"Triangle"` | ▶ 塗り三角 |
| `"Fork"` | ⊢ フォーク |
| `"Bowtie"` | ⋈ 蝶ネクタイ |

---

## 6. Binding（データバインディング）

### 6.1 コンストラクタ

```typescript
// 基本形
new go.Binding(targetProp: string, sourceProp?: string, converter?: Function)

// 例
new go.Binding("fill", "color")                        // data.color → shape.fill
new go.Binding("text", "score", (s) => `${s}点`)       // 変換付き
new go.Binding("fill")                                  // data.fill → shape.fill（同名）
```

### 6.2 メソッド

| メソッド | 説明 |
|---|---|
| `.makeTwoWay(backConverter?)` | 双方向バインドにする |
| `.ofObject(srcName?)` | 別の GraphObject をソースにする |
| `.ofModel()` | Model のプロパティをソースにする |

### 6.3 よく使うパターン

```typescript
// 位置の双方向バインド
new go.Binding("location", "loc", go.Point.parse).makeTwoWay(go.Point.stringify)

// サイズの双方向バインド
new go.Binding("desiredSize", "size", go.Size.parse).makeTwoWay(go.Size.stringify)

// 条件付き表示
new go.Binding("visible", "showDetails")

// テキスト編集の双方向バインド
new go.Binding("text").makeTwoWay()
```

---

## 7. トランザクション

```typescript
// ━━━ 基本パターン ━━━
diagram.startTransaction("operation name");
try {
  // モデル変更
  diagram.model.addNodeData({ key: 1, text: "New" });
  diagram.model.set(existingData, "color", "#FF0000");
  
  diagram.commitTransaction("operation name");
} catch (e) {
  diagram.rollbackTransaction();
  throw e;
}
```

### UndoManager

```typescript
// Undo/Redo を有効化
diagram.undoManager.isEnabled = true;  // ← "undoManager.isEnabled": true と同等

// Undo 可能か確認
diagram.undoManager.canUndo();  // boolean

// Redo 可能か確認
diagram.undoManager.canRedo();  // boolean

// Undo 実行
diagram.undoManager.undo();

// Redo 実行
diagram.undoManager.redo();

// 履歴をクリア
diagram.undoManager.clear();

// 最大履歴数を設定
diagram.undoManager.maxHistoryLength = 100;
```

---

## 8. CommandHandler

```typescript
const cmd = diagram.commandHandler;

// ━━━ クリップボード操作 ━━━
cmd.canCopySelection();   // コピー可能か
cmd.copySelection();      // コピー
cmd.canPasteSelection();  // 貼り付け可能か
cmd.pasteSelection();     // 貼り付け
cmd.canCutSelection();    // 切り取り可能か
cmd.cutSelection();       // 切り取り

// ━━━ 削除 ━━━
cmd.canDeleteSelection(); // 削除可能か
cmd.deleteSelection();    // 削除

// ━━━ 選択 ━━━
cmd.canSelectAll();       // 全選択可能か
cmd.selectAll();          // 全選択

// ━━━ Undo / Redo ━━━
cmd.canUndo();            // Undo 可能か
cmd.undo();               // Undo
cmd.canRedo();            // Redo 可能か
cmd.redo();               // Redo

// ━━━ ズーム ━━━
cmd.canIncreaseZoom();    // ズームイン可能か
cmd.increaseZoom(factor); // ズームイン
cmd.canDecreaseZoom();    // ズームアウト可能か
cmd.decreaseZoom(factor); // ズームアウト
cmd.canResetZoom();       // ズームリセット可能か
cmd.resetZoom();          // ズームを1.0に
cmd.canZoomToFit();       // 全体表示可能か
cmd.zoomToFit();          // 全体表示

// ━━━ グルーピング ━━━
cmd.canGroupSelection();    // グループ化可能か
cmd.groupSelection();       // グループ化
cmd.canUngroupSelection();  // グループ解除可能か
cmd.ungroupSelection();     // グループ解除

// ━━━ ツリー展開 ━━━
cmd.canCollapseTree();      // 折りたたみ可能か
cmd.collapseTree(node);     // 折りたたみ
cmd.canExpandTree();        // 展開可能か
cmd.expandTree(node);       // 展開
```

---

## 9. Tool クラス

```typescript
const tm = diagram.toolManager;

// ━━━ 主要ツールの取得 ━━━
tm.draggingTool;       // ドラッグツール
tm.linkingTool;        // リンク作成ツール
tm.relinkingTool;      // リンク付替えツール
tm.textEditingTool;    // テキスト編集ツール
tm.clickSelectingTool; // クリック選択ツール
tm.panningTool;        // パンツール
tm.dragSelectingTool;  // 範囲選択ツール
tm.resizingTool;       // リサイズツール
tm.rotatingTool;       // 回転ツール
tm.linkReshapingTool;  // リンク形状変更ツール

// ━━━ ツールの無効化 ━━━
tm.draggingTool.isEnabled = false;  // ドラッグ無効
tm.linkingTool.isEnabled = false;   // リンク作成無効

// ━━━ ホバー遅延 ━━━
tm.hoverDelay = 500;      // ホバー判定の遅延（ms）
tm.holdDelay = 800;       // ロングプレス判定の遅延（ms）
tm.toolTipDuration = 5000; // ツールチップの表示時間（ms）
```

---

## 10. Geometry（カスタムシェイプ）

```typescript
// ━━━ PathFigure で定義 ━━━
const geo = new go.Geometry();
const fig = new go.PathFigure(startX, startY, isFilled);
fig.add(new go.PathSegment(go.SegmentType.Line, x, y));
fig.add(new go.PathSegment(go.SegmentType.Bezier, x, y, cx1, cy1, cx2, cy2));
fig.add(new go.PathSegment(go.SegmentType.QuadraticBezier, x, y, cx, cy));
fig.add(new go.PathSegment(go.SegmentType.Arc, startAngle, sweepAngle, cx, cy, rx, ry));
fig.add(new go.PathSegment(go.SegmentType.Line, x, y).close()); // パスを閉じる
geo.add(fig);

// ━━━ SVG パス文字列から変換 ━━━
const geo2 = go.Geometry.parse("M 0 0 L 100 0 L 100 100 L 0 100 Z");

// ━━━ カスタム Figure の登録 ━━━
go.Shape.defineFigureGenerator("MyShape", (shape, w, h) => {
  // w, h はシェイプのサイズ
  const geo = new go.Geometry();
  // ... PathFigure を構築 ...
  return geo;
});
```

---

## 11. 逆引きリファレンス

### ダイアグラム操作

| やりたいこと | API |
|---|---|
| ダイアグラムを作成する | `new go.Diagram(divId, options)` |
| 読み取り専用にする | `diagram.isReadOnly = true` |
| 背景色を設定する | `div.style.backgroundColor = "#..."` |
| グリッド線を表示する | `diagram.grid.visible = true` |
| アニメーションを無効化する | `diagram.animationManager.isEnabled = false` |
| Undo/Redo を有効にする | `"undoManager.isEnabled": true` |

### ノード操作

| やりたいこと | API |
|---|---|
| ノードを追加する | `model.addNodeData(data)` |
| ノードを削除する | `model.removeNodeData(data)` |
| ノードのプロパティを更新する | `model.set(data, prop, value)` |
| キーでノードを検索する | `diagram.findNodeForKey(key)` |
| 全ノードをイテレートする | `diagram.nodes.each(fn)` |
| 選択中のノードを取得する | `diagram.selection.filter(p => p instanceof go.Node)` |
| ノードを中央に表示する | `diagram.centerRect(node.actualBounds)` |
| ノードの接続先を取得する | `node.findNodesConnected()` |
| ノードの子を取得する（ツリー） | `node.findTreeChildrenNodes()` |
| ノードの親を取得する（ツリー） | `node.findTreeParentNode()` |

### リンク操作

| やりたいこと | API |
|---|---|
| リンクを追加する | `(model as GraphLinksModel).addLinkData(data)` |
| リンクを削除する | `(model as GraphLinksModel).removeLinkData(data)` |
| ノード間のリンクを取得する | `nodeA.findLinksTo(nodeB)` |
| リンクの接続元ノードを取得する | `link.fromNode` |
| リンクの接続先ノードを取得する | `link.toNode` |
| リンクの経路を直交にする | `link.routing = go.Routing.Orthogonal` |
| リンクを曲線にする | `link.curve = go.Curve.Bezier` |

### 表示制御

| やりたいこと | API |
|---|---|
| 全体を画面に収める | `diagram.zoomToFit()` |
| ズーム倍率を変える | `diagram.scale = 1.5` |
| スクロールする | `diagram.scrollToRect(rect)` |
| ノードの表示/非表示 | `node.visible = false` |
| サブツリーを折りたたむ | `cmd.collapseTree(node)` |
| サブツリーを展開する | `cmd.expandTree(node)` |

### データ保存・読込

| やりたいこと | API |
|---|---|
| JSON にシリアライズする | `model.toJson()` |
| JSON から復元する | `go.Model.fromJson(jsonString)` |
| SVG を生成する | `diagram.makeSvg(options)` |
| PNG 画像を生成する | `diagram.makeImage(options)` |
| 画像データを取得する | `diagram.makeImageData(options)` |

### イベント

| やりたいこと | API |
|---|---|
| 選択変更を検知する | `addDiagramListener("ChangedSelection", fn)` |
| リンク作成を検知する | `addDiagramListener("LinkDrawn", fn)` |
| テキスト編集を検知する | `addDiagramListener("TextEdited", fn)` |
| モデル変更を検知する | `model.addChangedListener(fn)` |
| ノードクリックを処理する | `node.click = fn` |
| マウスホバーを処理する | `node.mouseEnter / mouseLeave = fn` |
| 削除前に確認する | `addDiagramListener("SelectionDeleting", fn)` |

---

## 📖 関連ドキュメント

- [01_基本情報.md](./01_基本情報.md) — GoJS の概要
- [04_カスタマイズ方法.md](./04_カスタマイズ方法.md) — ノード・リンクのスタイリング
- [05_イベントハンドリング.md](./05_イベントハンドリング.md) — イベントの詳細
- [06_レイアウト一覧.md](./06_レイアウト一覧.md) — レイアウトアルゴリズム
- [公式 API ドキュメント](https://gojs.net/latest/api/index.html)
