#!/usr/bin/env python
# -*- coding: utf-8 -*-

# この記法は利用できない。
# import pyjsdl as pygame
# 上記の記法ではPygameBridgeは以下にトランスコンパイルされる
# import * as {pygame} from 'pyjsdl.js';
# しかし、インポート側は以下のようにトランスコンパイルされる
# import {pygame} from './PygameBridge.js';
# JSの考え方に乗っ取ると、PygameBridge.jsはpygameがexportされていなければならないが、実際にはPygameBridgeはそのようにトランスコンパイルされない。
# 下記の書き方であれば、export var pygame・・・ が追加され。インポート側のトランスコンパイルで正しく読み込める

# Javascript
# import pyjsdl
# import pyjsdl.pyjsarray as imported_pyjsarray

# Javascript
# pygame = pyjsdl
# pyjsarray = imported_pyjsarray

# Python
import pygame
import sys
import os
import numpy

__author__ = 'Yomogiβ'
__version__ = '1.1.0'
__date__ = '2023/07/05 (Created: 2023/04/20 )'


def clear_draw_rect(surface: pygame.Surface, rect: pygame.Rect) -> None:
    """引数のSurfaceから引数のRectの範囲の描画をクリアする

    Args:
        surface (pygame.Surface):
            描画をクリアするSurface.
        rect (pygame.Rect):
            描画をクリアする範囲のRect.
    """
    # Javascript
    # surface.py_clear(rect.x, rect.y, rect.width, rect.height)

    # Python
    surface.fill((255, 255, 255, 0), rect)


def clear_draw_surface(surface: pygame.Surface) -> None:
    """引数のSurfaceの描画をクリアする

    Args:
        surface (pygame.Surface):
            描画をクリアするSurface.
    """
    # Javascript
    # surface.py_clear()

    # Python
    surface.fill((255, 255, 255, 0))


def rect_update(rect: pygame.Rect, left: float, top: float, width: float, height: float) -> None:
    """引数のRectの座標とサイズを更新する

    Args:
        rect (pygame.Rect):
            更新するRect.
        left (float):
            Rectの左端の座標.
        top (float):
            Rectの上端の座標.
        width (float):
            Rectの幅.
        height (float):
            Rectの高さ.
    """

    # Javascript
    # rect.js_update(left, top, width, height)

    # Python
    rect.update(left, top, width, height)


def find_data_file(filename):
    """frozen状況に合わせて引数のファイル名のファイルパスを取得する

    https://cx-freeze.readthedocs.io/en/latest/faq.html#data-files

    Args:
        filename (str):
            ファイル名.

    Returns:
        str:
            引数のファイル名のファイルパス.
    """

    # Javascript
    # pass

    # Python
    if getattr(sys, "frozen", False):
        datadir = os.path.dirname(sys.executable)
    else:
        datadir = os.path.abspath(".")
    return os.path.join(datadir, filename)


def get_font(font_name: str, font_size: int, font_weight: int) -> pygame.font.Font:
    """引数のフォント名、フォントサイズ、フォントウェイトのフォントを取得する

    Args:
        font_name (str):
            フォント名.
        font_size (int):
            フォントサイズ.
        font_weight (int):
            フォントウェイト.

    Returns:
        pygame.font.Font:
            引数の条件に合うpygameのフォントインスタンス
    """

    # Javascript
    # return pygame.font.Font(f'{font_name}_{font_weight}', font_size)

    # Python
    font_path = find_data_file(f"resource/fonts/{font_name}_{font_weight}.ttf")
    return pygame.font.Font(font_path, font_size)


def set_icon(icon_path: str) -> None:
    """引数のpngファイルパスをアプリアイコンとして設定する

    Args:
        icon_path (str):
            pngファイルパス.
    """

    # Javascript
    # pass

    # Python
    pygame.display.set_icon(pygame.image.load(find_data_file(icon_path)))


def set_callback(func) -> None:
    """引数の関数をメインループコールバック関数として設定する

    Args:
        func (Callable):
            メインループコールバック関数として設定する関数.
    """
    # Javascript
    # pygame.set_callback(func)

    # Python
    while True:
        func()


def make_surface(array_str: str, width: int, height: int) -> pygame.Surface:
    """引数の16進数文字列からpygameのSurfaceを生成する

    Args:
        array_bytes (str):
            Surfaceの色情報を表す16進数文字列
        width (int):
            Surfaceの幅.
        height (int):
            Surfaceの高さ.

    Returns:
        pygame.Surface:
            引数の16進数文字列から生成したSurface.
    """
    # Python
    array_bytes = bytes.fromhex(array_str)
    a_array = numpy.frombuffer(array_bytes, dtype=numpy.uint8)
    a_base_surface = numpy.reshape(a_array, [width, height, 4])
    a_base_surface = a_base_surface[:, :, :3]
    return pygame.surfarray.make_surface(a_base_surface)

    # Javascript
    # a_buffer = buffer.Buffer.js_from(array_str, "hex")
    # a_array = nj.uint8(Array.js_from(a_buffer))
    # a_viewboard_array = a_array.reshape(width, height, 4)
    # a_viewboard_array = a_viewboard_array.transpose(1, 0)
    # a_viewboard_array = a_viewboard_array.flatten()
    # a_canvas_image = __new__(ImageData(Uint8ClampedArray.js_from(a_viewboard_array.selection.data), width, height))
    # a_base_surface = pyjsarray.ImageMatrix(a_canvas_image)
    # return pygame.surfarray.make_surface(a_base_surface)


def output_surface(target_surface: pygame.Surface) -> str:
    """引数のSurfaceの色情報を表す16進数文字列を生成する

    Args:
        target_surface (pygame.Surface):
            色情報を表す16進数文字列を生成するSurface.

    Returns:
        str:
            引数のSurfaceの色情報を16進数文字列
    """
    # Python
    a_base_surface_rgb = pygame.surfarray.array3d(target_surface)
    a_base_surface_alpha = pygame.surfarray.array_alpha(target_surface)
    a_base_surface = numpy.dstack((a_base_surface_rgb, a_base_surface_alpha))
    return a_base_surface.tobytes().hex()

    # Javascript
    # a_base_surface = pygame.surfarray.array3d(target_surface)
    # a_array = nj.uint8(a_base_surface.getArray())
    # a_array = a_array.reshape(target_surface.get_height(), target_surface.get_width(), 4)
    # a_array = a_array.transpose(1, 0)
    # a_array = a_array.flatten()
    # return buf2hex(a_array.selection.data.buffer)


def cross_hair_mouse_mode() -> None:
    """マウスカーソルを十字にする"""
    # Javascript
    # canvas = document.getElementById('__panel__')
    # canvas.style.cursor = 'crosshair'

    # Python
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)


def normal_mouse_mode() -> None:
    """マウスカーソルを通常にする"""
    # Javascript
    # canvas = document.getElementById('__panel__')
    # canvas.style.cursor = 'default'

    # Python
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
