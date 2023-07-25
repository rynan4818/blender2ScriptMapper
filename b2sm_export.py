#  ____ ____   ____ ____          _   _____
# | __ )___ \ / ___|___ \  __   _/ | |___ /
# |  _ \ __) | |     __) | \ \ / / |   |_ \
# | |_) / __/| |___ / __/   \ V /| |_ ___) |
# |____/_____|\____|_____|   \_/ |_(_)____/
#
# Blender2Camera2 v1.3
# A Blender to Camera2 / Beat Saber Export Script
#
# Written by KandyWrong
#
# This script was released under the MIT license. See LICENSE.md for details.

import bpy
import copy
import hashlib
import json
import logging
import math
import mathutils
import os
import random
import time

from datetime import datetime

# ExportHelperはヘルパークラスで、ファイル名とファイルセレクタを呼び出すinvoke()関数を定義します。
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty
from bpy.types import Operator

'''
設定
'''

# スクリプトは、名前にこの接頭辞を含むカメラを検索します。
# スクリプトを通常使用する場合は、これを変更する必要はありません。
CONFIG_CAMERA_PREFIX = 'b2c2_'

# クロマキーエフェクト（グリーンスクリーン）による後処理が必要なプロジェクトに取り組んでいて、
# かつBeat Saberのビデオで使用するためにBlenderから何かをレンダリングしている場合、
# このオプションを有効にすると、Blenderのカメラセンサーの値が自動的に設定され、
# BlenderのレンダリングがBeat Saberのキャプチャと正確に一致するようになります。

# ポストプロセスで特殊効果を行わない場合、またはこれが何なのかよくわからない場合は、
# このオプションを無効のままにしておいてください。

# もちろん、これが何なのか、なぜ必要なのかを知っているのであれば、
# B2C2を使わずに自分でBlenderのカメラオプションを変更するのに必要な知識を持っているでしょう。
CONFIG_CAMERA_SENSOR_FIX_FOV_FOR_BLENDER_RENDERS = False

CONFIG_CAMERA_SENSOR_FIT    = 'VERTICAL'
CONFIG_CAMERA_SENSOR_HEIGHT = 24.0
CONFIG_CAMERA_SENSOR_WIDTH  = 42.666666

# Blender のシステムコンソール出力をディスク上のファイルにログ出力したい場合に true を設定します。
# ログファイルはblendファイルと同じフォルダに書き込まれます。これはデバッグにのみ有効です。
CONFIG_ENABLE_LOGGING_TO_DISK = True

# このスクリプトは、座標系変換時に行列変換を保存するための一時オブジェクトを使用します。
# このオブジェクトはスクリプトの実行開始時に作成され、スクリプトが終了すると（もちろんクラッシュしなければ）削除されます。
CONFIG_EXPORT_OBJECT_PREFIX = 'b2c2_export_object_'

'''
ログ関係
'''

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

'''
> BlenderからUnity/Beat Saberへの翻訳

要約:
    # BlenderのX軸で90度引いて、次に
    (px, pz, py) = mw_unity.to_translation()
    (rx, rz, ry) = mw_unity.to_euler('YXZ')
    (rx, rz, ry) = (-rx, -rz, -ry)
    #  ...そして、Unity互換の座標と回転が得られます。

仕組み:
- BlenderはZ-up、右手座標系を使用します。
- Blenderの正回転は反時計回り

- UnityはY-up、左手座標系を使用します。
- Unityの正回転は時計回り

このスクリプトを読んでいる人で、Blender座標をUnity座標に変換した方法を知りたい人のために:
    重要なのは、Blenderからエクスポートするときに正しいオイラー回転順序を設定することです。

UnityエンジンはZXYのオイラー次数を想定しています。参照してください:

    https://docs.unity3d.com/ScriptReference/Transform-eulerAngles.html

Camera2 の用語では、Unity はカメラの回転を次の順序で設定します：
* 回転 Z = カメラのロール角度。「樽の下」を見て、カメラのレンズがあなたに背を向けている場合、
  45度の正のZ回転（ロール）は、カメラを左（反時計回り）にロールさせます。

* 回転 X = カメラのピッチ角。カメラの上部が "上 "で、カメラのレンズが左を向いているようなカメラを見た場合、
  正のX回転（ピッチ）45度はカメラを下向き（反時計回り）にします。

* rot Y = カメラのヨー角。 Beat Saber プラットフォームを上から下に見て、
  高速道路が上 / 北 / 前方の位置にあることを想像してください。
  正の Y 回転 (ヨー) が 45 度の場合、カメラは右 (時計回り) を指します。

BlenderからUnityに最小限のドラマでエクスポートするには、Blenderから3つのオイラー角を正しい順序で
取得する必要があります。しかし、X/Y/Zで考えてはいけません。代わりに、roll / pitch / yawで考えてください。

その前に考えなければならないことがあります。

> BlenderとUnityにおけるカメラの向き

BlenderのカメラとUnityのカメラはピッチ角の解釈が異なります。

Blenderではピッチアングルが0度だとカメラは真下を向きます。

Unityでは、ピッチアングルが0度だとカメラはまっすぐ前方、地平線の方を向きます。(Blenderでの真正面はピッチ+90度です)。

したがって、BlenderからUnityにトランスレートして同じピッチの向きにするには、B2C2エクスポートスクリプトで90度減算する必要があります。

> まとめ

このコードを見ると:
    (rx, rz, ry) = mw_unity.to_euler('YXZ')

UnityエンジンはZXYを想定しているため、オイラーオーダーは "YXZ"となります。
従って、to_euler() はBlenderのZ軸が実際にはYであるかのように呼び出されなければなりません。

同じロジックが出力タプルにも当てはまります。ZとYが入れ替わります。

最後に、BlenderとUnityの反時計回りと時計回りの符号の違いを考慮するために、タプル内の生の回転角度に-1を掛けなければなりません。

私の脳内ではこのようにロジックが動いていて、キャプチャしたビデオを比較しながら何度もテストした結果、
スクリプトの出力はUnity / Beat Saberで正確に動作しているようです。もし他にもっと良い説明方法があれば、githubにissueを残してください。
'''

'''
クラス
'''

class B2C2Export(Operator, ExportHelper):
    """Export camera path data to Beat Saber Camera2 format"""
    bl_idname = "b2c2_export.export"
    bl_label = "Export"

    # ExportHelper mixinクラスは、このメソッドを使用します。
    filename_ext = ".json"

    filter_glob: StringProperty(
        default="*.json",
        options={'HIDDEN'},
        maxlen=255,  # 内部バッファーの最大長、それ以上はクランプされます。
    )

    # 演算子のプロパティのリスト。属性は、呼び出す前に演算子の設定からクラスのインスタンスに割り当てられます。
    setting_fixFovForBlenderRender: BoolProperty(
        name="Fix camera FOV for Blender renders",
        description="ポストプロセスでクロマキー合成（グリーン・スクリーン）を使用するプロジェクトでは、"   \
            "このオプションをチェックしてカメラのFOVを固定し、BlenderレンダリングのFOVがBeat SaberのFOVと一致するようにします。",
        default=False,
    )

    setting_loop: BoolProperty(
        name="Loop Script",
        description="チェックすると、曲がスクリプトより長い場合、移動スクリプトはループします。"  \
            "そうでない場合、移動スクリプトは一度だけ再生され、最後のキーフレームで停止します。",
        default=True,
    )

    setting_syncToSong: BoolProperty(
        name="Sync to Song",
        description="チェックを入れると、曲の一時停止時に移動スクリプトが一時停止します。",
        default=True,
    )

    def execute(self, context):

        # ファイルログハンドラの追加
        if (True == CONFIG_ENABLE_LOGGING_TO_DISK):
            logger_start_disk()

        # 移動スクリプトのエクスポート
        export_main(
                context,
                self.filepath,
                self.setting_fixFovForBlenderRender,
                self.setting_loop,
                self.setting_syncToSong)

        # ログハンドラのクリーンアップ
        handlers = logger.handlers[:]
        for handler in handlers:
            logger.removeHandler(handler)
            handler.close()

        return {'FINISHED'}


'''
メニュー 一覧
'''

# ダイナミック・メニューに追加する場合のみ必要です。
def menu_func_export(self, context):
    self.layout.operator(B2C2Export.bl_idname, text="Beat Saber Camera2 Movement Script (.json)")


# 登録し、「ファイルセレクタ」メニューに追加します（F3検索「テキストエクスポートオペレータ」でクイックアクセスするために必要です）。
def register():
    bpy.utils.register_class(B2C2Export)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(B2C2Export)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


'''
エクスポート機能
'''

def export_main(
        context,
        filepath,
        setting_fixFovForBlenderRender,
        setting_loop,
        setting_syncToSong):

    # スクリプトの実行時間の追跡
    now_head = datetime.now()
    logger.debug('Export started at ' + str(now_head))

    '''
    選択されたオブジェクトのリストを保存します。

    スクリプトが実行され、すべての選択が解除されると迷惑なので、B2C2 は（クラッシュしなければ）元の状態に戻してくれます。
    '''

    pre_selected_active_object = bpy.context.view_layer.objects.active.name

    pre_selected_objects = []
    for obj in bpy.context.selected_objects:
        pre_selected_objects.append(obj.name)

    # --------------------------------------------------------------------------

    '''
    カメラの検索

    ブレンドファイルからロードされている全てのオブジェクトを繰り返します。
    どのオブジェクトがカメラであるかを把握し、名前に特別な接頭辞を持つカメラを選び出します。
    '''

    cameras = []

    for obj_name in bpy.data.objects.keys():
        if 'CAMERA' == bpy.data.objects[obj_name].type:
            camera_name = obj_name.lower()

            if camera_name.startswith(CONFIG_CAMERA_PREFIX):
                logger.debug('Found camera with name ' + obj_name)
                cameras.append(bpy.data.objects[obj_name])

    logger.debug('Found ' + str(len(cameras)) + ' camera(s) to export')

    # --------------------------------------------------------------------------

    '''
    一時エクスポートオブジェクトの作成

    B2C2が一時オブジェクトのランダムな名前を生成できるように、hashlibが関係しています。
    もし、エクスポートされたオブジェクトの名前が、すでにBlendファイル内にある名前と衝突する場合は、宝くじを買ってください。
    '''
    m = hashlib.sha1()
    m.update(str(random.getrandbits(128)).encode('utf-8'))
    export_obj_name = CONFIG_EXPORT_OBJECT_PREFIX + str(m.hexdigest()[:20])

    bpy.ops.object.empty_add()
    export_obj = bpy.context.active_object
    export_obj.name = export_obj_name

    # --------------------------------------------------------------------------

    '''
    位置、回転、FOVの収集

    シーンの各フレームについて、上記のブロックで見つかったすべてのカメラからデータを収集します。
    これらのフレームをすべて組み合わせると、カメラ・パスが作成されます。

    この "data" とは:
    - カメラ位置 (in Blender X,Y,Z)
    - カメラ角度 (in Blender X,Y,Z)
    - カメラFOV (in degrees)
    '''

    scene = context.scene
    paths = {}

    layer = bpy.context.view_layer

    # シーン内の各（b2c2）カメラをループします。
    for camera in cameras:

        logger.debug('Retrieving data for camera    : ' + str(camera.name))

        # カメラセンサーの値を修正し、BlenderレンダリングのFOVがBeat SaberのFOVと一致するようにしました。
        # (クロマキーエフェクトの後処理にのみ必要)
        if CONFIG_CAMERA_SENSOR_FIX_FOV_FOR_BLENDER_RENDERS or setting_fixFovForBlenderRender:
            camera.data.sensor_fit      = CONFIG_CAMERA_SENSOR_FIT
            camera.data.sensor_width    = CONFIG_CAMERA_SENSOR_WIDTH
            camera.data.sensor_height   = CONFIG_CAMERA_SENSOR_HEIGHT

        # シーン内の各フレームについて...
        for frame in range(scene.frame_start, scene.frame_end + 1):

            # シーンをこのフレームに設定します。
            scene.frame_set(frame)
            layer.update()

            # 現在のカメラのワールド位置行列を取得します。
            mw_blender = camera.matrix_world

            # 以下のコメントを参照してください。
            # (BlenderとUnityにおけるカメラの向き)
            export_obj.matrix_world = mw_blender
            scene.frame_set(frame)
            layer.update()

            export_obj.rotation_euler[0] += math.radians(-90)
            scene.frame_set(frame)
            layer.update()

            mw_unity = copy.deepcopy(export_obj.matrix_world)

            '''
            視野（FOV）に関する注意事項

            Camera2移動スクリプトに記述されたFOV値は、ゲーム内の垂直FOVとして解釈されます。
            B2C2はこれを制御できません。これはBeat Saber / Unityゲームエンジンがどのように動作するかということです。

            Blenderの場合：FOVがどのように適用されるかは、最終的なレンダリング画像のアスペクト比に依存します。

                * 横長の画像の場合、FOVは横（幅）に適用されます。
                * ポートレート画像の場合、FOVは垂直（高さ）に適用されます。

            UnityのFOVの扱い方:
            https://docs.unity3d.com/ScriptReference/Camera-fieldOfView.html

            BlenderのFOVの扱い方:
            https://blender.stackexchange.com/questions/23431/how-to-set-camera-horizontal-and-vertical-fov
            https://docs.blender.org/api/current/bpy.types.Camera.html

            幸いなことに、Blenderは自動的にカメラデータオブジェクトで垂直方向のFOV値を提供するので、このような混乱を心配する必要はありません。
            '''

            # Grab (vertical) field-of-view angle
            fov = math.degrees(camera.data.angle_y)

            '''
            最終カメラ出力
            '''

            # Unityカメラの位置を分解します。to_euler() については、
            # "BlenderとUnityにおけるカメラの向き" の注記を参照してください。
            (px, pz, py) = mw_unity.to_translation()
            (rx, rz, ry) = mw_unity.to_euler('YXZ')

            # Unityカメラのデータを一時的な辞書にまとめます。
            dict_unity = {}
            dict_unity['frame'] = frame
            dict_unity['pos'] = (px, py, pz)
            dict_unity['rot'] = (-rx, -ry, -rz)
            dict_unity['fov'] = fov

            # パス辞書内のカメラのリストにデータを追加します。
            if camera.name not in paths:
                paths[camera.name] = []

            paths[camera.name].append(dict_unity)

    # 一時エクスポート・オブジェクトをクリーンアップします。
    export_obj.select_set(True)
    bpy.ops.object.delete()

    # --------------------------------------------------------------------------

    '''
    以前に選択したすべてのオブジェクトを再選択
    '''

    # すべての選択オブジェクトの選択を解除
    for obj in bpy.context.selected_objects:
        obj.select_set(False)

    # 元の選択に戻す
    for obj_name in pre_selected_objects:
        bpy.data.objects[obj_name].select_set(True)

    bpy.context.view_layer.objects.active = bpy.data.objects[pre_selected_active_object]

    # --------------------------------------------------------------------------

    '''
    エクスポート可能な形式に変換

    Camera2の動作スクリプトはJSON形式で保存されます。個々のカメラのキーフレームは、
    "frames "というタイトルの1つのリストに格納されます。
    各フレームは、"位置"、"FOV"、"回転"、およびいくつかのオプションフィールドを含む辞書です。

    上で作成したパスの辞書は、次のステップでJSONファイルへのエクスポートが簡単になるように、
    新しいリスト/辞書ベースの構造に変換する必要があります。
    '''

    movement = {}

    # フレーム時間（秒）を計算
    duration = 1 / scene.render.fps

    for camera_name in paths:

        # パス辞書内にカメラのフレームリストを作成します。
        if camera_name not in movement:
            movement[camera_name] = {}

        # オプションのグローバル設定を保存
        #movement[camera_name]['syncToSong'] = setting_syncToSong
        #movement[camera_name]['loop']       = setting_loop
        movement[camera_name]['ActiveInPauseMenu']          = True
        movement[camera_name]['TurnToHeadUseCameraSetting'] = False

        # 収納フレーム
        movement[camera_name]['Movements'] = []

        for i,frame in enumerate(paths[camera_name]):
            if i == 0:
                continue
            temp = {}

            # デバッグに役立つように、フレームインデックスを書き込みます。
            # Camera2はこのフィールドを無視します。
            temp['frame_index'] = i

            pre_frame = paths[camera_name][i - 1]
            temp['StartPos'] = {}
            temp['StartPos']['x'] = round(pre_frame['pos'][0], 3)
            temp['StartPos']['y'] = round(pre_frame['pos'][1], 3)
            temp['StartPos']['z'] = round(pre_frame['pos'][2], 3)
            temp['StartPos']['FOV'] = round(pre_frame['fov'], 3)

            temp['StartRot'] = {}
            temp['StartRot']['x'] = round(math.degrees(pre_frame['rot'][0]), 3)
            temp['StartRot']['y'] = round(math.degrees(pre_frame['rot'][1]), 3)
            temp['StartRot']['z'] = round(math.degrees(pre_frame['rot'][2]), 3)

            temp['EndPos'] = {}
            temp['EndPos']['x'] = round(frame['pos'][0], 3)
            temp['EndPos']['y'] = round(frame['pos'][1], 3)
            temp['EndPos']['z'] = round(frame['pos'][2], 3)
            temp['EndPos']['FOV'] = round(frame['fov'], 3)

            temp['EndRot'] = {}
            temp['EndRot']['x'] = round(math.degrees(frame['rot'][0]), 3)
            temp['EndRot']['y'] = round(math.degrees(frame['rot'][1]), 3)
            temp['EndRot']['z'] = round(math.degrees(frame['rot'][2]), 3)

            temp['TurnToHead'] = False
            temp['TurnToHeadHorizontal'] = False
            temp['Duration'] = duration
            temp['Delay'] = 0
            temp['EaseTransition'] = False

            movement[camera_name]['Movements'].append(temp)

    # --------------------------------------------------------------------------

    '''
    ディスクへのファイルの書き込み

    各カメラスクリプトをディスクに書き込みます。エクスポートスクリプトは、
    ブレンドファイル内で見つけた各カメラに別々のムーブメントスクリプトを作成します。
    '''

    path_base_noext = os.path.splitext(filepath)

    for camera_name in movement:
        path_target = path_base_noext[0] + '_' + camera_name + '.json'

        # 書き込み用にファイルを開く
        with open(path_target, 'w') as fh:
            fh.write(json.dumps(movement[camera_name], indent=4, sort_keys=True))

    # スクリプトの実行時間の追跡
    now_tail = datetime.now()

    logger.debug('Export finished at ' + str(now_tail))
    logger.debug('Export took ' + str(now_tail - now_head))

    return {'FINISHED'}


def logger_start_disk():

    '''
    ローカルディスクロガーを設定します。
    '''
    try:

        # フォーマッタの作成
        formatter = logging.Formatter(
            fmt='[%(process)d] %(levelname)s: %(module)s.%(funcName)s(): %(message)s')

        # ログディレクトリが存在しない場合は、作成します。
        log_path = os.path.join(os.path.dirname(bpy.data.filepath), 'logs')
        if not os.path.exists(log_path):
            os.mkdir(log_path)

        # ビルドファイルパス
        fh_path = os.path.basename(bpy.data.filepath)
        fh_path += '-' + time.strftime("%Y%m%d-%H%M%S") + '.log'
        fh_path = os.path.join(log_path, fh_path)

        # ロガーにファイルを指定します。
        fh = logging.FileHandler(fh_path)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return True

    except:
        raise
        return False


if __name__ == "__main__":
    register()

    bpy.ops.b2c2_export.export('INVOKE_DEFAULT')
