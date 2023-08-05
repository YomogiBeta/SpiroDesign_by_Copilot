#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'Blue S,Dragon'
__version__ = '1.0.0'
__date__ = '2023/07/14 (Created: 2023/06/20 )'

import math
import pygame
import unittest
import utils

from Model.SpiroModel import SpiroModel
from View.SpiroView import SpiroView
from Model.SpurGear import SpurGear
from Model.PinionGear import PinionGear
from src.Constants import INIT_BOARD_POSITION, DISPLAY_WIDTH, DISPLAY_HEIGHT, ACTIVE_SURFACE_PADDING, INIT_PEN_NIB, PICKING_CIRCLE_PADDING
from src.Constants import INIT_SPUR_GEAR_POSITION, INIT_SPUR_GEAR_RADIUS, INIT_PINION_GEAR_POSITION, INIT_PINION_GEAR_RADIUS
from src.Constants import BOARD_WIDTH, BOARD_HEIGHT
from bridge_pyjs import ui_call


class TestSpiroModel(unittest.TestCase):

    def setUp(self):
        """スピロモデルに関わるテストの準備"""
        ui_call.init()
        screen_surface = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA | pygame.DOUBLEBUF)
        ui_surface = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)
        self.a_spiro_model = SpiroModel(SpiroView(screen_surface, ui_surface))
        self.a_spiro_model.a_spiro_view.set_spiro_model(self.a_spiro_model)

    def test_init(self):
        """スピロモデルのフィールドのテスト"""
        self.assertIsInstance(self.a_spiro_model.a_spiro_view, SpiroView)
        self.assertIsInstance(self.a_spiro_model.a_spur_gear, SpurGear)
        self.assertEqual(self.a_spiro_model.a_spur_gear.center(), INIT_SPUR_GEAR_POSITION)
        self.assertEqual(self.a_spiro_model.a_spur_gear.radius(), INIT_SPUR_GEAR_RADIUS)
        self.assertIsInstance(self.a_spiro_model.a_pinion_gear, PinionGear)
        self.assertEqual(self.a_spiro_model.a_pinion_gear.center(), INIT_PINION_GEAR_POSITION)
        self.assertEqual(self.a_spiro_model.a_pinion_gear.radius(), INIT_PINION_GEAR_RADIUS)
        self.assertIsInstance(self.a_spiro_model.a_main_board_surface, pygame.Surface)
        self.assertEqual(self.a_spiro_model.a_main_board_surface_pos, INIT_BOARD_POSITION)
        self.assertIsInstance(self.a_spiro_model.a_gear_surface, pygame.Surface)
        self.assertEqual(self.a_spiro_model.an_active_surface, None)
        self.assertEqual(self.a_spiro_model.an_active_surface_pos, (0, 0))
        self.assertEqual(self.a_spiro_model.is_animated, False)
        self.assertEqual(self.a_spiro_model.is_rainbow, False)
        self.assertEqual(self.a_spiro_model.is_dived, True)
        self.assertEqual(self.a_spiro_model.is_circumscribe, False)

    def test_run(self):
        """runメソッドが正常終了かのテスト"""
        self.assertEqual(self.a_spiro_model.run(), None)

    def test_draw_frame(self):
        """描画処理が正常終了かのテスト"""
        self.assertEqual(self.a_spiro_model.draw_frame(), None)

    def test_set_spur_gear_center_position(self):
        """スーパーギアの中心座標の設定のテスト"""
        x, y = INIT_SPUR_GEAR_POSITION
        spur_gear_center_x, spur_gear_center_y = self.a_spiro_model.a_spur_gear.center()
        pinion_gear_center_x, pinion_gear_center_y = self.a_spiro_model.a_pinion_gear.center()
        self.a_spiro_model.set_spur_gear_center_position(spur_gear_center_x - x, spur_gear_center_y - y)
        self.assertEqual(self.a_spiro_model.a_spur_gear.center(), (spur_gear_center_x, spur_gear_center_y))
        self.assertEqual(self.a_spiro_model.a_pinion_gear.center(), (pinion_gear_center_x, pinion_gear_center_y))

        x, y = INIT_SPUR_GEAR_POSITION
        x += 30
        y += 60
        spur_gear_center_x, spur_gear_center_y = self.a_spiro_model.a_spur_gear.center()
        pinion_gear_center_x, pinion_gear_center_y = self.a_spiro_model.a_pinion_gear.center()
        dx, dy = x - spur_gear_center_x, y - spur_gear_center_y

        self.a_spiro_model.set_spur_gear_center_position(x, y)
        spur_gear_center_x, spur_gear_center_y = self.a_spiro_model.a_spur_gear.center()
        self.assertEqual(self.a_spiro_model.a_spur_gear.center(), (spur_gear_center_x, spur_gear_center_y))
        self.assertEqual(self.a_spiro_model.a_pinion_gear.center(), (pinion_gear_center_x + dx, pinion_gear_center_y + dy))

    def test_set_pinion_gear_center_position(self):
        """ピニオンギアの中心座標の設定のテスト"""
        x, y = INIT_PINION_GEAR_POSITION
        self.a_spiro_model.set_pinion_gear_center_position(x + 600, y)
        self.assertEqual(self.a_spiro_model.a_pinion_gear.center(), (x, y))

        x - (INIT_SPUR_GEAR_RADIUS - INIT_PINION_GEAR_RADIUS) * 2
        self.a_spiro_model.set_pinion_gear_center_position(x - (INIT_SPUR_GEAR_RADIUS - INIT_PINION_GEAR_RADIUS) * 2, y)
        self.assertEqual(self.a_spiro_model.a_pinion_gear.center(), (x - (INIT_SPUR_GEAR_RADIUS - INIT_PINION_GEAR_RADIUS) * 2, y))

        self.a_spiro_model.is_circumscribe = True
        x, y = INIT_PINION_GEAR_POSITION
        self.a_spiro_model.set_pinion_gear_center_position(x + (INIT_PINION_GEAR_RADIUS * 2), y)
        self.assertEqual(self.a_spiro_model.a_pinion_gear.center(), (x + (INIT_PINION_GEAR_RADIUS * 2), y))

    def test_add_spur_gear_position(self):
        """変化量によるスパーギアの中心座標の更新のテスト"""
        add_x, add_y = 10, 20
        spur_gear_center_x, spur_gear_center_y = self.a_spiro_model.a_spur_gear.center()
        self.a_spiro_model.add_spur_gear_position(add_x, add_y)
        self.assertEqual(self.a_spiro_model.a_spur_gear.center(), (spur_gear_center_x + add_x, spur_gear_center_y + add_y))

    def test_add_pinion_gear_position(self):
        """変化量によるピニオンギアの中心座標の更新のテスト"""
        dx, dy = 10, 20
        self.a_spiro_model.add_pinion_gear_position(dx, dy)
        center_x, center_y = self.a_spiro_model.a_pinion_gear.center()
        self.assertEqual(self.a_spiro_model.a_pinion_gear.center(), (center_x, center_y))

    def test_add_spur_gear_radius(self):
        """変化量によるスパーギアの半径の更新のテスト"""
        spur_gear_center_x, spur_gear_center_y = self.a_spiro_model.a_spur_gear.center()
        pinion_gear_center_x, pinion_gear_center_y = self.a_spiro_model.a_pinion_gear.center()
        add_radius = -40
        radius = self.a_spiro_model.a_spur_gear.radius()
        self.a_spiro_model.add_spur_gear_radius(add_radius)
        self.assertEqual(self.a_spiro_model.a_spur_gear.center(), (spur_gear_center_x, spur_gear_center_y))
        self.assertEqual(self.a_spiro_model.a_spur_gear.radius(), radius)
        self.assertEqual(self.a_spiro_model.a_pinion_gear.radius(), INIT_PINION_GEAR_RADIUS)
        self.assertEqual(self.a_spiro_model.a_pinion_gear.center(), (pinion_gear_center_x, pinion_gear_center_y))

        add_radius = 30
        radius = self.a_spiro_model.a_spur_gear.radius()
        spur_gear_center_x, spur_gear_center_y = self.a_spiro_model.a_spur_gear.center()
        self.a_spiro_model.add_spur_gear_radius(add_radius)
        pinion_gear_center_x, pinion_gear_center_y = self.a_spiro_model.a_pinion_gear.center()
        self.assertEqual(self.a_spiro_model.a_spur_gear.center(), (spur_gear_center_x, spur_gear_center_y))
        self.assertEqual(self.a_spiro_model.a_spur_gear.radius(), radius + add_radius)
        self.assertEqual(self.a_spiro_model.a_pinion_gear.radius(), INIT_PINION_GEAR_RADIUS)
        self.assertEqual(self.a_spiro_model.a_pinion_gear.center(),
                         (pinion_gear_center_x,
                         pinion_gear_center_y))

    def test_add_pinion_gear_radius(self):
        """変化量によるピニオンギアの半径の更新のテスト"""
        add_radius = 30
        self.a_spiro_model.add_pinion_gear_radius(add_radius)
        self.assertEqual(self.a_spiro_model.a_pinion_gear.a_radius, INIT_PINION_GEAR_RADIUS)

        add_radius = 10
        radius = self.a_spiro_model.a_pinion_gear.radius()
        self.a_spiro_model.add_pinion_gear_radius(add_radius)
        self.assertEqual(self.a_spiro_model.a_pinion_gear.a_radius, radius + add_radius)

        self.a_spiro_model.is_circumscribe = True
        add_radius = 30
        radius = self.a_spiro_model.a_pinion_gear.radius()
        self.a_spiro_model.add_pinion_gear_radius(add_radius)
        self.assertEqual(self.a_spiro_model.a_pinion_gear.a_radius, radius + add_radius)

    def test_check_picking_spur_wheel(self):
        """スパーギアのホイール選択のテスト"""
        center_x, center_y = self.a_spiro_model.a_spur_gear.center()
        self.a_spiro_model.a_spur_gear.update_picking_rect()
        self.assertEqual(self.a_spiro_model.check_picking_spur_wheel(center_x, center_y), None)
        self.assertEqual(self.a_spiro_model.check_picking_spur_wheel(
            center_x - PICKING_CIRCLE_PADDING / 2,
            center_y + self.a_spiro_model.a_spur_gear.a_radius - PICKING_CIRCLE_PADDING / 2),
            'bottom')

        self.assertEqual(self.a_spiro_model.check_picking_spur_wheel(
            center_x - self.a_spiro_model.a_spur_gear.a_radius - PICKING_CIRCLE_PADDING / 2,
            center_y - PICKING_CIRCLE_PADDING / 2),
            'left')
        self.assertEqual(self.a_spiro_model.check_picking_spur_wheel(
            center_x + self.a_spiro_model.a_spur_gear.a_radius - PICKING_CIRCLE_PADDING / 2,
            center_y - PICKING_CIRCLE_PADDING / 2),
            'right')
        self.assertEqual(self.a_spiro_model.check_picking_spur_wheel(
            center_x - PICKING_CIRCLE_PADDING / 2,
            center_y - self.a_spiro_model.a_spur_gear.a_radius - PICKING_CIRCLE_PADDING / 2),
            'top')

    def test_check_picking_pinion_wheel(self):
        """ピニオンギアのホイール選択のテスト"""
        center_x, center_y = self.a_spiro_model.a_pinion_gear.center()
        self.a_spiro_model.a_pinion_gear.update_picking_rect()
        self.assertEqual(self.a_spiro_model.check_picking_pinion_wheel(center_x, center_y), None)
        self.assertEqual(self.a_spiro_model.check_picking_pinion_wheel(
            center_x - PICKING_CIRCLE_PADDING / 2,
            center_y + self.a_spiro_model.a_pinion_gear.a_radius - PICKING_CIRCLE_PADDING / 2),
            'bottom')

        self.assertEqual(self.a_spiro_model.check_picking_pinion_wheel(
            center_x - self.a_spiro_model.a_pinion_gear.a_radius - PICKING_CIRCLE_PADDING / 2,
            center_y - PICKING_CIRCLE_PADDING / 2),
            'left')
        self.assertEqual(self.a_spiro_model.check_picking_pinion_wheel(
            center_x + self.a_spiro_model.a_pinion_gear.a_radius - PICKING_CIRCLE_PADDING / 2,
            center_y - PICKING_CIRCLE_PADDING / 2),
            'right')
        self.assertEqual(self.a_spiro_model.check_picking_pinion_wheel(
            center_x - PICKING_CIRCLE_PADDING / 2,
            center_y - self.a_spiro_model.a_pinion_gear.a_radius - PICKING_CIRCLE_PADDING / 2),
            'top')

    def test_check_spur_selected_wheel(self):
        """スパーギアの中心選択のテスト"""
        center_x, center_y = self.a_spiro_model.a_spur_gear.center()
        self.a_spiro_model.a_spur_gear.update_picking_rect()
        self.assertEqual(self.a_spiro_model.check_spur_selected_wheel(
            center_x + 500,
            center_y + 200),
            False)
        self.assertEqual(self.a_spiro_model.check_spur_selected_wheel(
            center_x - PICKING_CIRCLE_PADDING / 2,
            center_y - PICKING_CIRCLE_PADDING / 2),
            True)

    def test_check_pinion_selected_wheel(self):
        """ピニオンギアギアの中心選択のテスト"""
        center_x, center_y = self.a_spiro_model.a_pinion_gear.center()
        self.a_spiro_model.a_pinion_gear.update_picking_rect()
        self.assertEqual(self.a_spiro_model.check_pinion_selected_wheel(
            center_x + 30,
            center_y + 20),
            False)
        self.assertEqual(self.a_spiro_model.check_pinion_selected_wheel(
            center_x - PICKING_CIRCLE_PADDING / 2,
            center_y - PICKING_CIRCLE_PADDING / 2),
            True)

    def test_check_pen_selected_wheel(self):
        """ペンの選択のテスト"""
        center_x, center_y = self.a_spiro_model.a_pinion_gear.center()
        rotate_radian = math.radians(self.a_spiro_model.a_pinion_gear.a_pen_to_pinion_degrees)
        move_pen_x = self.a_spiro_model.a_pinion_gear.a_pen_to_pinion_distance * math.cos(rotate_radian) + center_x
        move_pen_y = self.a_spiro_model.a_pinion_gear.a_pen_to_pinion_distance * math.sin(rotate_radian) + center_y
        self.assertEqual(self.a_spiro_model.check_pen_selected_wheel(move_pen_x, move_pen_y), True)
        self.assertEqual(self.a_spiro_model.check_pen_selected_wheel(move_pen_x - 30, move_pen_y + 20), False)

    def test_add_pen_pos(self):
        """変化量によるペンの座標の更新のテスト"""
        center_x, center_y = self.a_spiro_model.a_pinion_gear.center()
        self.a_spiro_model.add_pen_pos(10, 10)
        rotate_radian = math.radians(self.a_spiro_model.a_pinion_gear.a_pen_to_pinion_degrees)
        move_pen_x = self.a_spiro_model.a_pinion_gear.a_pen_to_pinion_distance * math.cos(rotate_radian) + (center_x)
        move_pen_y = self.a_spiro_model.a_pinion_gear.a_pen_to_pinion_distance * math.sin(rotate_radian) + (center_y)
        self.assertEqual(self.a_spiro_model.a_pinion_gear.a_pen, pygame.Rect(move_pen_x, move_pen_y, INIT_PEN_NIB, INIT_PEN_NIB))

    def test_set_pen_nib(self):
        """ペンの太さ設定のテスト"""
        center_x, center_y = self.a_spiro_model.a_pinion_gear.center()
        self.a_spiro_model.set_pen_nib(3)
        rotate_radian = math.radians(self.a_spiro_model.a_pinion_gear.a_pen_to_pinion_degrees)
        move_pen_x = self.a_spiro_model.a_pinion_gear.a_pen_to_pinion_distance * math.cos(rotate_radian) + (center_x)
        move_pen_y = self.a_spiro_model.a_pinion_gear.a_pen_to_pinion_distance * math.sin(rotate_radian) + (center_y)
        self.assertEqual(self.a_spiro_model.a_pinion_gear.a_pen, pygame.Rect(move_pen_x, move_pen_y, 3, 3))

    def test_set_pen_color(self):
        """ペンの色設定のテスト"""
        self.a_spiro_model.set_pen_color((0, 255, 0))
        self.assertEqual(self.a_spiro_model.a_pinion_gear.a_pen_color, (0, 255, 0))

    def test_pen_rainbow(self):
        """ペンが虹色遷移のテスト"""
        self.a_spiro_model.a_pinion_gear.set_pen_color((255, 200, 0))
        self.a_spiro_model.pen_rainbow()
        self.assertEqual(self.a_spiro_model.a_pinion_gear.a_pen_color, (255, 205, 0))

        self.a_spiro_model.a_pinion_gear.set_pen_color((10, 255, 0))
        self.a_spiro_model.pen_rainbow()
        self.assertEqual(self.a_spiro_model.a_pinion_gear.a_pen_color, (5, 255, 0))

        self.a_spiro_model.a_pinion_gear.set_pen_color((0, 255, 200))
        self.a_spiro_model.pen_rainbow()
        self.assertEqual(self.a_spiro_model.a_pinion_gear.a_pen_color, (0, 255, 205))

        self.a_spiro_model.a_pinion_gear.set_pen_color((245, 0, 255))
        self.a_spiro_model.pen_rainbow()
        self.assertEqual(self.a_spiro_model.a_pinion_gear.a_pen_color, (250, 0, 255))

        self.a_spiro_model.a_pinion_gear.set_pen_color((255, 0, 10))
        self.a_spiro_model.pen_rainbow()
        self.assertEqual(self.a_spiro_model.a_pinion_gear.a_pen_color, (255, 0, 5))

    def test_start_rainbow(self):
        """虹色モード開始のテスト"""
        self.a_spiro_model.start_rainbow()
        self.assertEqual(self.a_spiro_model.rainbow(), True)

    def test_stop_rainbow(self):
        """虹色モード停止のテスト"""
        self.a_spiro_model.stop_rainbow()
        self.assertEqual(self.a_spiro_model.rainbow(), False)

    def test_start_animation(self):
        """アニメーション開始のテスト"""
        self.a_spiro_model.start_animation()
        self.assertEqual(self.a_spiro_model.animation(), True)

    def test_stop_animation(self):
        """アニメーション停止のテスト"""
        self.a_spiro_model.stop_animation()
        self.assertEqual(self.a_spiro_model.animation(), False)

    def test_start_circumscribe(self):
        """外接円モード開始のテスト"""
        self.a_spiro_model.start_circumscribe()
        self.assertEqual(self.a_spiro_model.is_circumscribe, True)

    def test_stop_circumscribe(self):
        """外接円モード停止のテスト"""
        self.a_spiro_model.stop_circumscribe()
        self.assertEqual(self.a_spiro_model.is_circumscribe, False)

    def test_current_clear(self):
        """current_clearの正常終了のテスト"""
        self.assertEqual(self.a_spiro_model.current_clear(), None)

    def test_clear(self):
        """clearの正常終了のテスト"""
        self.assertEqual(self.a_spiro_model.clear(), None)

    def test_dive(self):
        """diveのテスト"""
        self.assertEqual(self.a_spiro_model.dive(), None)
        self.assertEqual(self.a_spiro_model.is_dived, True)
        self.assertEqual(self.a_spiro_model.an_active_surface, None)

    def test_check_dive(self):
        """dive状態のテスト"""
        self.assertEqual(self.a_spiro_model.check_dive(), True)
        self.a_spiro_model.is_animated = True
        self.a_spiro_model.run()
        self.assertEqual(self.a_spiro_model.check_dive(), False)

    # def test_open_file(self):
    #     self.a_spiro_model.open_file()

    # def test_save_file(self):
    #     self.a_spiro_model.save_file()

    def test_set_create_active_surface(self):
        """アクティブサーフェイスの作成テスト"""
        self.a_spiro_model.set_spur_gear_center_position(300, 300)
        self.a_spiro_model.set_create_active_surface()
        self.assertIsInstance(self.a_spiro_model.an_active_surface, pygame.Surface)

        size = (self.a_spiro_model.a_spur_gear.a_radius * 2) + (self.a_spiro_model.a_pinion_gear.a_radius * 4) + ACTIVE_SURFACE_PADDING
        a_spur_gear_x, a_spur_gear_y = self.a_spiro_model.a_spur_gear.center()
        active_surface_x = a_spur_gear_x - (size / 2)
        active_surface_y = a_spur_gear_y - (size / 2)
        self.assertEqual(self.a_spiro_model.an_active_surface_pos, (active_surface_x, active_surface_y))

    def test_move_main_board_surface(self):
        """変化量によるメインボードの座標の更新のテスト"""
        dx, dy = 30, 20
        self.a_spiro_model.move_main_board_surface(dx, dy)
        main_board_x, main_board_y = self.a_spiro_model.a_main_board_surface_pos
        self.assertEqual(self.a_spiro_model.a_main_board_surface_pos, (main_board_x, main_board_y))

    def test_speed_up(self):
        """描画速度アップのテスト"""
        self.a_spiro_model.speed_up()
        self.a_spiro_model.speed_up()
        self.a_spiro_model.speed_up()
        self.a_spiro_model.speed_up()
        self.assertEqual(self.a_spiro_model._an_add_angle, 5)
        self.a_spiro_model.speed_up()
        self.a_spiro_model.speed_up()
        self.a_spiro_model.speed_up()
        self.a_spiro_model.speed_up()
        self.a_spiro_model.speed_up()
        self.assertEqual(self.a_spiro_model._an_add_angle, 10)
        self.a_spiro_model.speed_up()
        self.a_spiro_model.speed_up()
        self.assertEqual(self.a_spiro_model._an_add_angle, 10)

    def test_speed_down(self):
        """描画速度ダウンのテスト"""
        self.a_spiro_model.speed_up()
        self.a_spiro_model.speed_up()
        self.a_spiro_model.speed_up()
        self.a_spiro_model.speed_up()
        self.assertEqual(self.a_spiro_model._an_add_angle, 5)
        self.a_spiro_model.speed_down()
        self.a_spiro_model.speed_down()
        self.a_spiro_model.speed_down()
        self.a_spiro_model.speed_down()
        self.assertEqual(self.a_spiro_model._an_add_angle, 1)
        self.a_spiro_model.speed_down()
        self.a_spiro_model.speed_down()
        self.assertEqual(self.a_spiro_model._an_add_angle, 1)

    def test_main_board_surface(self):
        """メインボード情報のテスト"""
        self.assertIsInstance(self.a_spiro_model.main_board_surface(), pygame.Surface)
        self.assertEqual(self.a_spiro_model.a_main_board_surface_pos, INIT_BOARD_POSITION)

    def test_main_board_surface_pos(self):
        """メインボード座標情報のテスト"""
        dx, dy = 30, 20
        self.a_spiro_model.move_main_board_surface(dx, dy)
        main_board_x, main_board_y = self.a_spiro_model.a_main_board_surface_pos
        self.assertEqual(self.a_spiro_model.main_board_surface_pos(), (main_board_x, main_board_y))

    def test_gear_surface(self):
        """ギアサーフェイス情報のテスト"""
        self.assertIsInstance(self.a_spiro_model.gear_surface(), pygame.Surface)
        self.assertEqual(self.a_spiro_model.a_gear_surface.get_width(), BOARD_WIDTH)
        self.assertEqual(self.a_spiro_model.a_gear_surface.get_height(), BOARD_HEIGHT)

    def test_active_surface(self):
        """アクティブサーフェイス情報のテスト"""
        self.a_spiro_model.set_spur_gear_center_position(300, 300)
        self.a_spiro_model.set_create_active_surface()
        size = (self.a_spiro_model.a_spur_gear.a_radius * 2) + (self.a_spiro_model.a_pinion_gear.a_radius * 4) + ACTIVE_SURFACE_PADDING
        a_spur_gear_x, a_spur_gear_y = self.a_spiro_model.a_spur_gear.center()
        active_surface_x = a_spur_gear_x - (size / 2)
        active_surface_y = a_spur_gear_y - (size / 2)
        self.assertIsInstance(self.a_spiro_model.active_surface(), pygame.Surface)
        self.assertEqual(self.a_spiro_model.active_surface_pos(), (active_surface_x, active_surface_y))
        self.assertEqual(self.a_spiro_model.an_active_surface.get_width(), size)
        self.assertEqual(self.a_spiro_model.an_active_surface.get_height(), size)

    def test_active_surface_pos(self):
        """アクティブサーフェイス座標情報のテスト"""
        self.a_spiro_model.set_spur_gear_center_position(300, 300)
        self.a_spiro_model.set_create_active_surface()
        size = (self.a_spiro_model.a_spur_gear.a_radius * 2) + (self.a_spiro_model.a_pinion_gear.a_radius * 4) + ACTIVE_SURFACE_PADDING
        a_spur_gear_x, a_spur_gear_y = self.a_spiro_model.a_spur_gear.center()
        active_surface_x = a_spur_gear_x - (size / 2)
        active_surface_y = a_spur_gear_y - (size / 2)
        self.assertEqual(self.a_spiro_model.active_surface_pos(), (active_surface_x, active_surface_y))

    def test_spur_gear(self):
        """スパーギア情報のテスト"""
        self.assertIsInstance(self.a_spiro_model.spur_gear(), SpurGear)
        self.assertEqual(self.a_spiro_model.a_spur_gear.center(), INIT_SPUR_GEAR_POSITION)
        self.assertEqual(self.a_spiro_model.a_spur_gear.radius(), INIT_SPUR_GEAR_RADIUS)

        self.a_spiro_model.a_spur_gear.set_center_position(2000, 2000)
        self.a_spiro_model.a_spur_gear.set_radius(300)
        self.assertEqual(self.a_spiro_model.a_spur_gear.center(), (2000, 2000))
        self.assertEqual(self.a_spiro_model.a_spur_gear.radius(), 300)

    def test_pinion_gear(self):
        """ピニオンギア情報のテスト"""
        self.assertIsInstance(self.a_spiro_model.pinion_gear(), PinionGear)
        self.assertEqual(self.a_spiro_model.a_pinion_gear.center(), INIT_PINION_GEAR_POSITION)
        self.assertEqual(self.a_spiro_model.a_pinion_gear.radius(), INIT_PINION_GEAR_RADIUS)

        x, y = INIT_PINION_GEAR_POSITION
        spur_gear_center_x, spur_gear_center_y = self.a_spiro_model.a_spur_gear.center()
        dx = (x + 10) - spur_gear_center_x
        dy = (y + 10) - spur_gear_center_y
        gear_distance = self.a_spiro_model.a_spur_gear.radius() - self.a_spiro_model.a_pinion_gear.radius(
        ) if not self.a_spiro_model.is_circumscribe else self.a_spiro_model.a_spur_gear.radius() + self.a_spiro_model.a_pinion_gear.radius()
        amount_of_increase_in_x, amount_of_increase_in_y = utils.convert_length_of_line_to_x_and_y(
            dx, dy, gear_distance)
        pinion_x = spur_gear_center_x + amount_of_increase_in_x
        pinion_y = spur_gear_center_y + amount_of_increase_in_y
        self.a_spiro_model.add_pinion_gear_position(10, 10)
        self.assertEqual(self.a_spiro_model.a_pinion_gear.center(), (pinion_x, pinion_y))
        self.a_spiro_model.add_pinion_gear_radius(10)
        self.assertEqual(self.a_spiro_model.a_pinion_gear.radius(), INIT_PINION_GEAR_RADIUS + 10)

    def test_animation(self):
        """アニメーション情報のテスト"""
        self.a_spiro_model.start_animation()
        self.assertEqual(self.a_spiro_model.animation(), True)
        self.a_spiro_model.stop_animation()
        self.assertEqual(self.a_spiro_model.animation(), False)

    def test_rainbow(self):
        """レインボー情報のテスト"""
        self.a_spiro_model.start_rainbow()
        self.assertEqual(self.a_spiro_model.rainbow(), True)
        self.a_spiro_model.stop_rainbow()
        self.assertEqual(self.a_spiro_model.rainbow(), False)

    if __name__ == '__main__':
        unittest.main()
