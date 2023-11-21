# SpiroDesign
このプログラムはプロジェクト演習にて作成したスピロデザインの描画ツールです。

私たちが行ったプロジェクト演習とは、教員より開発を行うプログラムの要求仕様書を提示され、それをもとに基本設計～テストまでを教員の助けなくチームメンバーのみで行う授業です。

Pythonをベースとして書かれています。描画ライブラリは「pygame」及び「tkinter」のハイブリットです。

また、TranscryptにてJavascriptへ変換できるように設られている他、変換したJavascriptを読み込んで動作させるための、最低限のHTML,CSS,Javascriptプログラム群も内包されています。
(srcに同梱されているpyjsdlはhttps://github.com/jggatc/pyjsdl-ts の一部改良版です)

# メンバー
プロジェクト演習のメンバーは5名で行いました。各ファイルのコードには
基本的にauthor属性が記載されていますが、記述されている名前はGithubに上げる前に全て匿名化しています。

# マニュアル
## 利用方法
ビルド版の動作環境はMac,windowsです。  
web版はChrome版を推奨環境としています。

buildもしくは[web版](https://www.cc.kyoto-su.ac.jp/~g2154352/SpiroDesignWeb/web_page/)にアクセスして、利用できます。

<img width="499" alt="スクリーンショット 2023-11-21 17 54 03" src="https://github.com/YomogiBeta/SpiroDesign_by_Copilot/assets/46161490/03d99fb6-e85d-4dd6-b929-cb5a5819cd41">

### 基本操作
赤い円がスパーギア、小さい円がピニオンギア、青円の中に黒の点が入っているものがペンです。
スパーギア、ピニオンギアは円周上の4つの点をドラッグ&ドロップすることで大きさを変更できます。
また、円の中点をドラッグ&ドロップで位置を移動できます。
ペンもドラッグ&ドロップで位置を移動できます。
また、白の背景(画用紙)もドラッグ&ドロップで移動させることができます

### コンテキストメニュー
右クリック(スマホの場合は2本指でタップ)でコンテキストメニューを表示させることができます。

<img width="154" alt="スクリーンショット 2023-11-21 17 58 52" src="https://github.com/YomogiBeta/SpiroDesign_by_Copilot/assets/46161490/3dd223d2-6ec6-4d04-b8cd-d16178115b96">

|項目| 説明|
|:----|:----|
|start| スピロ定規での描画のシュミレーションを開始します。|
|stop| スピロ定規での描画のシュミレーションを終了します。|
|current_clear| 現在描画作業中の描画を全てクリアします。|
|clear| 現在描画中であるかどうかに関わらず、スパーギア(赤円)の範囲にある描画を全てクリアします。|
|speed_up|  シュミレーション速度をあげます。|
|speed_down|  シュミレーション速度を下げます。|
|color| ペンの色を変更するダイアログを開きます。|
|rainbow| ペンの色を虹色に遷移させるモードをONにします。ペン色を変更するとOFFになります。|
|nib| ペンの太さを変更するダイアログを開きます。|
|circumscribe| 外接円モードでのシュミレーションに変更します。|
|inscribe| 内接円モードでにシュミレーションに変更します(デフォルト)|
|dive| 現在の描画内容を確定させます。|
|new| 盤面の状況を全てクリアし、新しく作業を開始します。|
|open| 描画結果の保存ファイルを開きます。ビルド版とweb版で互換性があります。|
|save| 描画結果をファイルに保存します。|

# 開発を開始する。
## 環境構築
### mac
- Required
  - tcl/tk 8.6.13
  - pyenv
  - python 3.10.11  

macの場合、破損していないtcl-tkをインストールし、それをpython 3.10.11と紐付ける必要があります。  
そのためpyenvにてpython 3.10.11をインストールしている場合、一度アンインストールする必要があります。  
```pyenv uninstall 3.10.11```  
  
tcl/tk 8.6.13 は次のコマンドでインストールできます。  
```make install-mac-tcl-tk```  

その後、以下のコマンドでPythonをセットアップします。  
```make setup-python-mac```

### Windows
- Required
  - Makefile
  - pyenv
  - python 3.10.11  

以下のコマンドでPythonをセットアップします。  
```make setup-python```

## 実行
### Python版の実行
``` make run ```

### web版の実行
```make web-build-dev```  
```make web-run```  

## web依存のコードの記述
web依存のコードを記述する場合、以下のコマンドを実行します。  
```make rady_javascript```  

通常のコードを記述する場合、以下のコマンドで元に戻します。  
```make rady_python```  

## 単体テスト
次のコマンドで単体テストを実行できます。  
```make test```

## コードのメトリクスの出力
次のコマンドでコードのメトリクスを出力できます。  
```make metrics```





