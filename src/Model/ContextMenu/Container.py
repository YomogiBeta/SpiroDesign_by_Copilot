#!/usr/bin/env python
# -*- coding: utf-8 -*-

from View.UiView import UiView
from bridge_pyjs.PygameBridge import pygame


__author__ = 'Yomogiβ'
__version__ = '1.0.1'
__date__ = '2023/05/19 (Created: 2023/05/01 )'


class Container:
    """UIのベースとなるコンテナです。"""

    def __init__(self, ui_view: UiView, radius=0, shadow=False) -> None:
        """コンテナの初期化処理を行います。

        Args:
            ui_view (UiView):
                コンテナを描画するためのViewオブジェクト
            radius (int | optional):
                コンテナの角の丸みの半径
            shadow (bool | optional):
                コンテナに影をつけるかどうか
        """
        self.a_ui_view = ui_view
        self.radius = radius
        self.shadow = shadow

        self.shadow1: pygame.Rect = None
        self.shadow2: pygame.Rect = None
        self.shadow3: pygame.Rect = None
        self.shadow4: pygame.Rect = None

        self.rect: pygame.Rect = None

        self.rendered = False

    def render(self, x: int, y: int, width: int, height: int, color: tuple[int, int, int]) -> None:
        """コンテナの描画をリクエストします。

        Args:
            x (int):
                コンテナの左上のx座標
            y (int):
                コンテナの左上のy座標
            width (int):
                コンテナの幅
            height (int):
                コンテナの高さ
            color (tuple[int, int, int]):
                コンテナの色
        """
        if self.shadow:
            self.shadow1, self.shadow2, self.shadow3, self.shadow4 = self.a_ui_view.draw_shadow(x, y, width, height, self.radius)

        self.rect = self.a_ui_view.draw_square(x, y, width, height, color, self.radius)

        self.rendered = True

    def remove(self) -> None:
        """コンテナの描画を削除します。"""
        if self.shadow:
            self.a_ui_view.clear_rect(self.shadow1)
        self.a_ui_view.clear_rect(self.rect)
        self.rendered = False

    def is_rendered(self) -> bool:
        """コンテナが描画されているかどうかを返します。

        Returns:
            コンテナが描画状態である場合はTrue。そうでない場合はFalse。
        """
        return self.rendered

    def get_rect(self) -> pygame.Rect:
        """コンテナのRectオブジェクトを返します。

        Returns:
            コンテナのRectオブジェクト
        """
        return self.rect

    def get_radius(self) -> int:
        """コンテナの角の丸みの半径を返します。

        Returns:
            コンテナの角の丸みの半径の数値
        """
        return self.radius
