from Constants import BOARD_HEIGHT, BOARD_WIDTH, DISPLAY_HEIGHT, MIN_GEAR_RADIUS, PICKING_CIRCLE_PADDING
from bridge_pyjs.PygameBridge import pygame, rect_update
import math
__author__ = 'ARA T'
__version__ = '1.0.3'
__date__ = '2023/07/04 (Created: 2023/5/19)'


class SpiroGear:
    """
    スーパーギア及びピニオンギアの親クラス

    ギアの親クラスです。スーパーギア及びピニオンギアの共通の機能を提供します。
    このクラスは基本的に継承して使用されることを想定しています。
    """

    def __init__(self, x: float, y: float, radius: int) -> None:
        """
        ギアのコンストラクタメソッド.

        Args:
            x (int):
                ギアの中心のx座標.
            y	(int):
                ギアの中心のy座標.
            radius (int):
                ギアの半径.
        """
        self.a_center = (x, y)
        self.a_radius = radius
        self.a_bottom_rect = pygame.Rect(0, 0, 0, 0)
        self.a_left_rect = pygame.Rect(0, 0, 0, 0)
        self.a_right_rect = pygame.Rect(0, 0, 0, 0)
        self.a_top_rect = pygame.Rect(0, 0, 0, 0)
        self.a_center_rect = pygame.Rect(0, 0, 0, 0)
        self.update_picking_rect()

    def update_picking_rect(self) -> None:
        """ギアの上下左右のピッキングエリアのRectを更新します。"""
        center_x, center_y = self.a_center
        rect_update(self.a_bottom_rect,
                    center_x - PICKING_CIRCLE_PADDING / 2,
                    center_y + self.a_radius - PICKING_CIRCLE_PADDING / 2,
                    PICKING_CIRCLE_PADDING,
                    PICKING_CIRCLE_PADDING)
        rect_update(self.a_left_rect,
                    center_x - self.a_radius - PICKING_CIRCLE_PADDING / 2,
                    center_y - PICKING_CIRCLE_PADDING / 2,
                    PICKING_CIRCLE_PADDING,
                    PICKING_CIRCLE_PADDING)
        rect_update(self.a_right_rect,
                    center_x + self.a_radius - PICKING_CIRCLE_PADDING / 2,
                    center_y - PICKING_CIRCLE_PADDING / 2,
                    PICKING_CIRCLE_PADDING,
                    PICKING_CIRCLE_PADDING)
        rect_update(self.a_top_rect,
                    center_x - PICKING_CIRCLE_PADDING / 2,
                    center_y - self.a_radius - PICKING_CIRCLE_PADDING / 2,
                    PICKING_CIRCLE_PADDING,
                    PICKING_CIRCLE_PADDING)
        rect_update(self.a_center_rect,
                    center_x - PICKING_CIRCLE_PADDING / 2,
                    center_y - PICKING_CIRCLE_PADDING / 2,
                    PICKING_CIRCLE_PADDING,
                    PICKING_CIRCLE_PADDING)

    def set_center_position(self, x: float, y: float) -> None:
        """
        ギアの中心の座標を設定します.

        Args:
            x (int):
                ギアの中心のx座標.
            y	(int):
                ギアの中心のy座標.
        """
        self.a_center = (x, y)
        self.update_picking_rect()

    def rotate(self, degrees: float) -> None:
        """
        ギアを回転させます

        Args:
            degrees (int):
                回転させる角度.
        """
        gear_x, gear_y = self.center()

        bottom_x = gear_x + self.radius() * math.cos(math.radians(degrees + 90))
        bottom_y = gear_y + self.radius() * math.sin(math.radians(degrees + 90))
        bottom_x -= PICKING_CIRCLE_PADDING / 2
        bottom_y -= PICKING_CIRCLE_PADDING / 2

        left_x = gear_x + self.radius() * math.cos(math.radians(degrees + 180))
        left_y = gear_y + self.radius() * math.sin(math.radians(degrees + 180))
        left_x -= PICKING_CIRCLE_PADDING / 2
        left_y -= PICKING_CIRCLE_PADDING / 2

        right_x = gear_x + self.radius() * math.cos(math.radians(degrees))
        right_y = gear_y + self.radius() * math.sin(math.radians(degrees))
        right_x -= PICKING_CIRCLE_PADDING / 2
        right_y -= PICKING_CIRCLE_PADDING / 2

        top_x = gear_x + self.radius() * math.cos(math.radians(degrees + 270))
        top_y = gear_y + self.radius() * math.sin(math.radians(degrees + 270))
        top_x -= PICKING_CIRCLE_PADDING / 2
        top_y -= PICKING_CIRCLE_PADDING / 2

        rect_update(self.a_bottom_rect, bottom_x, bottom_y, PICKING_CIRCLE_PADDING, PICKING_CIRCLE_PADDING)
        rect_update(self.a_left_rect, left_x, left_y, PICKING_CIRCLE_PADDING, PICKING_CIRCLE_PADDING)
        rect_update(self.a_right_rect, right_x, right_y, PICKING_CIRCLE_PADDING, PICKING_CIRCLE_PADDING)
        rect_update(self.a_top_rect, top_x, top_y, PICKING_CIRCLE_PADDING, PICKING_CIRCLE_PADDING)

    def add_radius(self, value: int) -> bool:
        """
        引数に指定した分だけ半径を足します.

        引数に指定した分だけギアの半径を足します。
        引数の値にマイナスを指定すれば半径が小さくなります

        Args:
            value (int):
                半径に足し込む量.

        Returns:
            bool:
                半径を足し込めたかどうか.
        """
        update_radius = self.a_radius + value
        if update_radius < MIN_GEAR_RADIUS:
            return False

        x, y = self.a_center
        if x - update_radius < 0 or x + update_radius > BOARD_WIDTH:
            return False

        if y - update_radius < 0 or y + update_radius > BOARD_HEIGHT:
            return False

        if update_radius > DISPLAY_HEIGHT / 2:
            return False

        self.a_radius += value
        self.update_picking_rect()
        return True

    def set_radius(self, radius: int) -> bool:
        """半径を引数の値に変更します。

        Args:
            radius (int):
                半径.

        Returns:
            bool:
                半径を変更できたかどうか.
        """
        if radius < MIN_GEAR_RADIUS:
            return False

        x, y = self.a_center
        if x - radius < 0 or x + radius > BOARD_WIDTH:
            return False

        if y - radius < 0 or y + radius > BOARD_HEIGHT:
            return False

        if radius > DISPLAY_HEIGHT / 2:
            return False

        self.a_radius = radius
        self.update_picking_rect()
        return True

    def bottom_rect(self) -> pygame.Rect:
        """
        ギアの下部のピッキング可能円のRectインスタンスを返します

        Returns:
            下部のピッキング可能円のRectインスタンス
        """
        return self.a_bottom_rect

    def left_rect(self) -> pygame.Rect:
        """
        ギアの左のピッキング可能円のRectインスタンスを返します

        Returns:
            左のピッキング可能円のRectインスタンス
        """
        return self.a_left_rect

    def right_rect(self) -> pygame.Rect:
        """
        ギアの右のピッキング可能円のRectインスタンスを返します

        Returns:
            右のピッキング可能円のRectインスタンス
        """
        return self.a_right_rect

    def top_rect(self) -> pygame.Rect:
        """
        ギアの上部のピッキング可能円のRectインスタンスを返します

        Returns:
            上部のピッキング可能円のRectインスタンス
        """
        return self.a_top_rect

    def center_rect(self) -> pygame.Rect:
        """
        ギアの中心部のピッキング可能円のRectインスタンスを返します

        Returns:
            中心部のピッキング可能円のRectインスタンス
        """
        return self.a_center_rect

    def center(self) -> tuple[float, float]:
        """
        ギアの中心の座標を返します

        Returns:
            ギアの中心の座標
        """
        return self.a_center

    def radius(self) -> int:
        """
        ギアの半径を返します

        Returns:
            ギアの半径
        """
        return self.a_radius
