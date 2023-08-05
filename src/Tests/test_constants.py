#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Dragon'
__version__ = '1.0.0'
__date__ = '2023/07/10 (Created: 2023/07/08 )'


import unittest

from src.Constants import FRAME_RATE, DISPLAY_WIDTH, DISPLAY_HEIGHT, BOARD_WIDTH, BOARD_HEIGHT, INIT_BOARD_POSITION, ACTIVE_SURFACE_PADDING
from src.Constants import FONT_NAME, FONT_SIZE, FONT_WEIGHT, INIT_SPUR_GEAR_RADIUS, INIT_PINION_GEAR_RADIUS, INIT_SPUR_GEAR_POSITION
from src.Constants import INIT_PINION_GEAR_POSITION, INIT_PEN_TO_PINION_DISTANCE, INIT_PEN_NIB
from src.Constants import BACKGROUND_COLOR, SPUR_GEAR_COLOR, PINION_GEAR_COLOR, GEAR_LINE_COLOR, MAX_SPEED
from src.Constants import MIN_SPEED, SPEED_STEP, SPILIT_POINT_NUM, PICKING_CIRCLE_PADDING, PEN_HOLE, CIRCLE_PICKING_RADIUS
from src.Constants import MIN_PINION_GEAR_RADIUS, MIN_GEAR_RADIUS, FIILE_NAME_FORMAT
from src.Constants import CONTEXT_MENU_BACKGROUND_COLOR, CONTEXT_MENU_ON_BACKGROUND_COLOR
from src.Constants import CONTEXT_MENU_ON_DISABLE_BACKGROUND_COLOR, CONTEXT_MENU_HOVERD_BACKGROUND_COLOR, CONTEXT_MENU_DIVIDER_COLOR


class TestConstants(unittest.TestCase):

    def test_constants(self):
        """定数たちのテスト"""
        self.assertEqual(FRAME_RATE, 60)
        self.assertEqual(DISPLAY_WIDTH, 1280)
        self.assertEqual(DISPLAY_HEIGHT, 720)
        self.assertEqual(BOARD_WIDTH, 3000)
        self.assertEqual(BOARD_HEIGHT, 3000)
        self.assertEqual(INIT_BOARD_POSITION, (-1 * (BOARD_WIDTH / 2 - DISPLAY_WIDTH / 2), -1 * (BOARD_HEIGHT / 2 - DISPLAY_HEIGHT / 2)))
        self.assertEqual(ACTIVE_SURFACE_PADDING, 20)
        self.assertEqual(FONT_NAME, "NotoSansJP")
        self.assertEqual(FONT_SIZE, 12)
        self.assertEqual(FONT_WEIGHT, 400)
        self.assertEqual(INIT_SPUR_GEAR_RADIUS, 128)
        self.assertEqual(INIT_PINION_GEAR_RADIUS, 64)
        self.assertEqual(INIT_SPUR_GEAR_POSITION, (BOARD_WIDTH / 2, BOARD_HEIGHT / 2))
        self.assertEqual(INIT_PINION_GEAR_POSITION, (BOARD_WIDTH / 2 + INIT_PINION_GEAR_RADIUS, BOARD_HEIGHT / 2))
        self.assertEqual(INIT_PEN_TO_PINION_DISTANCE, 24.0)
        self.assertEqual(INIT_PEN_NIB, 4)
        self.assertEqual(BACKGROUND_COLOR, (255, 255, 255))
        self.assertEqual(SPUR_GEAR_COLOR, (255, 0, 0))
        self.assertEqual(PINION_GEAR_COLOR, (0, 0, 255))
        self.assertEqual(GEAR_LINE_COLOR, (0, 255, 0))
        self.assertEqual(MAX_SPEED, 10)
        self.assertEqual(MIN_SPEED, 1)
        self.assertEqual(SPEED_STEP, 1)
        self.assertEqual(SPILIT_POINT_NUM, 8)
        self.assertEqual(PICKING_CIRCLE_PADDING, 24)
        self.assertEqual(PEN_HOLE, 3)
        self.assertEqual(CIRCLE_PICKING_RADIUS, 4)
        self.assertEqual(MIN_PINION_GEAR_RADIUS, 14)
        self.assertEqual(MIN_GEAR_RADIUS, 12)
        self.assertEqual(FIILE_NAME_FORMAT, "spiro_data_%Y%m%d%H%M%S.json")
        self.assertEqual(CONTEXT_MENU_BACKGROUND_COLOR, (252, 252, 255))
        self.assertEqual(CONTEXT_MENU_ON_BACKGROUND_COLOR, (26, 28, 30))
        self.assertEqual(CONTEXT_MENU_ON_DISABLE_BACKGROUND_COLOR, (200, 200, 200))
        self.assertEqual(CONTEXT_MENU_HOVERD_BACKGROUND_COLOR, (241, 243, 245))
        self.assertEqual(CONTEXT_MENU_DIVIDER_COLOR, (200, 200, 200))
