#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Yomogiβ'
__version__ = '1.0.4'
__date__ = '2023/07/09 (Created: 2023/05/15)'

FRAME_RATE = 60
"""int: 目標フレームレート"""
DISPLAY_WIDTH = 1280
"""int: ウィンドウの幅"""
DISPLAY_HEIGHT = 720
"""int: ウィンドウの高さ"""

BOARD_WIDTH = 3000
"""int: メインボードの幅"""
BOARD_HEIGHT = 3000
"""int: メインボードの高さ"""
INIT_BOARD_POSITION = (-1 * (BOARD_WIDTH / 2 - DISPLAY_WIDTH / 2), -1 * (BOARD_HEIGHT / 2 - DISPLAY_HEIGHT / 2))
"""tuple[int, int]: メインボードの初期位置"""

ACTIVE_SURFACE_PADDING = 20
"""int: アクティブサーフェスのパディング"""

FONT_NAME = "NotoSansJP"
"""str: フォントの名前"""
FONT_SIZE = 12
"""int: フォントのサイズ"""
FONT_WEIGHT = 400
"""int: フォントの太さ"""


INIT_SPUR_GEAR_RADIUS = 128
"""int: 初期のスーパーギアの半径"""
INIT_PINION_GEAR_RADIUS = 64
"""int: 初期のピニオンギアの半径"""
INIT_SPUR_GEAR_POSITION = (BOARD_WIDTH / 2, BOARD_HEIGHT / 2)
"""tuple[int, int]: 初期のスーパーギアの位置"""
INIT_PINION_GEAR_POSITION = (BOARD_WIDTH / 2 + INIT_PINION_GEAR_RADIUS, BOARD_HEIGHT / 2)
"""tuple[int, int]: 初期のピニオンギアの位置"""
INIT_PEN_TO_PINION_DISTANCE = 24.0
"""int: 初期のペンとピニオンの距離"""
INIT_PEN_NIB = 4
"""int: 初期のペンの先端の半径"""

BACKGROUND_COLOR = (255, 255, 255)
"""tuple[int, int, int]: 背景色"""

SPUR_GEAR_COLOR = (255, 0, 0)
"""tuple[int, int, int]: スーパーギアの色"""
PINION_GEAR_COLOR = (0, 0, 255)
"""tuple[int, int, int]: ピニオンギアの色"""
GEAR_LINE_COLOR = (0, 255, 0)
"""tuple[int, int, int]: 補助線の色"""

MAX_SPEED = 10
"""int: 最大速度"""
MIN_SPEED = 1
"""int: 最小速度"""
SPEED_STEP = 1
"""int: 初期の速度のステップ"""

SPILIT_POINT_NUM = 8
"""int: 軌跡点のシュミレート分割数"""

PICKING_CIRCLE_PADDING = 24
"""int: ギアのセレクタのパディング"""
PEN_HOLE = 3
"""int: ペンの穴の半径"""
CIRCLE_PICKING_RADIUS = 4
"""int: ギアの選択範囲の描画半径"""
MIN_PINION_GEAR_RADIUS = 14
"""int: ピニオンギアの最小半径"""
MIN_GEAR_RADIUS = 12
"""int: ギアの最小半径"""

FIILE_NAME_FORMAT = "spiro_data_%Y%m%d%H%M%S.json"

CONTEXT_MENU_BACKGROUND_COLOR = (252, 252, 255)
"""tuple[int, int, int]: コンテキストメニューの背景色"""
CONTEXT_MENU_ON_BACKGROUND_COLOR = (26, 28, 30)
"""tuple[int, int, int]: コンテキストメニューの上の要素の色"""
CONTEXT_MENU_ON_DISABLE_BACKGROUND_COLOR = (200, 200, 200)
"""tuple[int, int, int]: コンテキストメニューの上の要素の色(無効時)"""
CONTEXT_MENU_HOVERD_BACKGROUND_COLOR = (241, 243, 245)
"""tuple[int, int, int]: コンテキストメニューがホバーされた時の要素の色"""
CONTEXT_MENU_DIVIDER_COLOR = (200, 200, 200)
"""tuple[int, int, int]: コンテキストメニューの区切り線の色"""

LONG_PRESS_START_MILLISEC = 500
"""int: ロングプレス判定の開始時間"""
LONG_PRESS_INTERVAL_MILLISEC = 100
"""int: ロングプレス判定の間隔"""
