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

3. `オブジェクトモード`で`Modeling`タブにします。右側の`シーンコレクション`の`Paths`グループの`Path1`は不要なので表示を消します。

![image](https://github.com/rynan4818/blender2ScriptMapper/assets/14249877/f3974e1e-a6ec-4899-badc-01d5c47ae21f)

4. 画面の表示を見やすい様に上から表示(表示ツリーのZ軸をクリック)して、`シーンコレクション`の`Paths`グループを選択した状態で、メニューの`追加`から`パス`を追加します。

![image](https://github.com/rynan4818/blender2ScriptMapper/assets/14249877/dac35311-d76f-4882-9f50-271533d0cae7)

5. 追加された`NURBSパス`を選択した状態で、'G' + 'Y' キーでマウスで前方に移動して、'R' + '90' + Enterで90度回転します。

![image](https://github.com/rynan4818/blender2ScriptMapper/assets/14249877/2af442a9-27af-4791-ba3d-65f24624763d)

6. 横方向からの視点にするため、表示ツリーの'X'をクリックします。'G' + 'Z' で目線より上に上げて、'G' + 'Y' で少し後方(左)に移動、'R'で少し上方から目線まで斜めにします。

![image](https://github.com/rynan4818/blender2ScriptMapper/assets/14249877/7c6a307f-79f8-402d-adef-bf1fb359a77a)

7. パスの`編集モード` (`NURBSパス`を選択した状態で、'TAB'キー)にします。

![image](https://github.com/rynan4818/blender2ScriptMapper/assets/14249877/2e8631f6-8146-41c0-9389-60cb3b1d940f)

8. 端の編集点を選択して'E'キーを押すと編集点が追加できます。追加した編集点をCtrlを押しながら移動するとグリッドに乗って調整しやすいです。

![image](https://github.com/rynan4818/blender2ScriptMapper/assets/14249877/5c92b868-c2fc-49bf-8448-24a509410950)

9. 末端を選択して'E'で追加でどんどんパスを伸ばしていきます。黒い細い線が実際のカメラパスになります。

![image](https://github.com/rynan4818/blender2ScriptMapper/assets/14249877/2b33d1ab-cb3c-4f1a-9c30-9e67400b6ff5)

10. 編集点を選択して'G'キーで移動してパスの形状を調整します。

![image](https://github.com/rynan4818/blender2ScriptMapper/assets/14249877/832ebdf1-d4f6-45fa-ad88-be75c47bc5a5)

11. 横からも見直してパスの編集点を調整します。

![image](https://github.com/rynan4818/blender2ScriptMapper/assets/14249877/15f585c8-ba6e-4df9-8b1a-64c837123a31)

12. `Modeling`タブで`オブジェクトモード`に戻して、`Render`の`b2c2_main`カメラを選択して、下のオプションリストの`コンストレイント`で`Follow Path1`の`ターゲット`を`NURBSパス`に変更します。

![image](https://github.com/rynan4818/blender2ScriptMapper/assets/14249877/83fda69f-1876-4ef5-8356-598c17334ae7)

13. `オフセット`を`-100～0`の範囲で、どこを始点にするか決めます。オフセット項目をマウスの左ドラッグで移動します。

![image](https://github.com/rynan4818/blender2ScriptMapper/assets/14249877/94e2d245-7a82-4f86-a3fd-a4394bf421a6)

14. カメラビューボタンで切り替えると、どの様に映るかわかります。

![image](https://github.com/rynan4818/blender2ScriptMapper/assets/14249877/c46af0d3-10b9-4bac-a354-fe34b35d6549)

15. カメラパスからTargetに向かって、カメラの角度が自動調整されます。Targetを選択して'G'キーで移動してアバターの顔の前あたりに調整します。

![image](https://github.com/rynan4818/blender2ScriptMapper/assets/14249877/2338318f-11a9-4966-b53a-5a3b6fedd0dc)
![image](https://github.com/rynan4818/blender2ScriptMapper/assets/14249877/5f392971-b655-41cb-ac2f-b289943e061a)

16. FOVの変更はデータのレンズのレンズ単位を視野角に変更すると、視野角で設定できます。

![image](https://github.com/rynan4818/blender2ScriptMapper/assets/14249877/78cc6596-e3d1-4e28-a947-25d4389ba933)

17. カメラを始点位置にオフセットしたら、`Layout`タブに移動して、下にもともとある不要なキーフレームを選択して、右クリックから削除します。

![image](https://github.com/rynan4818/blender2ScriptMapper/assets/14249877/4bd33d89-66d5-4868-aee8-52f4666b1a88)
![image](https://github.com/rynan4818/blender2ScriptMapper/assets/14249877/2e2a7dc4-3db9-4a30-8900-94bed7da6f16)

18. 開始フレームを0に移動して、オフセットの右にあるアニメーションをチェックすると、現在のフレームにキーフレームが追加されます。

![image](https://github.com/rynan4818/blender2ScriptMapper/assets/14249877/777543e2-1362-4b3e-a15f-28ce15cac872)

19. 終了フレームに値を変更します。終了フレームは、5秒間のパスなら60FPS☓5秒=300以上にします。実際にはScriptMapperで分割時間が自動調整されるので、多い分には問題ありません。短すぎると、長い時間で動かす時に動きがぎこちなくなります。終了フレームに変更したら、終了のオフセット位置に変更すると、終了のキーフレームが追加されます。

![image](https://github.com/rynan4818/blender2ScriptMapper/assets/14249877/46f1d86d-592b-4412-b745-1931ce5f4b47)

20. 再生ボタンでパスの動きを確認します。

![image](https://github.com/rynan4818/blender2ScriptMapper/assets/14249877/778d5ba3-2878-4e2f-82c3-8422fba5e782)

21. `Animation`タブにして、`b2c2_main`カメラを選択すると、オフセットの変化グラフが表示されます。表示はマウスのスクロールで大きくなるので、見やすく拡大します。バーを回転移動させると、イージングをかけることができます。

![image](https://github.com/rynan4818/blender2ScriptMapper/assets/14249877/ff7b9ff2-fd8a-458c-b808-3d8a247e6fb6)

22. `Scripting`タブを開いて、`開く`から`b2sm_export.py`を選択して開きます。Scriptingタブが見つからない場合は、タブの上をマウスの中ボタン（スクロールクリック）して左右に移動します。

![image](https://github.com/rynan4818/blender2ScriptMapper/assets/14249877/8d9dc27a-1c11-449a-a137-353afde83728)

23. 再生ボタンを押してスクリプトを実行します。出力するカメラスクリプトの保存先、ファイル名を決めてエクスポートします。エクスポートされるファイル名は、設定したファイル名+カメラ名(デフォルトならb2c2_main)になります。複数のb2c2_で始まる名前のカメラがBlender上にある場合、それぞれ別のスクリプトで出力されます。※Fix camera FOV for Blender rendersのオプションはScriptMapperで使う場合はOFFで構いません。

![image](https://github.com/rynan4818/blender2ScriptMapper/assets/14249877/550a9f6e-bc33-456d-9b9f-c859b69260c1)

24. 出力したスクリプトをScriptMapperで使うには、scriptコマンドが追加された[改造版Script Mapper](https://github.com/rynan4818/Scriptmapper)を使いますので、対応していない場合は差し替えます。※hibitさん配布の正式版が対応したら、そちらを使ってください。
25. 譜面フォルダに`script`フォルダを作成して、その中にエクスポートしたスクリプトを置きます。

![image](https://github.com/rynan4818/blender2ScriptMapper/assets/14249877/30295048-0a63-4551-862b-471f4aa96432)

26. ScriptMapperのブックマークに`script,エクスポートしたファイル名(.jsonなし)`のコマンドで設定します。例: `test_b2c2_main.json`なら`script,test_b2c2_main`

![image](https://github.com/rynan4818/blender2ScriptMapper/assets/14249877/daeb4040-e7a0-4771-8c8a-a2f09db3555e)

27. 作成したカメラパスで動作することを確認します。移動時間はScriptMapperで設定した間隔に自動調整されます。

![image](https://github.com/rynan4818/blender2ScriptMapper/assets/14249877/97ed47fd-4887-49fb-a549-2d101d702e33)

# カメラパスの作り方の参考
[Blender2Camera2のAdvanced Techniques](https://kandywrong.com/b2c2/advanced.html)に高度な制御方法など解説がありますので、参考にしてください。

その他にもBlenderのカメラパスの作り方のサイトはいっぱいあるので参考にしてください。リアルなカメラ手ブレのプラグイン[Camera Shakify](https://www.google.com/search?q=Camera+Shakify)などもあります。

