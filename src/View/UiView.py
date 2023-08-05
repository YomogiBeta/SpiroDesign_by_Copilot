#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bridge_pyjs.PygameBridge import pygame, clear_draw_rect, clear_draw_surface, get_font
from Constants import CONTEXT_MENU_DIVIDER_COLOR, FONT_NAME, FONT_SIZE, FONT_WEIGHT

__author__ = 'Yomogiβ'
__version__ = '2.0.0'
__date__ = '2023/06/16 (Created: 2023/05/01 )'


class UiView:
    """UIを描画するクラスです。"""

    def __init__(self, ui_surface: pygame.Surface) -> None:
        """UIビューの初期化処理を行う"""
        self.a_ui_surface = ui_surface

    def draw_square(self, x: int, y: int, width: int, height: int, color: tuple[int, int, int], radius=0) -> pygame.Rect:
        """四角形を描画します

        Args:
            x (int):
                四角形の左上のx座標
            y (int):
                四角形の左上のy座標
            width (int):
                四角形の幅
            height (int):
                四角形の高さ
            color (tuple[int, int, int]):
                四角形の色
            radius (int, optional):
                四角形の角の丸みの半径

        Returns:
            描画した四角形のRectオブジェクト
        """
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.a_ui_surface, color, rect, 0, radius)
        return rect

    def draw_shadow(self, x: int, y: int, width: int, height: int, radius=0):
        """特定の座標に四角形の影を描画します

        Args:
            x (int):
                四角形の左上のx座標
            y (int):
                四角形の左上のy座標
            width (int):
                四角形の幅
            height (int):
                四角形の高さ
            radius (int, optional):
                四角形の角の丸みの半径

        Returns:
            描画した影のRectオブジェクト(4つ)
        """
        shadow1 = self.draw_square(
            x - 6, y - 6, width + 11, height + 11, (217, 213, 218, 60), radius)
        shadow2 = self.draw_square(
            x - 4, y - 4, width + 7, height + 7, (217, 213, 218, 130), radius)
        shadow3 = self.draw_square(
            x - 2, y - 2, width + 4, height + 4, (217, 213, 218, 225), radius)
        shadow4 = self.draw_square(
            x - 1, y - 1, width + 2, height + 2, (217, 213, 218, 255), radius)
        return shadow1, shadow2, shadow3, shadow4

    def draw_text(self, x: int, y: int, text: str, color: tuple[int, int, int]) -> None:
        """テキストを描画します

        Args:
            x (int):
                テキストの左上のx座標
            y (int):
                テキストの左上のy座標
            text (str):
                テキストの内容
            color (tuple[int, int, int]):
                テキストの色
        """
        font = get_font(FONT_NAME, FONT_SIZE, FONT_WEIGHT)
        font_surface = font.render(text, True, color)
        self.a_ui_surface.blit(font_surface, (x, y))

    def draw_divider(self, x: int, y: int, width: int) -> None:
        """区切り線を描画します

        Args:
            x (int):
                区切り線の左上のx座標
            y (int):
                区切り線の左上のy座標
            width (int):
                区切り線の幅
        """
        pygame.draw.line(self.a_ui_surface, CONTEXT_MENU_DIVIDER_COLOR, (x, y), (x + width, y), 1)

    def clear_rect(self, rect: pygame.Rect) -> None:
        """UIレイヤーから指定した範囲をクリアします

        Args:
            rect (pygame.Rect):
                クリアする範囲のRect
        """
        clear_draw_rect(self.a_ui_surface, rect)

    def clear_ui_draw(self) -> None:
        """UIレイヤーをクリアします"""
        clear_draw_surface(self.a_ui_surface)

    def ui_surface(self) -> pygame.Surface:
        """UIレイヤーを返します

        Returns:
            UIレイヤーのSurfaceオブジェクト
        """
        return self.a_ui_surface
