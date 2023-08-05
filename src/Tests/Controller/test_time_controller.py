#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Dragon'
__version__ = '1.0.0'
__date__ = '2023/07/14 (Created: 2023/07/09 )'


import unittest
from unittest.mock import MagicMock

from Model.SpiroModel import SpiroModel
from View.SpiroView import SpiroView
from Controller.SpiroController import SpiroController
from Controller.TimeController import TimeController


class TestTimeContoroller(unittest.TestCase):

    def setUp(self) -> None:
        """タイムコントローラのテストの準備を行う"""
        self.a_time_controller = TimeController(SpiroController, SpiroModel, SpiroView)

    def test_init(self):
        """タイムコントローラのフィールドのテスト"""
        self.assertEqual(self.a_time_controller.a_spiro_controller, SpiroController)
        self.assertEqual(self.a_time_controller.a_spiro_model, SpiroModel)
        self.assertEqual(self.a_time_controller.a_spiro_view, SpiroView)

    def test_task(self):
        """タスクのテスト"""
        mock_task = MagicMock()
        self.a_time_controller.task = mock_task
        self.a_time_controller.task()
        mock_task.assert_called_once()

    def test_start_main_loop(self):
        """メインループのテスト"""
        mock_start_main_loop = MagicMock()
        self.a_time_controller.start_main_loop = mock_start_main_loop
        self.a_time_controller.start_main_loop()
        mock_start_main_loop.assert_called_once()
