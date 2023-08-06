# Blender2ScriptMapper
hibitさんが開発されている[Script Mapper](https://github.com/hibit-at/Scriptmapper)に、別のカメラスクリプトのカメラパスを読み込めるscriptコマンドを追加した[改造版Script Mapper](https://github.com/rynan4818/Scriptmapper)用に、Blenderで作ったカメラパスをCameraPlus用のカメラスクリプトとして出力するBlender用のスクリプトです。

これを使ってScriptmapperで作れないような複雑なカメラワークをBlenderで作って利用できます。

元はBlenderからCamera2用のカメラスクリプトを作る[Blender2Camera2](https://github.com/KandyWrong/blender2camera2)をCameraPlusフォーマットに変更したものになります。

# インストール方法

1. [Blender](https://blender.org/)がインストールされていない人は、[ダウンロード](https://blender.org/download/)してインストールします。

    Blenderのインストール方法、基本的な使い方はWeb上に色々あります。

    [3Dモデリングソフト「Blender」の操作を0から学べる1,400ページの解説書が無償公開](https://forest.watch.impress.co.jp/docs/news/1302036.html)などが、学生の講義用に作られていてわかりやすいです。最新は[2021年度版](https://web.wakayama-u.ac.jp/~tokoi/cgpe2021.html)にあります。`第１回概要説明、Blenderの基本操作`だけ読めば、本ツールの作業には支障はありません。

    また、元ツールの[Blender2Camera2のマニュアルのUsing Blender](https://kandywrong.com/b2c2/using-blender.html#installing-blender)が英語ですが、本ツールの使い方に集約されており、動画もあるので大変参考になります。
2. [Releases](https://github.com/rynan4818/blender2ScriptMapper/releases)から最新のAssetsの`Source code (zip)` をダウンロードします。※専用のzipファイルは無いのでSource codeでOKです。
3. ダウンロードした`blender2ScriptMapper-****-**-**.zip`を適当なフォルダで解凍します。

# 使い方

1. 解凍したblender2ScriptMapperの`template`フォルダにある`template.blend`を作業用にコピー＆リネームして適当に保存します。

    元ツールのBlender2Camera2では、プレイ録画した譜面の動画の音声と静止画分割したファイルを、`template`フォルダにある`audio`と`video`フォルダに入れて、Blender上でタイミングを測りながら、カメラパスを作成していく様になっています。本ツールでは、１カットのカメラパスのみ作成して、タイミングの調整などはScriptmapperを使うため、このあたりの作業は飛ばしています。
    `template.blend`とカメラスクリプト出力用の`b2sm_export.py`のみあれば作業可能です。
    もちろん、最初から最後までBlender上で作ることも可能で、その場合はBlender2Camera2のマニュアル通りに作成してください。Blender2ScriptMapperはBlender2Camera2の出力フォーマットをCameraPlus用に変更しただけなので、それ以外はBlender2Camera2と同様に使えます。

2. リネームした`template.blend`をBlenderで開きます。※.blendファイルをダブルクリック

    ここから先は、[Blender2Camera2のUsing the Template File](https://kandywrong.com/b2c2/tutorial.html#using-the-template-file)の手順と同じです。

3. `オブジェクトモード`で`Modeling`タブにします。右側の`シーンコレクション`の`Paths`グループの`Path1`は不要なので表示を消します
4. 画面の表示を見やすい様に上から表示(表示ツリーのZ軸をクリック)して、`シーンコレクション`の`Paths`グループを選択した状態で、メニューの`追加`から`パス`を追加します。
5. 追加された`NURBSパス`を選択した状態で、'G' + 'Y' キーでマウスで前方に移動して、'R' + '90' + Enterで90度回転します。
6. 横方向からの視点にするため、表示ツリーの'X'をクリックします。'G' + 'Z' で目線より上に上げて、'G' + 'Y' で少し後方(左)に移動、'R'で少し上方から目線まで斜めにします。
7. パスの`編集モード` (`NURBSパス`を選択した状態で、'TAB'キー)にします。
8. 端の編集点を選択して'E'キーを押すと編集点が追加できます。追加した編集点をCtrlを押しながら移動するとグリッドに乗って調整しやすいです。
9. 末端を選択して'E'で追加でどんどんパスを伸ばしていきます。黒い細い線が実際のカメラパスになります。
10. 編集点を選択して'G'キーで移動してパスの形状を調整します。
11. 横からも見直してパスの編集点を調整します。
12. `Modeling`タブで`オブジェクトモード`に戻して、`Render`の`b2c2_main`カメラを選択して、下のオプションリストの`コンストレイント`で`Follow Path1`の`ターゲット`を`NURBSパス`に変更します。
13. `オフセット`を`-100～0`の範囲で、どこを始点にするか決めます。オフセット項目をマウスの左ドラッグで移動します。
14. カメラビューボタンで切り替えると、どの様に映るかわかります。
15. カメラパスからTargetに向かって、カメラの角度が自動調整されます。Targetを選択して'G'キーで移動してアバターの顔の前あたりに調整します。
16. FOVの変更はデータのレンズのレンズ単位を視野角に変更すると、視野角で設定できます。
17. カメラを始点位置にオフセットしたら、`Layout`タブに移動して、下にもともとある不要なキーフレームを選択して、右クリックから削除します。
18. 終了フレームに値を変更します。終了フレームは、5秒間のパスなら60FPS☓5秒=300以上にします。実際にはScriptMapperで分割時間が自動調整されるので、多い分には問題ありません。短すぎると、長い時間で動かす時に動きがぎこちなくなります。終了フレームに変更したら、終了のオフセット位置に変更すると、終了のキーフレームが追加されます。
19. 再生ボタンでパスの動きを確認します。
20. `Animation`タブにして、`b2c2_main`カメラを選択すると、オフセットの変化グラフが表示されます。表示はマウスのスクロールで大きくなるので、見やすく拡大します。バーを回転移動させると、イージングをかけることができます。
21. `Scripting`タブを開いて、`開く`から`b2sm_export.py`を選択して開きます。Scriptingタブが見つからない場合は、タブの上をマウスの中ボタン（スクロールクリック）して左右に移動します。
22. 再生ボタンを押してスクリプトを実行します。出力するカメラスクリプトの保存先、ファイル名を決めてエクスポートします。エクスポートされるファイル名は、設定したファイル名+カメラ名(デフォルトならb2c2_main)になります。複数のb2c2_で始まる名前のカメラがBlender上にある場合、それぞれ別のスクリプトで出力されます。※Fix camera FOV for Blender rendersのオプションはScriptMapperで使う場合はOFFで構いません。
23. 出力したスクリプトをScriptMapperで使うには、scriptコマンドが追加された[改造版Script Mapper](https://github.com/rynan4818/Scriptmapper)を使いますので、対応していない場合は差し替えます。※hibitさん配布の正式版が対応したら、そちらを使ってください。
24. 譜面フォルダに`script`フォルダを作成して、その中にエクスポートしたスクリプトを置きます。
25. ScriptMapperのブックマークに`script,エクスポートしたファイル名(.jsonなし)`のコマンドで設定します。例: `test_b2c2_main.json`なら`script,test_b2c2_main`
26. 作成したカメラパスで動作することを確認します。移動時間はScriptMapperで設定した間隔に自動調整されます。
