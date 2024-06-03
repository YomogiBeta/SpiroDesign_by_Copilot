#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Model.ContextMenu.Container import Container
from Model.ContextMenu.ClickAble import ClickAble
from Constants import CONTEXT_MENU_BACKGROUND_COLOR, CONTEXT_MENU_HOVERD_BACKGROUND_COLOR
from Constants import CONTEXT_MENU_ON_BACKGROUND_COLOR, CONTEXT_MENU_ON_DISABLE_BACKGROUND_COLOR
from View.UiView import UiView


__author__ = 'Yomogiβ'
__version__ = '1.0.3'
__date__ = '2023/07/08 (Created: 2023/05/01 )'


class ButtonBase(ClickAble):
    """ボタンのクラスです。"""

    def __init__(self, ui_view: UiView, text: str, callback) -> None:
        """ボタンに関する情報の初期化を行います

        Args:
            ui_view (UiView):
                ボタンを描画するためのViewオブジェクト
            text (str):
                ボタンに表示するテキスト
            callback (Callable):
                ボタンがクリックされた時に呼び出される関数
        """
        super().__init__()
        self.a_ui_view = ui_view
        self.container = Container(ui_view, 4)
        self.a_enable = True
        self.a_text = text
        self.callback = callback
        self.background_color = CONTEXT_MENU_BACKGROUND_COLOR

    def render(self, x: int, y: int, width: int, height: int) -> None:
        """ボタンを描画を呼び出します。

        Args:
            x (int):
                ボタンのx座標
            y (int):
                ボタンのy座標
            width (int):
                ボタンの幅
            height (int):
                ボタンの高さ
            radius (int):
                ボタンの角の丸みの半径
        """
        self.container.render(x, y, width, height, self.background_color)
        self.set_rect(self.container.get_rect())
        text_color = CONTEXT_MENU_ON_BACKGROUND_COLOR if self.a_enable else CONTEXT_MENU_ON_DISABLE_BACKGROUND_COLOR
        self.a_ui_view.draw_text(x + 10, y + 1, self.a_text, text_color)

    def disable(self) -> None:
        """ボタンを無効化します。"""
        self.a_enable = False

    def enable(self) -> None:
        """ボタンを有効化します。"""
        self.a_enable = True

    def enable_status(self) -> bool:
        """ボタンが有効かどうかを取得します。

        Returns:
            bool: ボタンが有効かどうか
        """
        return self.a_enable

    def text(self) -> str:
        """ボタンのテキストを取得します。

        Returns:
            str: ボタンのテキスト
        """
        return self.a_text

    def hover_in(self) -> None:
        self.focus()

    def hover_out(self) -> None:
        self.un_focus()

    def focus(self) -> None:
        """ボタンにフォーカスを当てます。"""
        if self.a_enable:
            rect = self.container.get_rect()

            if self.container.is_rendered():
                self.container.remove()

            self.background_color = CONTEXT_MENU_HOVERD_BACKGROUND_COLOR
            self.render(rect.x, rect.y, rect.width, rect.height)

    def un_focus(self) -> None:
        """ボタンのフォーカスを外します。"""
        rect = self.container.get_rect()

        if self.container.is_rendered():
            self.container.remove()

        self.background_color = CONTEXT_MENU_BACKGROUND_COLOR
        self.render(rect.x, rect.y, rect.width, rect.height)

    def click(self) -> None:
        if self.a_enable:
            self.callback()
