#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Blue S, Dragon'
__version__ = '1.0.0'
__date__ = '2023/07/14 (Created: 2023/06/02 )'


import math
import pygame
import unittest
import utils

from Model.PinionGear import PinionGear
from src.Constants import INIT_PINION_GEAR_POSITION, INIT_PINION_GEAR_RADIUS, PICKING_CIRCLE_PADDING
from src.Constants import INIT_PEN_NIB, INIT_PEN_TO_PINION_DISTANCE


class TestPinionGear(unittest.TestCase):

    def setUp(self):
        """ピニオンギアに関わるテストの準備"""
        x, y = INIT_PINION_GEAR_POSITION
        self.a_pinion_gear = PinionGear(x, y, INIT_PINION_GEAR_RADIUS)

    def test_init(self):
        """ピニオンギアのフィールドのテスト"""
        center_x, center_y = INIT_PINION_GEAR_POSITION
        self.assertEqual(self.a_pinion_gear.a_center, (center_x, center_y))
        self.assertEqual(self.a_pinion_gear.a_radius, INIT_PINION_GEAR_RADIUS)
        self.assertEqual(self.a_pinion_gear.a_bottom_rect,
                         pygame.Rect(center_x - PICKING_CIRCLE_PADDING / 2,
                                     center_y + self.a_pinion_gear.a_radius - PICKING_CIRCLE_PADDING / 2,
                                     PICKING_CIRCLE_PADDING,
                                     PICKING_CIRCLE_PADDING))
        self.assertEqual(self.a_pinion_gear.a_left_rect,
                         pygame.Rect(center_x - self.a_pinion_gear.a_radius - PICKING_CIRCLE_PADDING / 2,
                                     center_y - PICKING_CIRCLE_PADDING / 2,
                                     PICKING_CIRCLE_PADDING,
                                     PICKING_CIRCLE_PADDING))
        self.assertEqual(self.a_pinion_gear.a_right_rect,
                         pygame.Rect(center_x + self.a_pinion_gear.a_radius - PICKING_CIRCLE_PADDING / 2,
                                     center_y - PICKING_CIRCLE_PADDING / 2,
                                     PICKING_CIRCLE_PADDING,
                                     PICKING_CIRCLE_PADDING))
        self.assertEqual(self.a_pinion_gear.a_top_rect,
                         pygame.Rect(center_x - PICKING_CIRCLE_PADDING / 2,
                                     center_y - self.a_pinion_gear.a_radius - PICKING_CIRCLE_PADDING / 2,
                                     PICKING_CIRCLE_PADDING,
                                     PICKING_CIRCLE_PADDING))
        self.assertEqual(self.a_pinion_gear.a_center_rect,
                         pygame.Rect(center_x - PICKING_CIRCLE_PADDING / 2,
                                     center_y - PICKING_CIRCLE_PADDING / 2,
                                     PICKING_CIRCLE_PADDING,
                                     PICKING_CIRCLE_PADDING))
        self.assertEqual(self.a_pinion_gear.a_pen_color, (0, 0, 0))
        self.assertEqual(self.a_pinion_gear.a_pen_to_pinion_degrees, 0.0)
        self.assertEqual(self.a_pinion_gear.a_pen_to_pinion_distance, INIT_PEN_TO_PINION_DISTANCE)
        rotate_radian = math.radians(self.a_pinion_gear.a_pen_to_pinion_degrees)
        move_pen_x = self.a_pinion_gear.a_pen_to_pinion_distance * math.cos(rotate_radian) + center_x
        move_pen_y = self.a_pinion_gear.a_pen_to_pinion_distance * math.sin(rotate_radian) + center_y
        self.assertEqual(self.a_pinion_gear.a_pen, pygame.Rect(move_pen_x, move_pen_y, INIT_PEN_NIB, INIT_PEN_NIB))

    def test_set_center_position(self):
        """ピニオンギアの中心座標の設定をテスト"""
        center_x, center_y = INIT_PINION_GEAR_POSITION
        center_x + 300, center_y + 200
        self.assertEqual(self.a_pinion_gear.set_center_position(center_x, center_y), None)
        self.assertEqual(self.a_pinion_gear.a_center, (center_x, center_y))
        rotate_radian = math.radians(self.a_pinion_gear.a_pen_to_pinion_degrees)
        move_pen_x = self.a_pinion_gear.a_pen_to_pinion_distance * math.cos(rotate_radian) + (center_x)
        move_pen_y = self.a_pinion_gear.a_pen_to_pinion_distance * math.sin(rotate_radian) + (center_y)
        self.assertEqual(self.a_pinion_gear.a_pen, pygame.Rect(move_pen_x, move_pen_y, INIT_PEN_NIB, INIT_PEN_NIB))

    def test_add_radius(self):
        """変化量によるピニオンギアの半径の更新のテスト"""
        self.assertEqual(self.a_pinion_gear.add_radius(-60), False)
        self.assertEqual(self.a_pinion_gear.add_radius(300), True)

    def test_set_radius(self):
        """ピニオンギアの半径がが設定されているかのテスト"""
        self.assertEqual(self.a_pinion_gear.set_radius(10), False)
        self.assertEqual(self.a_pinion_gear.set_radius(20), True)
        self.assertEqual(self.a_pinion_gear.a_pen_to_pinion_distance, 24)
        self.assertEqual(self.a_pinion_gear.set_radius(300), True)
        self.assertEqual(self.a_pinion_gear.a_pen_to_pinion_distance, 304)

    def test_force_set_radius(self):
        """半径が強制的に設定されるかのテスト"""
        self.assertEqual(self.a_pinion_gear.force_set_radius(500), None)
        self.assertEqual(self.a_pinion_gear.a_radius, 500)
        self.assertEqual(self.a_pinion_gear.a_pen_to_pinion_distance, 460)

    def test_set_pen_pos(self):
        """ペンの位置のテスト"""
        center_x, center_y = INIT_PINION_GEAR_POSITION
        rotate_radian = math.radians(self.a_pinion_gear.a_pen_to_pinion_degrees)
        move_pen_x = self.a_pinion_gear.a_pen_to_pinion_distance * math.cos(rotate_radian) + (center_x)
        move_pen_y = self.a_pinion_gear.a_pen_to_pinion_distance * math.sin(rotate_radian) + (center_y)

        self.a_pinion_gear.set_pen_pos(500, 213)
        self.assertEqual(self.a_pinion_gear.a_pen, pygame.Rect(move_pen_x, move_pen_y, INIT_PEN_NIB, INIT_PEN_NIB))

        center_x - 30, center_y + 30
        self.a_pinion_gear.set_pen_pos(center_x, center_y)
        rotate_radian = math.radians(self.a_pinion_gear.a_pen_to_pinion_degrees)
        move_pen_x = self.a_pinion_gear.a_pen_to_pinion_distance * math.cos(rotate_radian) + (center_x)
        move_pen_y = self.a_pinion_gear.a_pen_to_pinion_distance * math.sin(rotate_radian) + (center_y)
        self.assertEqual(self.a_pinion_gear.a_pen, pygame.Rect(move_pen_x, move_pen_y, INIT_PEN_NIB, INIT_PEN_NIB))

    def test_add_pen_pos(self):
        """変化量によるペンの位置の更新のテスト"""
        center_x, center_y = INIT_PINION_GEAR_POSITION
        self.a_pinion_gear.add_pen_pos(300, 200)
        rotate_radian = math.radians(self.a_pinion_gear.a_pen_to_pinion_degrees)
        move_pen_x = self.a_pinion_gear.a_pen_to_pinion_distance * math.cos(rotate_radian) + (center_x)
        move_pen_y = self.a_pinion_gear.a_pen_to_pinion_distance * math.sin(rotate_radian) + (center_y)
        self.assertEqual(self.a_pinion_gear.pen(), pygame.Rect(move_pen_x, move_pen_y, INIT_PEN_NIB, INIT_PEN_NIB))

        self.a_pinion_gear.add_pen_pos(30, 10)
        rotate_radian = math.radians(self.a_pinion_gear.a_pen_to_pinion_degrees)
        move_pen_x = self.a_pinion_gear.a_pen_to_pinion_distance * math.cos(rotate_radian) + (center_x)
        move_pen_y = self.a_pinion_gear.a_pen_to_pinion_distance * math.sin(rotate_radian) + (center_y)
        self.assertEqual(self.a_pinion_gear.pen(), pygame.Rect(move_pen_x, move_pen_y, INIT_PEN_NIB, INIT_PEN_NIB))

    def test_set_pen_color(self):
        """ペンの色設定のテスト"""
        self.a_pinion_gear.set_pen_color((100, 100, 100))
        self.assertEqual(self.a_pinion_gear.a_pen_color, (100, 100, 100))

        self.a_pinion_gear.set_pen_color((300, 100, 100))
        self.assertEqual(self.a_pinion_gear.a_pen_color, (100, 100, 100))

        self.a_pinion_gear.set_pen_color((100, -10, 100))
        self.assertEqual(self.a_pinion_gear.a_pen_color, (100, 100, 100))

    def test_set_pen_nib(self):
        """ペンの太さ設定のテスト"""
        center_x, center_y = INIT_PINION_GEAR_POSITION
        rotate_radian = math.radians(self.a_pinion_gear.a_pen_to_pinion_degrees)

        self.a_pinion_gear.set_pen_nib(1)
        move_pen_x = self.a_pinion_gear.a_pen_to_pinion_distance * math.cos(rotate_radian) + (center_x)
        move_pen_y = self.a_pinion_gear.a_pen_to_pinion_distance * math.sin(rotate_radian) + (center_y)
        self.assertEqual(self.a_pinion_gear.a_pen, pygame.Rect(move_pen_x, move_pen_y, INIT_PEN_NIB, INIT_PEN_NIB))

        self.a_pinion_gear.set_pen_nib(2)
        move_pen_x = self.a_pinion_gear.a_pen_to_pinion_distance * math.cos(rotate_radian) + (center_x)
        move_pen_y = self.a_pinion_gear.a_pen_to_pinion_distance * math.sin(rotate_radian) + (center_y)
        self.assertEqual(self.a_pinion_gear.a_pen, pygame.Rect(move_pen_x, move_pen_y, 2, 2))

        self.a_pinion_gear.set_pen_nib(5)
        move_pen_x = self.a_pinion_gear.a_pen_to_pinion_distance * math.cos(rotate_radian) + (center_x)
        move_pen_y = self.a_pinion_gear.a_pen_to_pinion_distance * math.sin(rotate_radian) + (center_y)
        self.assertEqual(self.a_pinion_gear.a_pen, pygame.Rect(move_pen_x, move_pen_y, 5, 5))

    def test_pen_to_pinion_degrees(self):
        """ピニオンギアの中心とペンの間の角度のテスト"""
        self.assertEqual(self.a_pinion_gear.a_pen_to_pinion_degrees, 0.0)
        pen_x, pen_y = self.a_pinion_gear.pen().topleft
        center_x, center_y = self.a_pinion_gear.center()
        degrees = utils.calculate_angle(center_x, center_y, pen_x + 10, pen_y + 10)
        self.a_pinion_gear.add_pen_pos(10, 10)
        self.assertEqual(self.a_pinion_gear.a_pen_to_pinion_degrees, degrees)

    def test_pen_to_pinion_distance(self):
        """ピニオンギアの中心とペンの間の距離のテスト"""
        self.assertEqual(self.a_pinion_gear.a_pen_to_pinion_distance, INIT_PEN_TO_PINION_DISTANCE)
        pen_x, pen_y = self.a_pinion_gear.pen().topleft
        center_x, center_y = self.a_pinion_gear.center()
        distance = math.sqrt((pen_x + 10 - center_x) ** 2 + (pen_y + 10 - center_y) ** 2)
        self.a_pinion_gear.add_pen_pos(10, 10)
        self.assertEqual(self.a_pinion_gear.a_pen_to_pinion_distance, distance)

    def test_pen(self):
        """ペン情報が正しく返されるかのテスト"""
        center_x, center_y = INIT_PINION_GEAR_POSITION
        center_x + 430, center_y + 215
        pen_nib = 6
        self.a_pinion_gear.set_pen_pos(center_x, center_y)
        self.a_pinion_gear.set_pen_nib(pen_nib)
        rotate_radian = math.radians(self.a_pinion_gear.a_pen_to_pinion_degrees)
        move_pen_x = self.a_pinion_gear.a_pen_to_pinion_distance * math.cos(rotate_radian) + (center_x)
        move_pen_y = self.a_pinion_gear.a_pen_to_pinion_distance * math.sin(rotate_radian) + (center_y)
        self.assertEqual(self.a_pinion_gear.pen(), pygame.Rect(move_pen_x, move_pen_y, pen_nib, pen_nib))

    def test_pen_color(self):
        """ペン色情報が正しく返されるかのテスト"""
        self.assertEqual(self.a_pinion_gear.pen_color(), (0, 0, 0))
        self.a_pinion_gear.set_pen_color((100, 100, 100))
        self.assertEqual(self.a_pinion_gear.pen_color(), (100, 100, 100))


if __name__ == '__main__':
    unittest.main()
