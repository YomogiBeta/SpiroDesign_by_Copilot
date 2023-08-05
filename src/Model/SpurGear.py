#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Constants import BOARD_HEIGHT, BOARD_WIDTH
from Model.SpiroGear import SpiroGear

__author__ = 'Yomogiβ'
__version__ = '1.0.1'
__date__ = '2023/07/08 (Created: 2023/05/18 )'


class SpurGear(SpiroGear):
    """ スパーギアモデル """

    def __init__(self, x: int, y: int, radius: int) -> None:
        super().__init__(x, y, radius)

    def set_center_position(self, x: float, y: float) -> bool:
        """
        ギアの中心の座標を設定します. ただし、スパーギアがボードの外にはみ出る場合は設定しません

        Args:
            x (int):
                ギアの中心のx座標.
            y	(int):
                ギアの中心のy座標.

        Returns:
            bool:
                ギアの中心の座標が設定できたかどうか.
        """
        left = x - self.radius()
        right = x + self.radius()
        top = y - self.radius()
        bottom = y + self.radius()

        if left < 0:
            return False
        if right > BOARD_WIDTH:
            return False
        if top < 0:
            return False
        if bottom > BOARD_HEIGHT:
            return False
        super().set_center_position(x, y)
        return True
