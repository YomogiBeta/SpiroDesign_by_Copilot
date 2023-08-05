#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Model.SpiroModel import SpiroModel
from Model.ContextMenu.ContextMenu import ContextMenu
from View.SpiroView import SpiroView
from bridge_pyjs.PygameBridge import pygame, cross_hair_mouse_mode, normal_mouse_mode
from bridge_pyjs.ExitBridge import bridge_exit

__author__ = 'SHIRO'
__version__ = '1.2.1'
__date__ = '2023/07/09 (Created: 2023/5/19)'


class SpiroController:
    """スピロプログラムのコントローラクラス

    スピロプログラムのコントローラクラスです。スピロプログラムに関わるイベント処理を行います。
    """

    def __init__(self, spiro_model: SpiroModel, spiro_view: SpiroView, context_menu: ContextMenu) -> None:
        """スピロプログラムコントローラの初期化処理を行う

        Args:
            spiro_model (SpiroModel):
                スピロモデル
            spiro_view (SpiroView):
                スピロビュー
            context_menu (ContextMenu):
                コンテキストメニュー
        """
        self.a_spiro_model = spiro_model
        self.a_context_menu_model = context_menu
        self.a_last_mouse_pos = (0, 0)
        self.a_spiro_view = spiro_view
        self.a_mouse_clicked = False

        self.spur_picking_type = None
        self.pinion_picking_type = None
        self.is_spur_selected_picking = False
        self.is_pinion_selected_picking = False
        self.is_pen_selected_picking = False

        self.mouse_shape = False

    def left_mouse_button_down_event(self, event: pygame.event.Event) -> None:
        """マウスの左ボタンが押された時の処理を行う.

        Args:
            event (pygame.event.Event):
                pygameのイベントオブジェクト
        """
        if self.a_spiro_model.check_dive():
            self._gear_controller(event, 0, 0)
        self.a_context_menu_model.has_buttons_downed(event)

    def left_mouse_button_up_event(self, event: pygame.event.Event) -> None:
        """マウスの左ボタンが離された時の処理を行う

        Args:
            event (pygame.event.Event):
                pygameのイベントオブジェクト
        """
        self.a_context_menu_model.has_buttons_clicked(event)
        self.a_context_menu_model.close_menu()

    def right_mouse_button_down_event(self, event: pygame.event.Event) -> None:
        """マウスの右ボタンが押された時の処理を行う.

        Args:
            event (pygame.event.Event):
                pygameのイベントオブジェクト
        """
        self.a_context_menu_model.open_menu(event)

    def _check_controll(self) -> bool:
        """制御中のものが存在しないことを確認するメソッド"""
        return sum((self.spur_picking_type is not None,
                    self.pinion_picking_type is not None,
                    self.is_spur_selected_picking,
                    self.is_pinion_selected_picking,
                    self.is_pen_selected_picking)) == 0

    def _gear_controller(self, event: pygame.event.Event, dx: int, dy: int) -> None:
        """ドラッグ時のギアのコントロール

        Args:
            event (Event):
                pygameのイベントオブジェクト
            dx (int):
                x方向の移動量
            dy (int):
                y方向の移動量
        """

        x, y = event.pos
        main_board_x, main_board_y = self.a_spiro_model.main_board_surface_pos()
        x = x - main_board_x
        y = y - main_board_y

        spur_picking_type = self.a_spiro_model.check_picking_spur_wheel(x, y)
        picking_pinion_type = self.a_spiro_model.check_picking_pinion_wheel(x, y)

        if (self.a_spiro_model.check_pen_selected_wheel(x, y) and self._check_controll()) or self.is_pen_selected_picking:
            self.a_spiro_model.add_pen_pos(dx, dy)
            self.is_pen_selected_picking = True

        elif (picking_pinion_type is not None and self._check_controll()) or self.pinion_picking_type is not None:
            value = dx + dy
            if self.pinion_picking_type == "left":
                value = (-1 * dx) + dy
            elif self.pinion_picking_type == "top":
                value = dx + (-1 * dy)
            self.a_spiro_model.add_pinion_gear_radius(value)
            self.pinion_picking_type = picking_pinion_type if picking_pinion_type is not None else self.pinion_picking_type

        elif (self.a_spiro_model.check_spur_selected_wheel(x, y) and self._check_controll()) or self.is_spur_selected_picking:
            self.a_spiro_model.add_spur_gear_position(dx, dy)
            self.is_spur_selected_picking = True

        elif (self.a_spiro_model.check_pinion_selected_wheel(x, y) and self._check_controll()) or self.is_pinion_selected_picking:
            self.a_spiro_model.add_pinion_gear_position(dx, dy)
            self.is_pinion_selected_picking = True

        elif (spur_picking_type is not None and self._check_controll()) or self.spur_picking_type is not None:
            value = dx + dy
            if self.spur_picking_type == "left":
                value = (-1 * dx) + dy
            elif self.spur_picking_type == "top":
                value = dx + (-1 * dy)
            self.a_spiro_model.add_spur_gear_radius(value)
            self.spur_picking_type = spur_picking_type if spur_picking_type is not None else self.spur_picking_type

    def mouse_drag_event(self, event: pygame.event.Event) -> None:
        """マウスのドラッグイベントの処理を行う.

        Args:
            event (pygame.event.Event):
                pygameのイベントオブジェクト
        """

        # スーパーギアの半径の可変
        before_x, before_y = self.a_last_mouse_pos
        event_x, event_y = event.pos
        dx, dy = event_x - before_x, event_y - before_y

        if self.a_spiro_model.check_dive():
            self._gear_controller(event, dx, dy)

        if self._check_controll():
            self.a_spiro_model.move_main_board_surface(dx, dy)

    def mouse_motion_event(self, event: pygame.event.Event) -> None:
        """マウスの移動イベントの処理を行う.

        Args:
            event (pygame.event.Event):
                pygameのイベントオブジェクト
        """
        x, y = event.pos
        main_board_x, main_board_y = self.a_spiro_model.main_board_surface_pos()
        x = x - main_board_x
        y = y - main_board_y

        spur_picking_bool = self.a_spiro_model.check_picking_spur_wheel(x, y) is not None
        picking_pinion_bool = self.a_spiro_model.check_picking_pinion_wheel(x, y) is not None

        self.a_context_menu_model.has_buttons_hovered(event)
        is_wheel = sum((spur_picking_bool,
                        picking_pinion_bool,
                        self.a_spiro_model.check_spur_selected_wheel(x, y),
                        self.a_spiro_model.check_pinion_selected_wheel(x, y),
                        self.a_spiro_model.check_pen_selected_wheel(x, y)))

        if (is_wheel >= 1 or not self._check_controll()) and self.a_spiro_model.check_dive():
            if not self.mouse_shape:
                cross_hair_mouse_mode()
                self.mouse_shape = True
        elif is_wheel == 0 and self._check_controll():
            if self.mouse_shape:
                normal_mouse_mode()
                self.mouse_shape = False

    def events_router(self, event: pygame.event.Event) -> None:
        """イベントのルーティングを行う

        Args:
            event (Event):
                pygameのイベントオブジェクト
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左ボタンが押されたらleft_mouse_button_down_event
                self.left_mouse_button_down_event(event)
                self.a_last_mouse_pos = event.pos
                self.a_mouse_clicked = True
            elif event.button == 3:  # 右ボタンが押されたらright_mouse_button_down_event
                self.right_mouse_button_down_event(event)
            return

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # 左ボタンが押されたらleft_mouse_button_up_event
                self.left_mouse_button_up_event(event)
            self.a_mouse_clicked = False

            self.spur_picking_type = None
            self.pinion_picking_type = None
            self.is_spur_selected_picking = False
            self.is_pinion_selected_picking = False
            self.is_pen_selected_picking = False

            return

        if event.type == pygame.MOUSEMOTION:
            self.mouse_motion_event(event)
            if self.a_mouse_clicked:
                self.mouse_drag_event(event)
            self.a_last_mouse_pos = event.pos
            return

        if event.type == pygame.QUIT:
            pygame.quit()
            bridge_exit()

    def events_process(self) -> None:
        """イベントのルーティングにイベント情報を受け渡す"""
        for event in pygame.event.get():
            self.events_router(event)
