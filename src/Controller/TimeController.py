#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Constants import FRAME_RATE
from Controller.SpiroController import SpiroController
from Model.SpiroModel import SpiroModel
from View.SpiroView import SpiroView
from bridge_pyjs.PygameBridge import pygame, set_callback


__author__ = 'Yomogiβ'
__version__ = '2.0.0'
__date__ = '2023/06/26 (Created: 2023/5/18)'


class TimeController:
    """フレーム処理を呼び出すクラスです。"""

    def __init__(self, spiro_controller: SpiroController, spiro_model: SpiroModel, spiro_view: SpiroView) -> None:
        """タイムコントローラーの初期化処理を行う

        Args:
            spiro_controller (SpiroController):
                スピロコントローラー
            spiro_model (SpiroModel):
                スピロモデル
            spiro_view (SpiroView):
                スピロビュー
        """
        self.a_spiro_controller = spiro_controller
        self.a_spiro_model = spiro_model
        self.a_spiro_view = spiro_view

    def task(self) -> None:
        """フレーム処理を呼び出す"""
        self.a_spiro_controller.events_process()
        self.a_spiro_model.run()
        self.a_spiro_view.commit()
        pygame.time.Clock().tick(FRAME_RATE)

    def start_main_loop(self):
        """メインループを開始する"""
        set_callback(self.task)
