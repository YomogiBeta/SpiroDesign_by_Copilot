#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Dragon'
__version__ = '1.0.0'
__date__ = '2023/07/14 (Created: 2023/07/08 )'


import unittest

from View.UiView import UiView
from Constants import DISPLAY_WIDTH, DISPLAY_HEIGHT
from bridge_pyjs.PygameBridge import pygame


class TestUiView(unittest.TestCase):

    def setUp(self):
        """Uiビューに関わるテストの準備"""
        self.a_ui_view = UiView(pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA))
        pygame.init()

    def test_init(self):
        """Uiビューのフィールドのテスト"""
        self.assertIsInstance(self.a_ui_view.a_ui_surface, pygame.Surface)
        self.assertEqual(self.a_ui_view.a_ui_surface.get_width(), DISPLAY_WIDTH)
        self.assertEqual(self.a_ui_view.a_ui_surface.get_height(), DISPLAY_HEIGHT)

    def test_draw_square(self):
        """四角形の描画テスト"""
        square = self.a_ui_view.draw_square(10, 10, 30, 40, (255, 255, 255), 30)
        self.assertEqual(square, pygame.Rect(10, 10, 30, 40))

    def test_draw_shadow(self):
        """影の描画テスト"""
        shadow1, shadow2, shadow3, shadow4 = self.a_ui_view.draw_shadow(10, 10, 30, 40, 10)
        self.assertEqual(shadow1, pygame.Rect(4, 4, 41, 51))
        self.assertEqual(shadow2, pygame.Rect(6, 6, 37, 47))
        self.assertEqual(shadow3, pygame.Rect(8, 8, 34, 44))
        self.assertEqual(shadow4, pygame.Rect(9, 9, 32, 42))

    def test_draw_text(self):
        """テキストの描画テスト"""
        self.assertEqual(self.a_ui_view.draw_text(10, 10, 'test', (255, 255, 255)), None)

    def test_draw_divider(self):
        """区切り線の描画テスト"""
        self.assertEqual(self.a_ui_view.draw_divider(10, 10, 30), None)

    def test_clear_rect(self):
        """clear_rectの正常終了かのテスト"""
        self.assertEqual(self.a_ui_view.clear_rect(pygame.Rect(10, 10, 10, 10)), None)

    def test_clear_ui_draw(self):
        """clear_ui_drawの正常終了かのテスト"""
        self.assertEqual(self.a_ui_view.clear_ui_draw(), None)

    def test_ui_surface(self):
        """Uiサーフェイス情報のテスト"""
        self.assertEqual(self.a_ui_view.ui_surface(), self.a_ui_view.a_ui_surface)
