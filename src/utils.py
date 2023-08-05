#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Yomogiβ, Blue S'
__version__ = '1.0.1'
__date__ = '2023/07/04 (Created: 2023/06/25 )'

import math


def convert_length_of_line_to_x_and_y(dx: int, dy: int, value: int) -> tuple[int, int]:
    """
    x軸とy軸に対して斜め直線の長さをx軸とy軸に対して並行な直線の長さに変更.

    Args:
        dx (int):
            x座標の差
        dy (int):
            y座標の差
        value (int):
            変換したい直線の長さ

    Returns:
        x (int):
            変換したい直線のx軸に対する長さ
        y (int):
            変換したい直線のy軸に対する長さ
    """
    if dx == 0:
        return dx, dy
    # スパーギアの中心とピニオンギアの中心を結ぶ直線(y = ax + b)の係数aを求める
    coefficient_a = (dy) / (dx)
    # ピニオンギアがスーパーギアの周りを回転した角度を求める
    radian_piniongear = math.atan(coefficient_a)
    # ピニオンギアの中心のx座標とy座標の増加量を求める
    # ピニオンギアの中心がスーパーギアの中心より右側にある時
    if dx >= 0:
        x = math.cos(radian_piniongear) * value
        y = math.sin(radian_piniongear) * value

    # ピニオンギアの中心がスーパーギアの中心より左側にある時
    elif dx < 0:
        x = - (math.cos(-radian_piniongear) * value)
        y = math.sin(-radian_piniongear) * value

    return x, y


def calculate_angle(ax: float, ay: float, bx: float, by: float) -> float:
    """(ax,ay)から(bx,by)への角度を計算する

    Args:
        ax (float):
            始点のx座標
        ay (float):
            始点のy座標
        bx (float):
            終点のx座標
        by (float):
            終点のy座標

    Returns:
        float: (ax,ay)から(bx,by)への角度(degrees)
    """

    dx = bx - ax
    dy = by - ay
    angle_radians = math.atan2(dy, dx)
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees
