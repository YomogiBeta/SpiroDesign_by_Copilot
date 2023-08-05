#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'SHIRO, Dragon'
__version__ = '1.0.0'
__date__ = '2023/07/14 (Created: 2023/06/02 )'


import unittest
from unittest.mock import MagicMock

from Controller.SpiroController import SpiroController
from bridge_pyjs.PygameBridge import pygame


class TestSpiroController(unittest.TestCase):

    def setUp(self) -> None:
        """スピロコントローラのテストの準備を行う"""
        self.a_spiro_controller = SpiroController(None, None, None)

    def test_init(self):
        """スピロコントローラのフィールドのテスト"""
        self.assertEqual(self.a_spiro_controller.a_spiro_model, None)
        self.assertEqual(self.a_spiro_controller.a_spiro_view, None)
        self.assertEqual(self.a_spiro_controller.a_context_menu_model, None)
        self.assertEqual(self.a_spiro_controller.a_last_mouse_pos, (0, 0))
        self.assertEqual(self.a_spiro_controller.a_mouse_clicked, False)
        self.assertEqual(self.a_spiro_controller.spur_picking_type, None)
        self.assertEqual(self.a_spiro_controller.pinion_picking_type, None)
        self.assertEqual(self.a_spiro_controller.is_spur_selected_picking, False)
        self.assertEqual(self.a_spiro_controller.is_pinion_selected_picking, False)
        self.assertEqual(self.a_spiro_controller.is_pen_selected_picking, False)
        self.assertEqual(self.a_spiro_controller.mouse_shape, False)

    def test_routing_left_mouse_button_down(self):
        """マウスの左ボタンが押された時のルーティングのテスト。"""
        mock = MagicMock()
        self.a_spiro_controller.left_mouse_button_down_event = mock
        a_left_button_down = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (0, 0)})
        self.a_spiro_controller.events_router(a_left_button_down)
        mock.assert_called_once()

    def test_routing_left_mouse_button_up(self):
        """マウスの左ボタンが離された時のルーティングのテスト。"""
        mock = MagicMock()
        self.a_spiro_controller.left_mouse_button_up_event = mock
        a_left_button_up = pygame.event.Event(pygame.MOUSEBUTTONUP, {"button": 1, "pos": (0, 0)})
        self.a_spiro_controller.events_router(a_left_button_up)
        mock.assert_called_once()

    def test_routing_right_mouse_button_down(self):
        """マウスの右ボタンが押された時のルーティングのテスト"""
        mock = MagicMock()
        self.a_spiro_controller.right_mouse_button_down_event = mock
        a_right_button_down = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 3})
        self.a_spiro_controller.events_router(a_right_button_down)
        mock.assert_called_once()

    def test_routing_mouse_drag_event(self):
        """マウスがドラッグされた時のルーティングのテスト"""
        button_down_event_mock = MagicMock()
        motion_event_mock = MagicMock()
        drag_event_mock = MagicMock()

        self.a_spiro_controller.left_mouse_button_down_event = button_down_event_mock
        self.a_spiro_controller.mouse_motion_event = motion_event_mock
        self.a_spiro_controller.mouse_drag_event = drag_event_mock

        a_left_button_down = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (0, 0)})
        a_mouse_motion = pygame.event.Event(pygame.MOUSEMOTION, {"pos": (0, 0)})

        self.a_spiro_controller.events_router(a_left_button_down)
        self.a_spiro_controller.events_router(a_mouse_motion)

        button_down_event_mock.assert_called_once()
        motion_event_mock.assert_called_once()
        drag_event_mock.assert_called_once()

    def test_routing_mouse_motion_event(self):
        """マウスが移動した時のルーティングのテスト"""
        mock = MagicMock()
        self.a_spiro_controller.mouse_motion_event = mock
        a_mouse_motion = pygame.event.Event(pygame.MOUSEMOTION, {"pos": (0, 0)})
        self.a_spiro_controller.events_router(a_mouse_motion)
        mock.assert_called_once()

    def test_events_router(self):
        """イベントルーティングのテスト"""
        mock_right_buttown = MagicMock()
        mock_event_router = MagicMock()
        self.a_spiro_controller.right_mouse_button_down_event = mock_right_buttown
        self.a_spiro_controller.events_router = mock_event_router
        a_right_button_down = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 3})
        self.a_spiro_controller.events_router(a_right_button_down)
        mock_event_router.assert_called_once()

    def test_events_process(self):
        """イベントプロセスのテスト"""
        mock_event_process = MagicMock()
        self.a_spiro_controller.events_process = mock_event_process
        self.a_spiro_controller.events_process()
        mock_event_process.assert_called_once()


if __name__ == '__main__':
    unittest.main()
