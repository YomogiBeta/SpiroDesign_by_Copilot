#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Dragon'
__version__ = '1.0.0'
__date__ = '2023/07/14 (Created: 2023/07/08 )'


import pygame
import unittest

from Model.SpurGear import SpurGear
from src.Constants import INIT_SPUR_GEAR_POSITION, INIT_SPUR_GEAR_RADIUS, PICKING_CIRCLE_PADDING


class TestSpurGear(unittest.TestCase):

    def setUp(self):
        """スパーギアに関わるテストの準備"""
        x, y = INIT_SPUR_GEAR_POSITION
        self.a_spur_gear = SpurGear(x, y, INIT_SPUR_GEAR_RADIUS)

    def test_init(self):
        """ピニオンギアのフィールドのテスト"""
        x, y = INIT_SPUR_GEAR_POSITION
        self.assertEqual(self.a_spur_gear.a_center, (x, y))
        center_x, center_y = self.a_spur_gear.center()
        self.assertEqual(self.a_spur_gear.a_radius, INIT_SPUR_GEAR_RADIUS)
        self.assertEqual(self.a_spur_gear.a_bottom_rect,
                         pygame.Rect(center_x - PICKING_CIRCLE_PADDING / 2,
                                     center_y + self.a_spur_gear.a_radius - PICKING_CIRCLE_PADDING / 2,
                                     PICKING_CIRCLE_PADDING,
                                     PICKING_CIRCLE_PADDING))
        self.assertEqual(self.a_spur_gear.a_left_rect,
                         pygame.Rect(center_x - self.a_spur_gear.a_radius - PICKING_CIRCLE_PADDING / 2,
                                     center_y - PICKING_CIRCLE_PADDING / 2,
                                     PICKING_CIRCLE_PADDING,
                                     PICKING_CIRCLE_PADDING))
        self.assertEqual(self.a_spur_gear.a_right_rect,
                         pygame.Rect(center_x + self.a_spur_gear.a_radius - PICKING_CIRCLE_PADDING / 2,
                                     center_y - PICKING_CIRCLE_PADDING / 2,
                                     PICKING_CIRCLE_PADDING,
                                     PICKING_CIRCLE_PADDING))
        self.assertEqual(self.a_spur_gear.a_top_rect,
                         pygame.Rect(center_x - PICKING_CIRCLE_PADDING / 2,
                                     center_y - self.a_spur_gear.a_radius - PICKING_CIRCLE_PADDING / 2,
                                     PICKING_CIRCLE_PADDING,
                                     PICKING_CIRCLE_PADDING))
        self.assertEqual(self.a_spur_gear.a_center_rect,
                         pygame.Rect(center_x - PICKING_CIRCLE_PADDING / 2,
                                     center_y - PICKING_CIRCLE_PADDING / 2,
                                     PICKING_CIRCLE_PADDING,
                                     PICKING_CIRCLE_PADDING))

    def test_set_center_position(self):
        """スパーギアの中心座標の設定のテスト"""
        x, y = INIT_SPUR_GEAR_POSITION
        center_x, center_y = self.a_spur_gear.center()
        self.assertEqual(self.a_spur_gear.set_center_position(center_x - x, center_y - y), False)
        self.assertEqual(self.a_spur_gear.set_center_position(center_x + 3000, center_y + 3000), False)
        self.assertEqual(self.a_spur_gear.set_center_position(center_x + 500, center_y + 500), True)
