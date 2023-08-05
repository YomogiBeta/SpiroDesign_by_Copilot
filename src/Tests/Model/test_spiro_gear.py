#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ARA T, Dragon'
__version__ = '1.0.0'
__date__ = '2023/07/14 (Created: 2023/06/02 )'


import math
import pygame
import unittest

from Model.SpiroGear import SpiroGear
from src.Constants import PICKING_CIRCLE_PADDING


class TestSpiroGear(unittest.TestCase):

    def setUp(self):
        """スピロギアに関わるテストの準備"""
        self.a_spiro_gear = SpiroGear(300, 200, 150)

    def test_init(self):
        "スピロギアのフィールドのテスト"
        self.assertEqual(self.a_spiro_gear.a_center, (300, 200))
        self.assertEqual(self.a_spiro_gear.a_radius, 150)
        center_x, center_y = self.a_spiro_gear.a_center
        self.assertEqual(self.a_spiro_gear.a_bottom_rect,
                         pygame.Rect(center_x - PICKING_CIRCLE_PADDING / 2,
                                     center_y + self.a_spiro_gear.a_radius - PICKING_CIRCLE_PADDING / 2,
                                     PICKING_CIRCLE_PADDING,
                                     PICKING_CIRCLE_PADDING))
        self.assertEqual(self.a_spiro_gear.a_left_rect,
                         pygame.Rect(center_x - self.a_spiro_gear.a_radius - PICKING_CIRCLE_PADDING / 2,
                                     center_y - PICKING_CIRCLE_PADDING / 2,
                                     PICKING_CIRCLE_PADDING,
                                     PICKING_CIRCLE_PADDING))
        self.assertEqual(self.a_spiro_gear.a_right_rect,
                         pygame.Rect(center_x + self.a_spiro_gear.a_radius - PICKING_CIRCLE_PADDING / 2,
                                     center_y - PICKING_CIRCLE_PADDING / 2,
                                     PICKING_CIRCLE_PADDING,
                                     PICKING_CIRCLE_PADDING))
        self.assertEqual(self.a_spiro_gear.a_top_rect,
                         pygame.Rect(center_x - PICKING_CIRCLE_PADDING / 2,
                                     center_y - self.a_spiro_gear.a_radius - PICKING_CIRCLE_PADDING / 2,
                                     PICKING_CIRCLE_PADDING,
                                     PICKING_CIRCLE_PADDING))
        self.assertEqual(self.a_spiro_gear.a_center_rect,
                         pygame.Rect(center_x - PICKING_CIRCLE_PADDING / 2,
                                     center_y - PICKING_CIRCLE_PADDING / 2,
                                     PICKING_CIRCLE_PADDING,
                                     PICKING_CIRCLE_PADDING))

    def test_updte_picking_rect(self):
        """スピロギアの更新をテスト"""
        self.a_spiro_gear.update_picking_rect()
        center_x, center_y = self.a_spiro_gear.center()
        self.assertEqual(self.a_spiro_gear.a_bottom_rect,
                         pygame.Rect(center_x - PICKING_CIRCLE_PADDING / 2,
                                     center_y + self.a_spiro_gear.a_radius - PICKING_CIRCLE_PADDING / 2,
                                     PICKING_CIRCLE_PADDING,
                                     PICKING_CIRCLE_PADDING))
        self.assertEqual(self.a_spiro_gear.a_left_rect,
                         pygame.Rect(center_x - self.a_spiro_gear.a_radius - PICKING_CIRCLE_PADDING / 2,
                                     center_y - PICKING_CIRCLE_PADDING / 2,
                                     PICKING_CIRCLE_PADDING,
                                     PICKING_CIRCLE_PADDING))
        self.assertEqual(self.a_spiro_gear.a_right_rect,
                         pygame.Rect(center_x + self.a_spiro_gear.a_radius - PICKING_CIRCLE_PADDING / 2,
                                     center_y - PICKING_CIRCLE_PADDING / 2,
                                     PICKING_CIRCLE_PADDING,
                                     PICKING_CIRCLE_PADDING))
        self.assertEqual(self.a_spiro_gear.a_top_rect,
                         pygame.Rect(center_x - PICKING_CIRCLE_PADDING / 2,
                                     center_y - self.a_spiro_gear.a_radius - PICKING_CIRCLE_PADDING / 2,
                                     PICKING_CIRCLE_PADDING,
                                     PICKING_CIRCLE_PADDING))
        self.assertEqual(self.a_spiro_gear.a_center_rect,
                         pygame.Rect(center_x - PICKING_CIRCLE_PADDING / 2,
                                     center_y - PICKING_CIRCLE_PADDING / 2,
                                     PICKING_CIRCLE_PADDING,
                                     PICKING_CIRCLE_PADDING))

    def test_set_center_position(self):
        """スピロギアの中心座標の設定をテスト"""
        center_x, center_y = 200, 300
        self.a_spiro_gear.set_center_position(center_x, center_y)
        self.assertEqual(self.a_spiro_gear.a_center, (center_x, center_y))
        self.assertEqual(self.a_spiro_gear.a_bottom_rect,
                         pygame.Rect(center_x - PICKING_CIRCLE_PADDING / 2,
                                     center_y + self.a_spiro_gear.a_radius - PICKING_CIRCLE_PADDING / 2,
                                     PICKING_CIRCLE_PADDING,
                                     PICKING_CIRCLE_PADDING))
        self.assertEqual(self.a_spiro_gear.a_left_rect,
                         pygame.Rect(center_x - self.a_spiro_gear.a_radius - PICKING_CIRCLE_PADDING / 2,
                                     center_y - PICKING_CIRCLE_PADDING / 2,
                                     PICKING_CIRCLE_PADDING,
                                     PICKING_CIRCLE_PADDING))
        self.assertEqual(self.a_spiro_gear.a_right_rect,
                         pygame.Rect(center_x + self.a_spiro_gear.a_radius - PICKING_CIRCLE_PADDING / 2,
                                     center_y - PICKING_CIRCLE_PADDING / 2,
                                     PICKING_CIRCLE_PADDING,
                                     PICKING_CIRCLE_PADDING))
        self.assertEqual(self.a_spiro_gear.a_top_rect,
                         pygame.Rect(center_x - PICKING_CIRCLE_PADDING / 2,
                                     center_y - self.a_spiro_gear.a_radius - PICKING_CIRCLE_PADDING / 2,
                                     PICKING_CIRCLE_PADDING,
                                     PICKING_CIRCLE_PADDING))
        self.assertEqual(self.a_spiro_gear.a_center_rect,
                         pygame.Rect(center_x - PICKING_CIRCLE_PADDING / 2,
                                     center_y - PICKING_CIRCLE_PADDING / 2,
                                     PICKING_CIRCLE_PADDING,
                                     PICKING_CIRCLE_PADDING))

    def test_rotate(self):
        """スピロギアの回転のテスト"""
        degrees = 90
        self.a_spiro_gear.rotate(degrees)
        gear_x, gear_y = self.a_spiro_gear.center()

        bottom_x = gear_x + self.a_spiro_gear.radius() * math.cos(math.radians(degrees + 90))
        bottom_y = gear_y + self.a_spiro_gear.radius() * math.sin(math.radians(degrees + 90))
        bottom_x -= PICKING_CIRCLE_PADDING / 2
        bottom_y -= PICKING_CIRCLE_PADDING / 2

        left_x = gear_x + self.a_spiro_gear.radius() * math.cos(math.radians(degrees + 180))
        left_y = gear_y + self.a_spiro_gear.radius() * math.sin(math.radians(degrees + 180))
        left_x -= PICKING_CIRCLE_PADDING / 2
        left_y -= PICKING_CIRCLE_PADDING / 2

        right_x = gear_x + self.a_spiro_gear.radius() * math.cos(math.radians(degrees))
        right_y = gear_y + self.a_spiro_gear.radius() * math.sin(math.radians(degrees))
        right_x -= PICKING_CIRCLE_PADDING / 2
        right_y -= PICKING_CIRCLE_PADDING / 2

        top_x = gear_x + self.a_spiro_gear.radius() * math.cos(math.radians(degrees + 270))
        top_y = gear_y + self.a_spiro_gear.radius() * math.sin(math.radians(degrees + 270))
        top_x -= PICKING_CIRCLE_PADDING / 2
        top_y -= PICKING_CIRCLE_PADDING / 2
        self.assertEqual(self.a_spiro_gear.a_bottom_rect, pygame.Rect(bottom_x, bottom_y, PICKING_CIRCLE_PADDING, PICKING_CIRCLE_PADDING))
        self.assertEqual(self.a_spiro_gear.a_left_rect, pygame.Rect(left_x, left_y, PICKING_CIRCLE_PADDING, PICKING_CIRCLE_PADDING))
        self.assertEqual(self.a_spiro_gear.a_right_rect, pygame.Rect(right_x, right_y, PICKING_CIRCLE_PADDING, PICKING_CIRCLE_PADDING))
        self.assertEqual(self.a_spiro_gear.a_top_rect, pygame.Rect(top_x, top_y, PICKING_CIRCLE_PADDING, PICKING_CIRCLE_PADDING))

    def test_add_radius(self):
        """変化量によるギアの半径の更新のテスト"""
        self.assertEqual(self.a_spiro_gear.add_radius(30), True)
        self.assertEqual(self.a_spiro_gear.a_radius, 180)

        self.a_spiro_gear.set_radius(30)
        self.assertEqual(self.a_spiro_gear.add_radius(-20), False)
        self.assertEqual(self.a_spiro_gear.a_radius, 30)

        self.assertEqual(self.a_spiro_gear.add_radius(1500), False)
        self.assertEqual(self.a_spiro_gear.add_radius(1600), False)
        self.assertEqual(self.a_spiro_gear.add_radius(400), False)
        self.a_spiro_gear.set_center_position(1564, 50)
        self.assertEqual(self.a_spiro_gear.add_radius(60), False)
        self.assertEqual(self.a_spiro_gear.add_radius(3000), False)

    def test_set_radius(self):
        """ギアの半径が正しく設定されるかのテスト"""
        self.assertEqual(self.a_spiro_gear.set_radius(30), True)
        self.assertEqual(self.a_spiro_gear.set_radius(1600), False)
        self.assertEqual(self.a_spiro_gear.set_radius(1450), False)
        self.assertEqual(self.a_spiro_gear.set_radius(400), False)
        self.a_spiro_gear.set_center_position(1564, 50)
        self.assertEqual(self.a_spiro_gear.set_radius(60), False)
        self.assertEqual(self.a_spiro_gear.set_radius(3000), False)

    def test_bottom_rect(self):
        """ボトムレクトのテスト"""
        center_x, center_y = self.a_spiro_gear.center()
        self.a_spiro_gear.update_picking_rect()
        self.assertEqual(self.a_spiro_gear.bottom_rect(),
                         pygame.Rect(center_x - PICKING_CIRCLE_PADDING / 2,
                                     center_y + self.a_spiro_gear.a_radius - PICKING_CIRCLE_PADDING / 2,
                                     PICKING_CIRCLE_PADDING,
                                     PICKING_CIRCLE_PADDING))

    def test_left_rect(self):
        """レフトレクトのテスト"""
        center_x, center_y = self.a_spiro_gear.center()
        self.a_spiro_gear.update_picking_rect()
        self.assertEqual(self.a_spiro_gear.left_rect(),
                         (center_x - self.a_spiro_gear.a_radius - PICKING_CIRCLE_PADDING / 2,
                         center_y - PICKING_CIRCLE_PADDING / 2,
                         PICKING_CIRCLE_PADDING,
                         PICKING_CIRCLE_PADDING))

    def test_right_rect(self):
        """ライトレクトのテスト"""
        center_x, center_y = self.a_spiro_gear.center()
        self.a_spiro_gear.update_picking_rect()
        self.assertEqual(self.a_spiro_gear.right_rect(),
                         pygame.Rect(center_x + self.a_spiro_gear.a_radius - PICKING_CIRCLE_PADDING / 2,
                                     center_y - PICKING_CIRCLE_PADDING / 2,
                                     PICKING_CIRCLE_PADDING,
                                     PICKING_CIRCLE_PADDING))

    def test_top_rect(self):
        """トップレクトのテスト"""
        center_x, center_y = self.a_spiro_gear.center()
        self.a_spiro_gear.update_picking_rect()
        self.assertEqual(self.a_spiro_gear.top_rect(),
                         pygame.Rect(center_x - PICKING_CIRCLE_PADDING / 2,
                                     center_y - self.a_spiro_gear.a_radius - PICKING_CIRCLE_PADDING / 2,
                                     PICKING_CIRCLE_PADDING,
                                     PICKING_CIRCLE_PADDING))

    def test_center_rect(self):
        """センターレクトのテスト"""
        center_x, center_y = self.a_spiro_gear.center()
        self.a_spiro_gear.update_picking_rect()
        self.assertEqual(self.a_spiro_gear.center_rect(),
                         pygame.Rect(center_x - PICKING_CIRCLE_PADDING / 2,
                                     center_y - PICKING_CIRCLE_PADDING / 2,
                                     PICKING_CIRCLE_PADDING,
                                     PICKING_CIRCLE_PADDING))


if __name__ == '__main__':
    unittest.main()
