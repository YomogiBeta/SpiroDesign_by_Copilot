#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Blue S, Yomogiβ'
__version__ = '3.0.0'
__date__ = '2023/07/08 (Created: 2023/5/19 )'

from Constants import INIT_PEN_NIB, INIT_PEN_TO_PINION_DISTANCE, MIN_PINION_GEAR_RADIUS, PEN_HOLE
from Model.SpiroGear import SpiroGear
from bridge_pyjs.PygameBridge import pygame, rect_update
import math
import utils


class PinionGear(SpiroGear):
    """
    ピニオンギアモデル

        ピニオンギアのモデルです。ピニオンギアはペンを実装しています
    """

    def __init__(self, x: int, y: int, radius: int) -> None:
        """
        各種値の初期化及び親クラスのコンストラクタの呼び出しを行います.

        Args:
            x (int):
                ギアの中心座標x
            y (int):
                ギアの中心座標y
            radius (int):
                ギアの半径
        """
        super().__init__(x, y, radius)
        self.a_pen_color = (0, 0, 0)
        self.a_pen_to_pinion_degrees = 0.0
        self.a_pen_to_pinion_distance = INIT_PEN_TO_PINION_DISTANCE
        self.a_pen = pygame.Rect(0, 0, INIT_PEN_NIB, INIT_PEN_NIB)
        self.set_center_position(*self.center())

    def set_center_position(self, x: float, y: float) -> None:
        super().set_center_position(x, y)
        rotate_radian = math.radians(self.a_pen_to_pinion_degrees)
        move_pen_x = self.a_pen_to_pinion_distance * math.cos(rotate_radian) + x
        move_pen_y = self.a_pen_to_pinion_distance * math.sin(rotate_radian) + y

        self.set_pen_pos(move_pen_x, move_pen_y, True)  # 反応的にペンの位置を設定

    def add_radius(self, value: int) -> bool:
        if self.radius() + value < MIN_PINION_GEAR_RADIUS:
            return False
        if super().add_radius(value):
            update_distance = self.a_pen_to_pinion_distance + value
            if update_distance >= 0:
                self.a_pen_to_pinion_distance = update_distance
            self.set_center_position(*self.center())
        return True

    def set_radius(self, value: int) -> bool:
        if value < MIN_PINION_GEAR_RADIUS:
            return False

        before_radius = self.radius()
        dradius = value - before_radius

        if super().set_radius(value):
            update_distance = self.a_pen_to_pinion_distance + dradius
            if update_distance >= 0:
                self.a_pen_to_pinion_distance = update_distance
            self.set_center_position(*self.center())
        return True

    def force_set_radius(self, value: int) -> None:
        """ピニオンギアの半径を強制的に指定"""
        before_radius = self.radius()
        dradius = value - before_radius

        self.a_radius = value
        self.a_pen_to_pinion_distance += dradius
        self.set_center_position(*self.center())

    def set_pen_pos(self, x: int, y: int, reactive=False) -> None:
        """
        ペンがピニオンギアからでない範囲でペンの位置を設定します。引数の座標がルールから逸脱している場合は設定は行われません。

        Args:
            x (int):
                ペンのx座標
            y (int):
                ペンのy座標
            reactive (bool | optional):
                反応的なペン座標の設定であるかどうか
        """
        center_x, center_y = self.center()
        nib = self.a_pen.width
        pen_radius = (nib / 2)
        radius = self.radius()
        distance = math.sqrt(((x + pen_radius) - center_x)**2 + ((y + pen_radius) - center_y)**2)

        if distance <= radius - pen_radius - PEN_HOLE or reactive:
            rect_update(self.a_pen, x, y, nib, nib)
            if not reactive:
                self.a_pen_to_pinion_degrees = utils.calculate_angle(center_x, center_y, x, y)
                self.a_pen_to_pinion_distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)

    def add_pen_pos(self, dx: float, dy: float, reactive=False) -> None:
        """
        ペンの座標を引数の値だけ移動させます。内部での座標の指定には同クラスのset_pen_posを利用します。

        Args:
            dx (int):
                xの移動量
            dy (int):
                yの移動量
            reactive (bool | optional):
                反応的なペン座標の設定であるかどうか
        """
        pen_x, pen_y = self.pen().topleft
        self.set_pen_pos(pen_x + dx, pen_y + dy, reactive)

    def set_pen_color(self, color: tuple[int, int, int]) -> None:
        """
        ペンの色を設定します。色情報のtupleではない場合、設定は行われません。

        Args:
            color (tuple[int, int, int]):
                ペンの色情報
        """
        for color_sample in color:
            if ((color_sample > 255) or (color_sample < 0)):
                return
        self.a_pen_color = color

    def set_pen_nib(self, nib: float) -> None:
        """
        ペンの太さを設定します。引数の値が2以下の場合、設定は行われません。

        Args:
            nib (int):
                ペンの太さ
        """
        if (nib >= 2):
            if nib > self.a_pen.width:
                diff_distance = nib - self.a_pen.width
                self.a_pen_to_pinion_distance -= diff_distance
            rect_update(self.a_pen, *self.a_pen.topleft, nib, nib)
            self.set_center_position(*self.center())

    def pen_to_pinion_degrees(self) -> float:
        """ ペンからピニオンへ線分を引いた時の角度を返します。

        Returns:
            float: ペンからピニオンへ線分を引いた時の角度
        """
        return self.a_pen_to_pinion_degrees

    def pen_to_pinion_distance(self) -> float:
        """ ペンからピニオンまでの距離を返します。

        Returns:
            float: ペンからピニオンまでの距離
        """
        return self.a_pen_to_pinion_distance

    def pen(self) -> pygame.Rect:
        """ ペンのReactインスタンスを返します。

        Returns:
            Rect: ペンのReactインスタンス
        """
        return self.a_pen

    def pen_color(self) -> tuple[int, int, int]:
        """ ペンの色を返します。

        Returns:
            tuple[int, int, int]: ペンの色情報
        """
        return self.a_pen_color
