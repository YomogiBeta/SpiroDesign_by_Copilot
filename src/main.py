#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Yomogiβ'
__version__ = '1.1.2'
__date__ = '2023/07/04 (Created: 2023/06/16 )'

from Constants import DISPLAY_WIDTH, DISPLAY_HEIGHT
from Controller.SpiroController import SpiroController
from Controller.TimeController import TimeController
from Model.ContextMenu.ContextMenu import ContextMenu
from Model.SpiroModel import SpiroModel
from View.SpiroView import SpiroView
from View.UiView import UiView
from bridge_pyjs import ui_call
from bridge_pyjs.PygameBridge import pygame, set_icon


def create_menu(context_menu: ContextMenu, spiro_model: SpiroModel, root) -> list:
    """コンテキストメニューを作成する

    Args:
        context_menu (ContextMenu):
            コンテキストメニュー
        spiro_model (SpiroModel):
            スピロモデル
        time_controller (TimeController):
            時間制御のコントローラー

    Returns:
        list[dict[str, Callable]]:
            コンテキストメニューのリスト
    """
    def start():
        spiro_model.start_animation()
        context_menu.disable_item("start")
        context_menu.enable_item("stop")
        context_menu.enable_item("speed_up")
        context_menu.enable_item("speed_down")

        context_menu.disable_item("color")
        context_menu.disable_item("nib")
        context_menu.disable_item("rainbow")
        context_menu.disable_item("dive")
        context_menu.disable_item("new")
        context_menu.disable_item("open")
        context_menu.disable_item("save")
        context_menu.disable_item("circumscribe")
        context_menu.disable_item("inscribe")

    def stop():
        spiro_model.stop_animation()
        context_menu.disable_item("stop")
        context_menu.enable_item("start")
        context_menu.disable_item("speed_up")
        context_menu.disable_item("speed_down")

        context_menu.enable_item("color")
        context_menu.enable_item("rainbow")
        context_menu.enable_item("dive")
        context_menu.enable_item("new")
        context_menu.enable_item("open")
        context_menu.enable_item("save")

    def dive():
        spiro_model.dive()
        context_menu.enable_item("circumscribe")
        context_menu.enable_item("inscribe")
        context_menu.enable_item("nib")

    def switch_rainbow():
        if spiro_model.rainbow():
            spiro_model.stop_rainbow()
        else:
            spiro_model.start_rainbow()

    def set_nib():
        def set_nib(nib: float):
            if nib is not None:
                spiro_model.set_pen_nib(nib)
        ui_call.askvalue(root, set_nib, spiro_model.pinion_gear().pen().width)

    def select_color():
        animationed = spiro_model.animation()
        if animationed:
            spiro_model.stop_animation()

        def set_color(color: tuple[int, int, int]):
            if color is not None:
                spiro_model.set_pen_color(color)
                spiro_model.stop_rainbow()
            if animationed:
                spiro_model.start_animation()

        ui_call.askcolorcode(set_color)

    def reset_spiro_model():
        result = ui_call.askquestion("保存していない画面は復元できません。新しく作り直しますか？")
        if result:
            spiro_model.state_init()

    return [
        {
            "start": start,
            "stop": stop
        },
        {
            "current_clear": spiro_model.current_clear,
            "clear": spiro_model.clear
        },
        {
            "speed_up": spiro_model.speed_up,
            "speed_down": spiro_model.speed_down
        },
        {
            "color": select_color,
            "rainbow": switch_rainbow,
            "nib": set_nib,
        },
        {
            "circumscribe": spiro_model.start_circumscribe,
            "inscribe": spiro_model.stop_circumscribe
        },
        {
            "dive": dive
        },
        {
            "new": reset_spiro_model,
            "open": spiro_model.open_file,
            "save": spiro_model.save_file
        }
    ]


if __name__ in ('__main__', 'spirodesign__main__', 'SpiroDesign__main__'):
    # UIコールの初期化
    root = ui_call.init()

    # Pygameの初期化
    pygame.init()
    pygame.display.set_caption("SpiroDesign by Copilot (StandAlone)")

    # ディスプレイの作成
    screen_surface = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA | pygame.DOUBLEBUF)
    ui_surface = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)

    # iconをpygameアイコンから変更
    set_icon("resource/spirodesign.png")

    # Viewの作成
    spiro_view = SpiroView(screen_surface, ui_surface)
    ui_view = UiView(ui_surface)

    # Modelの作成
    spiro_model = SpiroModel(spiro_view)
    context_model = ContextMenu(ui_view)

    # ViewにSpiroModelを設定
    spiro_view.set_spiro_model(spiro_model)

    # Controllerを作成
    spiro_controller = SpiroController(spiro_model, spiro_view, context_model)
    time_controller = TimeController(spiro_controller, spiro_model, spiro_view)

    # コンテキストメニューの設定
    menu = create_menu(context_model, spiro_model, root)
    context_model.set_menu(menu)

    # メインループの開始
    time_controller.start_main_loop()
