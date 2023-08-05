#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Constants import SPUR_GEAR_COLOR, PINION_GEAR_COLOR, GEAR_LINE_COLOR, BACKGROUND_COLOR
from Constants import PEN_HOLE, CIRCLE_PICKING_RADIUS
from Model.PinionGear import PinionGear
from Model.SpiroGear import SpiroGear
from Model.SpurGear import SpurGear
from bridge_pyjs.PygameBridge import pygame
# from Model.SpiroModel import SpiroModel

__author__ = 'Yomogiβ'
__version__ = '2.0.2'
__date__ = '2023/07/06 (Created: 2023/05/01 )'


class SpiroView:
    """スピロビューのクラスです"""

    def __init__(self, screen: pygame.Surface, ui_surface: pygame.Surface) -> None:
        """スピロビューの初期化処理を行う

        Args:
            screen (pygame.Surface):
                スクリーン
            ui_surface (pygame.Surface):
                UIサーフェス
        """
        self.a_screen = screen
        self.a_ui_surface = ui_surface

    def set_spiro_model(self, spiro_model) -> None:
        """スピロモデルを設定する

        Args:
            spiro_model (SpiroModel):
                スピロプログラムのモデル
        """
        self.a_spiro_model = spiro_model
        spiro_model.draw_frame()

    def draw_spur_gear(self) -> None:
        """スーパーギアを描画する"""

        a_draw_surface = self.a_spiro_model.gear_surface()
        a_spur_gear: SpurGear = self.a_spiro_model.spur_gear()

        self.draw_gear_base(a_draw_surface, a_spur_gear, SPUR_GEAR_COLOR)

    def draw_pinion_gear(self) -> None:
        """ピニオンギアを描画する"""
        a_draw_surface = self.a_spiro_model.gear_surface()
        a_pinion_gear: PinionGear = self.a_spiro_model.pinion_gear()

        pygame.draw.aaline(a_draw_surface, GEAR_LINE_COLOR, a_pinion_gear.top_rect().center, a_pinion_gear.bottom_rect().center)
        pygame.draw.aaline(a_draw_surface, GEAR_LINE_COLOR, a_pinion_gear.left_rect().center, a_pinion_gear.right_rect().center)

        self.draw_gear_base(a_draw_surface, a_pinion_gear, PINION_GEAR_COLOR)

    def draw_gear_base(self, surface: pygame.Surface, gear: SpiroGear, color: tuple[int, int, int]) -> None:
        """ギアの基本部分を描画する

        Args:
            surface (pygame.Surface):
                描画するサーフェス
            gear (SpiroGear):
                描画するギア
            color (tuple[int, int, int]):
                描画するギアの色
        """
        pygame.draw.circle(surface, color, gear.center(), gear.radius(), 2)

        pygame.draw.circle(surface, BACKGROUND_COLOR, gear.top_rect().center, CIRCLE_PICKING_RADIUS)
        pygame.draw.circle(surface, color, gear.top_rect().center, CIRCLE_PICKING_RADIUS, 2)

        pygame.draw.circle(surface, BACKGROUND_COLOR, gear.bottom_rect().center, CIRCLE_PICKING_RADIUS)
        pygame.draw.circle(surface, color, gear.bottom_rect().center, CIRCLE_PICKING_RADIUS, 2)

        pygame.draw.circle(surface, BACKGROUND_COLOR, gear.left_rect().center, CIRCLE_PICKING_RADIUS)
        pygame.draw.circle(surface, color, gear.left_rect().center, CIRCLE_PICKING_RADIUS, 2)

        pygame.draw.circle(surface, BACKGROUND_COLOR, gear.right_rect().center, CIRCLE_PICKING_RADIUS)
        pygame.draw.circle(surface, color, gear.right_rect().center, CIRCLE_PICKING_RADIUS, 2)

        pygame.draw.circle(surface, BACKGROUND_COLOR, gear.center(), CIRCLE_PICKING_RADIUS)
        pygame.draw.circle(surface, color, gear.center(), CIRCLE_PICKING_RADIUS, 2)

    def draw_gear_connection_line(self) -> None:
        """スーパーギアとピニオンギアの中心を線で結ぶ"""
        a_draw_surface = self.a_spiro_model.gear_surface()
        a_spur_gear: SpurGear = self.a_spiro_model.spur_gear()
        a_pinion_gear: PinionGear = self.a_spiro_model.pinion_gear()

        pygame.draw.aaline(a_draw_surface, (0, 0, 0), a_spur_gear.center(), a_pinion_gear.center())

    def draw_pen(self) -> None:
        """ペンを描画する"""
        a_draw_surface = self.a_spiro_model.gear_surface()
        a_pinion_gear: PinionGear = self.a_spiro_model.pinion_gear()
        a_pen_pos = a_pinion_gear.pen().center
        a_pen_nib = a_pinion_gear.pen().width / 2
        a_pen_color = a_pinion_gear.pen_color()

        pygame.draw.circle(a_draw_surface, a_pen_color, a_pen_pos, a_pen_nib)
        pygame.draw.circle(a_draw_surface, PINION_GEAR_COLOR, a_pen_pos, a_pen_nib + PEN_HOLE, 2)

    def draw_pen_pos(self, points: list) -> None:
        """ペンの位置を軌跡として描画する"""
        a_draw_surface = self.a_spiro_model.active_surface()
        if a_draw_surface is not None:
            a_active_surface_pos_x, a_active_surface_pos_y = self.a_spiro_model.active_surface_pos()
            a_pinion_gear: PinionGear = self.a_spiro_model.pinion_gear()
            a_pen_color = a_pinion_gear.pen_color()
            a_pen_nib = a_pinion_gear.pen().width / 2

            for point in points:
                x, y = point

                a_path_pos = (x - a_active_surface_pos_x, y - a_active_surface_pos_y)
                pygame.draw.circle(a_draw_surface, a_pen_color, a_path_pos, a_pen_nib)

    def commit(self) -> None:
        """描画を確定する

        一番下のレイヤーがmain_board_surface
        その一つ上のレイヤーがactive_surface
        さらにその上のレイヤーがgear_surface
        一番上のレイヤーがui_surface

        この順番でscreenにレイヤーを反映していき、最後に画面更新をpygameに指示する。
        """
        self.a_screen.fill((233, 233, 233))

        a_blits_list = []

        a_blits_list.append((self.a_spiro_model.main_board_surface(),
                            self.a_spiro_model.main_board_surface_pos()))

        active_x, active_y = self.a_spiro_model.active_surface_pos()
        main_x, main_y = self.a_spiro_model.main_board_surface_pos()

        if self.a_spiro_model.active_surface() is not None:
            a_blits_list.append((self.a_spiro_model.active_surface(),
                                (active_x + main_x, active_y + main_y)))

        a_blits_list.append((self.a_spiro_model.gear_surface(),
                            self.a_spiro_model.main_board_surface_pos()))

        a_blits_list.append((self.a_ui_surface, (0, 0)))

        self.a_screen.blits(a_blits_list, False)
        pygame.display.update(self.a_screen.get_rect())
