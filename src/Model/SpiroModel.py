#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Constants import BACKGROUND_COLOR, BOARD_HEIGHT, BOARD_WIDTH
from Constants import INIT_PINION_GEAR_POSITION, INIT_SPUR_GEAR_POSITION, INIT_BOARD_POSITION
from Constants import INIT_SPUR_GEAR_RADIUS, INIT_PINION_GEAR_RADIUS
from Constants import MAX_SPEED, MIN_SPEED, SPEED_STEP, ACTIVE_SURFACE_PADDING, FIILE_NAME_FORMAT, SPILIT_POINT_NUM
from Model.PinionGear import PinionGear
from Model.SpurGear import SpurGear
from View.SpiroView import SpiroView
from bridge_pyjs.PygameBridge import pygame, clear_draw_surface, output_surface, make_surface
from bridge_pyjs.ParseIntBridge import parse_int
from Model.SpiroFileParser import SpiroFileParser
from bridge_pyjs.ui_call.ui_call import download_content, askopenfilecontent, messagebox
import utils
import math
import datetime

__author__ = 'Blue S, ARA T, Yomogiβ'
__version__ = '1.1.1'
__date__ = '2023/07/08 (Created: 2023/05/19)'


class SpiroModel:
    """
    スピロプログラムのモデルクラス

    スピロプログラムのモデルクラスです。スピロプログラムの実現に必要な機能を提供します。
    """

    def __init__(self, view: SpiroView) -> None:
        """スピロプログラムモデルの初期化処理を行う

        Args:
            view (SpiroView): スピロプログラムのビュー
        """
        self.a_spiro_view = view
        self.state_init()

    def state_init(self) -> None:
        """スピロモデルが動作するにおけるメンバ変数の初期化を行う"""
        self.a_spur_gear = SpurGear(*INIT_SPUR_GEAR_POSITION, INIT_SPUR_GEAR_RADIUS)
        self.a_pinion_gear = PinionGear(*INIT_PINION_GEAR_POSITION, INIT_PINION_GEAR_RADIUS)

        self.a_main_board_surface = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT), pygame.SRCALPHA)
        self.a_main_board_surface.fill(BACKGROUND_COLOR)
        self.a_main_board_surface_pos = INIT_BOARD_POSITION
        self.a_gear_surface = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT), pygame.SRCALPHA)

        self.an_active_surface = None
        self.an_active_surface_pos = (0, 0)

        self.is_animated = False
        self.is_rainbow = False
        self.is_dived = True
        self.is_circumscribe = False

        self._an_add_angle = MIN_SPEED

        self._reload_run_state = True
        self._move_angle = 0.0
        self._rotate_angle = 0.0
        self._a_pinion_to_spur_distance = 0.0

        self._a_points = []

    def run(self) -> None:
        """１フレームの計算処理を呼び出す"""
        if self.is_animated:
            # ダイブ済みの場合は、描画領域を確保し、ダイブ前にする。
            if self.is_dived:
                self.set_create_active_surface()
                self.is_dived = False

            # レインボーモードの場合は、ペンの色を虹色に遷移させる。
            if self.is_rainbow:
                self.pen_rainbow()

            spur_gear_center_x, spur_gear_center_y = self.a_spur_gear.center()
            pinion_gear_x, pinion_gear_y = self.a_pinion_gear.center()
            pinion_gear_radius = self.a_pinion_gear.radius()
            pen_radius = self.a_pinion_gear.pen().width / 2
            pen_to_pinion_distance = self.a_pinion_gear.pen_to_pinion_distance()
            pen_to_pinion_degrees = self.a_pinion_gear.pen_to_pinion_degrees()

            # 1フレームの計算に必要な初期化処理を行う。
            if self._reload_run_state:
                self._move_angle = utils.calculate_angle(spur_gear_center_x, spur_gear_center_y, pinion_gear_x, pinion_gear_y)
                self._rotate_angle = 0

                self._a_pinion_to_spur_distance = \
                    math.sqrt((pinion_gear_x - spur_gear_center_x) ** 2 + (pinion_gear_y - spur_gear_center_y) ** 2)

                self._reload_run_state = False

            an_angle_direction = 1 if self.is_circumscribe else -1
            add_pinion_radius = pinion_gear_radius * an_angle_direction
            distance_circumference = self._a_pinion_to_spur_distance * 2 * math.pi
            pinion_circumference = pinion_gear_radius * 2 * math.pi

            rotate_angle_index = self._rotate_angle
            move_angle_index = self._move_angle
            pinion_x = 0
            pinion_y = 0
            # 分割数分のペンの軌跡のシュミレートを行う。(an_add_angle(1フレームで動かす度数)が大きくなっても一定の密度で点をうち、点と点の間に隙間をなくせるようにする)
            for _ in range(self._an_add_angle * SPILIT_POINT_NUM):

                # スパーギアの内接(または外接)の円周上に沿って動くピニオンギアの座標を計算する。
                pinion_x = spur_gear_center_x + (self.a_spur_gear.radius() + add_pinion_radius) * math.cos(math.radians(move_angle_index))
                pinion_y = spur_gear_center_y + (self.a_spur_gear.radius() + add_pinion_radius) * math.sin(math.radians(move_angle_index))

                # ピニオンギアの回転角度に応じて、ペンをペンとピニオンギアの距離を半径とした円の円周上を回転させた時の座標を計算する。
                rotate_angle = an_angle_direction * rotate_angle_index * (distance_circumference / pinion_circumference)
                rotate_x = pen_to_pinion_distance * \
                    math.cos(math.radians(rotate_angle + pen_to_pinion_degrees))
                rotate_y = pen_to_pinion_distance * \
                    math.sin(math.radians(rotate_angle + pen_to_pinion_degrees))

                # 動くピニオンギアの座標を回転させたペンの座標に足し込み、ペンのポイント座標とする。
                x = rotate_x + pinion_x
                y = rotate_y + pinion_y

                # 計算した座標を描画ポイントのリストに追加する。
                self._a_points.append((x, y))

                # 次の計算のために、回転角度を 1/分割数 増やす。
                rotate_angle_index += (1 / SPILIT_POINT_NUM)
                move_angle_index += (1 / SPILIT_POINT_NUM)

            self.a_pinion_gear.set_center_position(pinion_x, pinion_y)
            self.a_pinion_gear.rotate(an_angle_direction * self._rotate_angle * (distance_circumference / pinion_circumference))

            move_pen_x, move_pen_y = self._a_points[len(self._a_points) - 1]
            self.a_pinion_gear.set_pen_pos(move_pen_x - pen_radius, move_pen_y - pen_radius, True)  # 反応的にペンの座標を設定

            self._move_angle = (self._move_angle + self._an_add_angle) % 36000000  # 10万周すると0に戻る
            self._rotate_angle = (self._rotate_angle + self._an_add_angle) % 36000000  # 10万周すると0に戻る

        self.draw_frame()

    def draw_frame(self) -> None:
        """Viewに各情報の描画を依頼する。"""
        clear_draw_surface(self.a_gear_surface)
        self.a_spiro_view.draw_gear_connection_line()
        self.a_spiro_view.draw_spur_gear()
        self.a_spiro_view.draw_pinion_gear()
        self.a_spiro_view.draw_pen()

        if self.an_active_surface is not None and self.is_animated:
            self.a_spiro_view.draw_pen_pos(self._a_points)
        self._a_points = []

    def set_spur_gear_center_position(self, x: int, y: int) -> None:
        """
        スパーギアの中心の座標を設定する.

        Args:
            x (int):
                ギアの中心のx座標
            y (int):
                ギアの中心のy座標
        """
        spur_gear_center_x, spur_gear_center_y = self.a_spur_gear.center()  # スパーギアの中心の座標を取得する
        pinion_gear_center_x, pinion_gear_center_y = self.a_pinion_gear.center()  # ピニオンギアの中心の座標を取得する
        dx, dy = x - spur_gear_center_x, y - spur_gear_center_y  # スパーギアの移動した距離を求める
        if self.a_spur_gear.set_center_position(x, y):  # スパーギアの中心の座標を設定する
            self.a_pinion_gear.set_center_position(pinion_gear_center_x + dx,
                                                   pinion_gear_center_y + dy)  # ピニオンギアの中心の座標を設定する

    def set_pinion_gear_center_position(self, x: int, y: int) -> None:
        """
        現在の制約状態(内接円、外接円)を考慮しながらピニオンギアの中心の座標を設定します.

        Args:
            x (int):
                ギアの中心のx座標
            y (int):
                ギアの中心のy座標
        """
        spur_gear_center_x, spur_gear_center_y = self.a_spur_gear.center()  # スパーギアの中心の座標を取得する
        spur_gear_radius = self.a_spur_gear.radius()
        pinion_gear_radius = self.a_pinion_gear.radius()
        # スパーギアの中心のx座標とピニオンギアの中心のx座標の差
        dx = x - spur_gear_center_x
        # スパーギアの中心のy座標とピニオンギアの中心のy座標の差
        dy = y - spur_gear_center_y

        gear_distance = spur_gear_radius - pinion_gear_radius if not self.is_circumscribe else spur_gear_radius + pinion_gear_radius
        amount_of_increase_in_x, amount_of_increase_in_y = utils.convert_length_of_line_to_x_and_y(
            dx, dy, gear_distance)

        pinion_x = spur_gear_center_x + amount_of_increase_in_x
        pinion_y = spur_gear_center_y + amount_of_increase_in_y
        self.a_pinion_gear.set_center_position(pinion_x, pinion_y)

    def add_spur_gear_position(self, dx: int, dy: int) -> None:
        """
        マウスの移動量に合わせてスパーギアの中心の座標を移動する.

        Args:
            dx (int):
                x方向の移動量
            dy (int):
                y方向の移動量
        """
        spur_gear_center_x, spur_gear_center_y = self.a_spur_gear.center()
        self.set_spur_gear_center_position(spur_gear_center_x + dx, spur_gear_center_y + dy)

    def add_pinion_gear_position(self, dx: int, dy: int) -> None:
        """
        マウスの移動量に合わせてピニオンギアの中心の座標を移動する.

        Args:
            dx (int):
                x方向の移動量
            dy (int):
                y方向の移動量
        """
        pinion_gear_center_x, pinion_gear_center_y = self.a_pinion_gear.center()
        self.set_pinion_gear_center_position(pinion_gear_center_x + dx, pinion_gear_center_y + dy)

    def add_spur_gear_radius(self, value: int) -> None:
        """
        スパーギアの半径を指定した値だけ増やす.

        Args:
            value (int):
                増やす半径の量
        """
        pinion_gear_radius = self.a_pinion_gear.radius()  # ピニオンギアの半径を取得する
        spur_gear_radius = self.a_spur_gear.radius()  # スパーギアの半径を取得する
        spur_gear_center_x, spur_gear_center_y = self.a_spur_gear.center()  # スパーギアの中心の座標を取得する
        pinion_gear_center_x, pinion_gear_center_y = self.a_pinion_gear.center()  # ピニオンギアの中心の座標を取得する

        amount_of_increase_in_x, amount_of_increase_in_y = utils.convert_length_of_line_to_x_and_y(
            spur_gear_center_x - pinion_gear_center_x, spur_gear_center_y - pinion_gear_center_y, value)

        min_spur_gear_radius = pinion_gear_radius * 2 - pinion_gear_radius / 2
        if ((spur_gear_radius + value) > min_spur_gear_radius):
            self.a_spur_gear.add_radius(value)  # スパーギアの半径を増やす
            self.set_pinion_gear_center_position(pinion_gear_center_x + amount_of_increase_in_x,
                                                 pinion_gear_center_y + amount_of_increase_in_y)

    def add_pinion_gear_radius(self, value: int) -> None:
        """
        ピニオンギアの半径をセットする

        Args:
            value (int):
                ギアの半径
        """
        pinion_gear_radius = self.a_pinion_gear.radius()  # ピニオンギアの半径を取得する
        spur_gear_radius = self.a_spur_gear.radius()  # スパーギアの半径を取得する
        spur_gear_center_x, spur_gear_center_y = self.a_spur_gear.center()  # スパーギアの中心の座標を取得する
        pinion_gear_center_x, pinion_gear_center_y = self.a_pinion_gear.center()  # ピニオンギアの中心の座標を取得する
        # スパーギアの中心のx座標とピニオンギアの中心のx座標の差
        dx = pinion_gear_center_x - spur_gear_center_x
        # スパーギアの中心のx座標とピニオンギアの中心のx座標の差
        dy = pinion_gear_center_y - spur_gear_center_y
        # ピニオンギアの中心のx座標とy座標の増加量を求める
        amount_of_increase_in_x, amount_of_increase_in_y = utils.convert_length_of_line_to_x_and_y(
            dx, dy, value / 2)

        max_pinion_gear_radius = spur_gear_radius - (spur_gear_radius / 3)
        if not self.is_circumscribe:
            if (max_pinion_gear_radius > pinion_gear_radius + value):
                self.a_pinion_gear.add_radius(value)  # ピニオンギアの半径を増やす
                self.set_pinion_gear_center_position(pinion_gear_center_x + amount_of_increase_in_x,
                                                     pinion_gear_center_y + amount_of_increase_in_y)
        elif self.is_circumscribe:
            self.a_pinion_gear.add_radius(value)  # ピニオンギアの半径を増やす
            self.set_pinion_gear_center_position(pinion_gear_center_x + amount_of_increase_in_x,
                                                 pinion_gear_center_y + amount_of_increase_in_y)

    def check_picking_spur_wheel(self, x: int, y: int) -> str | None:
        """
        引数の座標がスパーギアのピッキング可能円かどうかを判定する。

        Args:
            x (int):
                x座標
            y (int):
                y座標

        Returns:
            True:
                可能
            False:
                それ以外の場合
        """
        if self.a_spur_gear.a_top_rect.collidepoint((x, y)):
            return "top"
        if self.a_spur_gear.a_left_rect.collidepoint((x, y)):
            return "left"
        if self.a_spur_gear.a_right_rect.collidepoint((x, y)):
            return "right"
        if self.a_spur_gear.a_bottom_rect.collidepoint((x, y)):
            return "bottom"
        return None

    def check_picking_pinion_wheel(self, x: int, y: int) -> str | None:
        """
        引数の座標がピニオンギアのピッキング可能円かどうかを判定する。

        Args:
            x (int):
                x座標
            y (int):
                y座標

        Returns:
            True:
                可能
            False:
                それ以外の場合
        """
        if self.a_pinion_gear.a_top_rect.collidepoint((x, y)):
            return "top"
        if self.a_pinion_gear.a_left_rect.collidepoint((x, y)):
            return "left"
        if self.a_pinion_gear.a_right_rect.collidepoint((x, y)):
            return "right"
        if self.a_pinion_gear.a_bottom_rect.collidepoint((x, y)):
            return "bottom"
        return None

    def check_spur_selected_wheel(self, x: int, y: int) -> bool:
        """引数の座標がスパーギアをホールドしているかどうかを判定する.

        Args:
            x (int):
                x座標
            y (int):
                y座標

        Returns:
            True:
                ホールドしている
            False:
                ホールドしていない
        """

        return self.a_spur_gear.center_rect().collidepoint((x, y))

    def check_pinion_selected_wheel(self, x: int, y: int) -> bool:
        """引数の座標がピニオンギアをホールドしているかどうかを判定する.

        Args:
            x (int):
                x座標
            y (int):
                y座標

        Returns:
            True:
                ホールドしている
            False:
                ホールドしていない
        """

        return self.a_pinion_gear.center_rect().collidepoint((x, y))

    def check_pen_selected_wheel(self, x: int, y: int) -> bool:
        """引数の座標がペンをホールドしているかどうかを判定する.

        Args:
            x (int):
                x座標
            y (int):
                y座標

        Returns:
            True:
                ホールドしている
            False:
                ホールドしていない
        """

        return self.a_pinion_gear.pen().collidepoint((x, y))

    def add_pen_pos(self, dx: int, dy: int) -> None:
        """
        ペンの座標を設定する.

        Args:
            x (int):
                ペンのx座標.
            y (int):
                ペンのy座標.
        """
        self.a_pinion_gear.add_pen_pos(dx, dy)

    def set_pen_nib(self, nib: int) -> None:
        """
        ペンの太さを設定します。

        Args:
            nib (int):
                ペンの太さ
        """
        self.a_pinion_gear.set_pen_nib(nib)

    def set_pen_color(self, color: tuple[int, int, int]) -> None:
        """
        ペンの色を設定します。色情報のtupleではない場合、設定は行われません。

        Args:
            color (tuple[int, int, int]):
                ペンの色情報
        """
        self.a_pinion_gear.set_pen_color(color)

    def pen_rainbow(self) -> None:
        """ペンの色を虹色遷移させる。"""
        r, g, b = self.a_pinion_gear.pen_color()
        if (r == 255 and g < 255 and b == 0):
            g += 5
        elif (r > 0 and g == 255 and b == 0):
            r -= 5
        elif (r == 0 and g == 255 and b < 255):
            b += 5
        elif (r == 0 and g > 0 and b == 255):
            g -= 5
        elif (r < 255 and g == 0 and b == 255):
            r += 5
        elif (r == 255 and g == 0 and b > 0):
            b -= 5

        self.set_pen_color((r, g, b))

    def start_rainbow(self) -> None:
        """ペンの色の虹色モードを開始します"""
        self.is_rainbow = True
        self.set_pen_color((255, 0, 0))

    def stop_rainbow(self) -> None:
        """ペンの色の虹色モードを終了します"""
        self.is_rainbow = False

    def start_animation(self) -> None:
        """アニメーションを開始する。。"""
        self.is_animated = True

    def stop_animation(self) -> None:
        """アニメーションを停止する"""
        self.is_animated = False

    def start_circumscribe(self) -> None:
        """外接円モードをスタートする"""
        self.is_circumscribe = True
        if not self.is_animated:
            self.set_pinion_gear_center_position(*self.a_pinion_gear.center())

    def stop_circumscribe(self) -> None:
        """外接円モードをストップする"""
        self.is_circumscribe = False

        spur_gear_radius = self.a_spur_gear.radius()
        pinion_gear_radius = self.a_pinion_gear.radius()
        max_pinion_gear_radius = spur_gear_radius - (spur_gear_radius / 3)

        if pinion_gear_radius > max_pinion_gear_radius:
            self.a_pinion_gear.force_set_radius(max_pinion_gear_radius)  # ピニオンギアの半径を反応的に更新する

        self.set_pinion_gear_center_position(*self.a_pinion_gear.center())

    def current_clear(self) -> None:
        """dive前の軌跡のみをクリアする"""
        if not self.is_dived:
            clear_draw_surface(self.an_active_surface)

    def clear(self) -> None:
        """軌跡をクリア(メイン軌跡ボード・アクティブ領域からスパーギアの範囲をクリアする)"""
        pygame.draw.circle(self.a_main_board_surface, BACKGROUND_COLOR, self.a_spur_gear.center(), self.a_spur_gear.radius())

        spur_x, spur_y = self.a_spur_gear.center()
        active_x, active_y = self.an_active_surface_pos
        clear_active_x = spur_x - active_x
        clear_active_y = spur_y - active_y

        if self.an_active_surface is not None:
            pygame.draw.circle(self.an_active_surface, BACKGROUND_COLOR, (clear_active_x, clear_active_y), self.a_spur_gear.radius())

    def dive(self) -> None:
        """diveする"""
        if not self.is_dived:
            self.a_main_board_surface.blit(self.an_active_surface, self.an_active_surface_pos)
            self.is_dived = True
            self.an_active_surface = None

            self._reload_run_state = True

            self.a_pinion_gear.rotate(0)  # 回転をリセットする

            # ピニオンギアの中心位置の設定を呼び出し、現在のピニオンギアの座標に基づいてペンの座標を反応的に変更する
            self.a_pinion_gear.set_center_position(*self.a_pinion_gear.center())

    def check_dive(self) -> bool:
        """dive中かどうかを返す

        Returns:
            bool: dive中ならTrue。そうでないならFalse。
        """
        return self.is_dived

    def open_file(self) -> None:
        """スピロプログラムの保存ファイルを開き、内容を復元する"""
        def attach_file_content(file_content: str) -> None:
            a_spiro_file_parser = SpiroFileParser.decode(file_content)
            if a_spiro_file_parser is None:
                return

            self.a_main_board_surface = make_surface(a_spiro_file_parser.a_board_data, BOARD_WIDTH, BOARD_HEIGHT)
            self.a_main_board_surface_pos = (a_spiro_file_parser.a_board_pos_x, a_spiro_file_parser.a_board_pos_y)
            self.a_spur_gear.set_center_position(a_spiro_file_parser.a_spur_gear_center_x, a_spiro_file_parser.a_spur_gear_center_y)
            self.a_spur_gear.set_radius(a_spiro_file_parser.a_spur_gear_radius)
            self.a_pinion_gear.set_center_position(a_spiro_file_parser.a_pinion_gear_center_x, a_spiro_file_parser.a_pinion_gear_center_y)
            self.a_pinion_gear.set_radius(a_spiro_file_parser.a_pinion_gear_radius)
            self.is_circumscribe = a_spiro_file_parser.a_is_circumscrib
            self.a_pinion_gear.set_pen_pos(a_spiro_file_parser.a_pen_pos_x, a_spiro_file_parser.a_pen_pos_y)
            self.a_pinion_gear.set_pen_nib(a_spiro_file_parser.a_pen_nib)

            r, g, b = a_spiro_file_parser.a_pen_color.split(",")
            self.a_pinion_gear.set_pen_color((parse_int(r), parse_int(g), parse_int(b)))

        askopenfilecontent(attach_file_content, "*.json")

    def save_file(self) -> None:
        """現在のメインボードの状態を保存する"""
        animated = self.is_animated
        if animated:
            self.stop_animation()

        clear_draw_surface(self.a_gear_surface)
        board_data = output_surface(self.a_main_board_surface)
        r, g, b = self.a_pinion_gear.pen_color()
        file_parser = SpiroFileParser(
            board_data,
            *self.a_main_board_surface_pos,
            *self.a_spur_gear.center(),
            self.a_spur_gear.radius(),
            *self.a_pinion_gear.center(),
            self.a_pinion_gear.radius(),
            self.is_circumscribe,
            *self.a_pinion_gear.pen().topleft,
            self.a_pinion_gear.pen().width,
            f"{r},{g},{b}"
        )

        # 　現在の日付をファイルネームとして変数に束縛する
        now = datetime.datetime.now()
        file_name = now.strftime(FIILE_NAME_FORMAT)

        download_content(file_parser.encode(), file_name)
        messagebox("ダウンロードディレクトリに保存しました")

        if animated:
            self.start_animation()

    def set_create_active_surface(self) -> pygame.Surface:
        """スパーギアの状態からアクティブなSutfaceを作成し、設定する

        Returns:
            pygame.Surface: アクティブなSurface
        """
        if self.is_dived:
            a_spur_gear_radius = self.a_spur_gear.radius()
            a_pinion_gear_radius = self.a_pinion_gear.radius()
            a_spur_gear_x, a_spur_gear_y = self.a_spur_gear.center()
            size = (a_spur_gear_radius * 2) + (a_pinion_gear_radius * 4) + ACTIVE_SURFACE_PADDING

            self.an_active_surface = pygame.Surface((size, size), pygame.SRCALPHA)

            active_surface_x = a_spur_gear_x - (size / 2)
            active_surface_y = a_spur_gear_y - (size / 2)
            self.an_active_surface_pos = (active_surface_x, active_surface_y)

    def move_main_board_surface(self, dx: int, dy: int) -> None:
        """メインボードのSurfaceを移動する

        Args:
            dx (int): x軸方向の移動量
            dy (int): y軸方向の移動量
        """
        main_board_x, main_board_y = self.a_main_board_surface_pos
        self.a_main_board_surface_pos = (main_board_x + dx, main_board_y + dy)

    def speed_up(self) -> None:
        """アニメーションのスピードを上げる"""
        self._an_add_angle += SPEED_STEP
        if self._an_add_angle >= MAX_SPEED:
            self._an_add_angle = MAX_SPEED

    def speed_down(self) -> None:
        """アニメーションのスピードを下げる"""
        self._an_add_angle -= SPEED_STEP
        if self._an_add_angle <= MIN_SPEED:
            self._an_add_angle = MIN_SPEED

    def main_board_surface(self) -> pygame.Surface:
        """メインボードのSurfaceを返す

        Returns:
            pygame.Surface: メインボードのSurface
        """
        return self.a_main_board_surface

    def main_board_surface_pos(self) -> tuple[int, int]:
        """メインボードのSurfaceの座標を返す

        Returns:
            tuple[int, int]: メインボードのSurfaceの座標
        """
        return self.a_main_board_surface_pos

    def gear_surface(self) -> pygame.Surface:
        """ギアのsurfaceを返す

        Returns:
            pygame.Surface: ギアのsurface
        """
        return self.a_gear_surface

    def active_surface(self) -> pygame.Surface:
        """アクティブな軌跡用Surfaceを返す

        Returns:
            pygame.Surface: アクティブな軌跡用Surface
        """
        return self.an_active_surface

    def active_surface_pos(self) -> tuple[int, int]:
        """アクティブな軌跡用Surfaceの座標を返す

        Returns:
            tuple[int, int]: アクティブな軌跡用Surfaceの座標
        """
        return self.an_active_surface_pos

    def spur_gear(self) -> SpurGear:
        """スパーギア

        Returns:
            SpurGear: スパーギアのインスタンス
        """
        return self.a_spur_gear

    def pinion_gear(self) -> PinionGear:
        """ピニオンギア

        Returns:
            PinionGear: ピニオンギアのインスタンス
        """
        return self.a_pinion_gear

    def animation(self) -> bool:
        """アニメーション中かどうかを返す

        Returns:
            bool: アニメーション中かどうか
        """
        return self.is_animated

    def rainbow(self) -> bool:
        """虹色遷移中かどうかを返す

        Returns:
            bool: 虹色遷移中かどうか
        """
        return self.is_rainbow
