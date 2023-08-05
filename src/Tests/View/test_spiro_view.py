#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Dragon'
__version__ = '1.0.0'
__date__ = '2023/07/14 (Created: 2023/07/08 )'


import unittest

from Model.SpiroModel import SpiroModel
from Model.SpurGear import SpurGear
from View.SpiroView import SpiroView
from Constants import DISPLAY_WIDTH, DISPLAY_HEIGHT
from bridge_pyjs.PygameBridge import pygame


class TestSpiroView(unittest.TestCase):

    def setUp(self):
        """スピロビューに関わるテストの準備"""
        screen_surface = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA | pygame.DOUBLEBUF)
        ui_surface = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)
        self.a_spiro_view = SpiroView(screen_surface, ui_surface)
        self.a_spiro_view.set_spiro_model(SpiroModel(self.a_spiro_view))

    def test_init(self):
        """スピロビューのフィールドのテスト"""
        self.assertEqual(self.a_spiro_view.a_screen, pygame.display.set_mode(
            (DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA | pygame.DOUBLEBUF))
        self.assertIsInstance(self.a_spiro_view.a_spiro_model, SpiroModel)

    def test_set_spiro_model(self):
        """スピロモデルが束縛されているかのテスト"""
        self.assertIsInstance(self.a_spiro_view.a_spiro_model, SpiroModel)

    def test_draw_spur_gear(self):
        """スパーギアの描画処理が正常終了かのテスト"""
        self.assertEqual(self.a_spiro_view.draw_spur_gear(), None)

    def test_draw_pinion_gear(self):
        """ピニオンギアの描画処理が正常終了かのテスト"""
        self.assertEqual(self.a_spiro_view.draw_pinion_gear(), None)

    def test_draw_gear_base(self):
        """ギアーベースの描画処理が正常終了かのテスト"""
        a_draw_surface = self.a_spiro_view.a_spiro_model.gear_surface()
        a_spur_gear: SpurGear = self.a_spiro_view.a_spiro_model.spur_gear()
        self.assertEqual(self.a_spiro_view.draw_gear_base(a_draw_surface, a_spur_gear, (255, 0, 0)), None)

    def test_draw_gear_connection_line(self):
        """スパーギアとピニオンギアの中心を結ぶペンの描画処理が正常終了かのテスト"""
        self.assertEqual(self.a_spiro_view.draw_gear_connection_line(), None)

    def test_draw_pen_pos(self):
        """ペンの位置への描画処理が正常終了かのテスト"""
        self.assertEqual(self.a_spiro_view.draw_pen_pos(list[0, 0]), None)

    def test_commit(self):
        """描画確定の正常終了のテスト"""
        self.assertEqual(self.a_spiro_view.commit(), None)
