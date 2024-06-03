#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Model.ContextMenu.ButtonBase import ButtonBase
from Model.ContextMenu.Container import Container
from View.UiView import UiView
from bridge_pyjs.PygameBridge import pygame, get_font
from Constants import DISPLAY_WIDTH, DISPLAY_HEIGHT, FONT_NAME, FONT_SIZE, FONT_WEIGHT, CONTEXT_MENU_BACKGROUND_COLOR

__author__ = 'Yomogiβ'
__version__ = '2.0.0'
__date__ = '2023/06/16 (Created: 2023/05/01 )'

# web互換にするにあたってコンテキストメニューだけは独自にpygameにて実装しなければならないため、実装する。


class ContextMenu:
    """コンテキストメニュークラス

    pygame上でコンテキストメニューの機能を提供します。
    コンテキストのアイテムはset_menuメソッドで指定します。引数にはコンテキストを構成するListを渡します。リストの中身はコンテキストメニューの項目ラベルと、それに対応する関数の辞書型です。
    基本的にListに1つの辞書型を入れることで、辞書型内のキーをラベルとしたコンテキストが生成されます。
    グループごとに複数の辞書型を入れることで、グループごとにDividerを挟んだコンテキストが生成されます。

    Examples:
        >>> # 引数のmenuには以下のようなListを渡します。
        >>> # startとendを項目として持つコンテキストを生成する例
        >>> menu = [
        >>>     {
        >>>         "start": lambda: print("start"),
        >>>         "end": lambda: print("end"),
        >>>     }
        >>> ]

        >>> # startとend・say_helloとsay_byeを項目として持ち、endとsay_helloの間にDividerを挟んだコンテキストを生成する例
        >>> menu = [
        >>>     {
        >>>         "start": lambda: print("start"),
        >>>         "end": lambda: print("end"),
        >>>     },
        >>>     {
        >>>         "say_hello": lambda: print("hello"),
        >>>         "say_bye": lambda: print("bye"),
        >>>     }
        >>> ]

    """

    MIN_WIDTH = 120
    WIDTH_PADDING = 10
    HEIGHT_PADDING = 20

    def __init__(self, ui_view: UiView) -> None:
        """コンテキストメニューの初期化処理を行う

        Args:
            ui_view (UiView):
                UiViewのインスタンス
            menu (list[dict[str, Callable]]):
                コンテキストメニューの項目を表す辞書のリスト
        """
        self.a_ui_view = ui_view
        self.open_menu_state = False
        self.draw_menu_pos = (0, 0)
        self.container = Container(ui_view, 8, True)

        self.context_items: list[ButtonBase | None] = []

        self.focus_index = -1
        self.before_focus_button = None

    def set_menu(self, menu: list) -> None:
        """コンテキストメニューの項目を設定する

        Args:
            menu (list[dict[str, Callable]]):
                コンテキストメニューの項目を表す辞書のリスト
        """

        # Javascriptの文字列に対するmaxメソッドの振る舞いが異なるため、forを使用した実装に変更
        a_max_length = -1
        max_key_text = ""
        for dic_items in menu:
            for key in dic_items.keys():
                if a_max_length < len(key):
                    a_max_length = len(key)
                    max_key_text = key

        # max_key_text = max((key for dic_items in menu for key in dic_items.keys()), key=len)

        width, _ = get_font(FONT_NAME, FONT_SIZE, FONT_WEIGHT).size(max_key_text)
        self.max_width = max(width + self.WIDTH_PADDING, self.MIN_WIDTH)
        self.max_height = sum(len(dic_items) for dic_items in menu) * self.HEIGHT_PADDING + (len(menu) * 5) + 30

        for dic_items in menu:
            for key, callback in dic_items.items():
                self.context_items.append(ButtonBase(self.a_ui_view, key, callback))
            self.context_items.append(None)

        self.context_items = self.context_items[:-1]  # 最後のNoneを削除(最後にDividerを描画しないため)

    def open_render(self, x: int, y: int) -> None:
        """コンテキストメニューを描画を各パーツにリクエストする

        Args:
            x (int):
                描画するx座標
            y (int):
                描画するy座標
        """

        if DISPLAY_WIDTH - x < self.max_width:
            x -= self.max_width

        if DISPLAY_HEIGHT - y < self.max_height:
            y -= self.max_height

        self.container.render(x, y, self.max_width, self.max_height, CONTEXT_MENU_BACKGROUND_COLOR)
        for item in self.context_items:
            if item is not None:
                item.render(x, y + 3, self.max_width, self.HEIGHT_PADDING)
                y += self.HEIGHT_PADDING + 3
            else:
                self.a_ui_view.draw_divider(x, y + 3, self.max_width)
                y += 3

    def close_render(self) -> None:
        """コンテキストメニューの描画削除を各パーツにリクエストする"""
        if self.container.is_rendered():

            self.container.remove()
            for item in self.context_items:
                if item is not None:
                    item.set_rect(None)

    def open_menu(self, event: pygame.event.Event) -> None:
        """コンテキストメニューを開く

        Args:
            event (pygame.event.Event):
                pygameのイベントオブジェクト
        """
        # Mouse right down
        self.close_render()

        self.open_menu_state = True
        self.draw_menu_pos = event.pos

        self.open_render(*event.pos)

    def close_menu(self) -> None:
        """コンテキストメニューを閉じる"""
        # Mouse left down
        self.focus_index = -1
        if self.before_focus_button is not None:
            self.before_focus_button.un_focus()

        self.before_focus_button = None

        if self.open_menu_state:
            self.open_menu_state = False
            self.close_render()

    def disable_item(self, key: str) -> None:
        """コンテキストメニューのボタンを押下不可モードにする

        Args:
            key (str):
                押下不可にするボタンのラベル
        """
        for button in self.context_items:
            if button is not None and button.text() == key:
                button.disable()
                return

    def enable_item(self, key: str) -> None:
        """コンテキストメニューのボタンを押下可能モードにする

        Args:
            key (str):
                押下可能にするボタンのラベル
        """
        for button in self.context_items:
            if button is not None and button.text() == key:
                button.enable()
                return

    def has_buttons_downed(self, event: pygame.event.Event) -> None:
        """イベントよりコンテキストメニューのボタンにマウスダウンイベントが発生したかどうか判定するc

        Args:
            event (pygame.event.Event):
                pygameのイベントオブジェクト
        """
        # Mouse left down
        for item in self.context_items:
            if item is not None:
                item.check_down_me(event)

    def has_buttons_clicked(self, event: pygame.event.Event) -> None:
        """イベントよりコンテキストメニューのボタンがクリックされたかを判定する

        Args:
            event (pygame.event.Event):
                pygameのイベントオブジェクト
        """
        # Mouse left down
        for item in self.context_items:
            if item is not None:
                item.check_click_me(event)

    def has_buttons_hovered(self, event: pygame.event.Event) -> None:
        """イベントよりコンテキストメニューのボタンがホバーされたかを判定する

        Args:
            event (pygame.event.Event):
                pygameのイベントオブジェクト
        """
        # Mouse motion
        for item in self.context_items:
            if item is not None:
                item.check_hover_me(event)

    def has_focused_button_enter(self) -> None:
        """エンターが押された時にフォーカスされたボタンをクリックする"""
        if not self.open_menu_state:
            return

        if self.before_focus_button is not None:
            self.before_focus_button.click()

        self.close_menu()

    def _check_button_item_enable(self, index: int) -> bool:
        """ボタンが有効かどうかを判定する

        Args:
            index (int):
                ボタンのインデックス

        Returns:
            bool: ボタンが有効かどうか
        """

        if self.context_items[index] is not None:
            return self.context_items[index].enable_status()
        return False

    def next_button_focus(self) -> None:
        """次のボタンにフォーカスを当てる"""
        if not self.open_menu_state:
            return

        if self.focus_index + 1 < len(self.context_items):
            a_cache_index = self.focus_index
            self.focus_index += 1

            if not self._check_button_item_enable(self.focus_index):
                while not self._check_button_item_enable(self.focus_index):
                    self.focus_index += 1

                    if self.focus_index >= len(self.context_items):
                        self.focus_index = a_cache_index
                        return

            if self.before_focus_button is not None:
                self.before_focus_button.un_focus()

            self.context_items[self.focus_index].focus()
            self.before_focus_button = self.context_items[self.focus_index]

    def prev_button_focus(self) -> None:
        """前のボタンにフォーカスを当てる"""
        if not self.open_menu_state:
            return

        if self.focus_index >= -1:
            a_cache_index = self.focus_index

            if self.focus_index <= 0:
                self.focus_index = 0
            else:
                self.focus_index -= 1

            if not self._check_button_item_enable(self.focus_index):
                while not self._check_button_item_enable(self.focus_index):
                    self.focus_index -= 1

                    if self.focus_index < 0:
                        self.focus_index = a_cache_index
                        return

            if self.before_focus_button is not None:
                self.before_focus_button.un_focus()

            self.context_items[self.focus_index].focus()
            self.before_focus_button = self.context_items[self.focus_index]
