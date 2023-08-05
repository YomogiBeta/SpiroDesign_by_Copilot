#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Dragon'
__version__ = '1.0.0'
__date__ = '2023/07/14 (Created: 2023/07/08 )'


import unittest

from Model.SpiroFileParser import SpiroFileParser
from Model.SpiroModel import SpiroModel
from View.SpiroView import SpiroView
from src.Constants import BOARD_HEIGHT, BOARD_WIDTH, DISPLAY_HEIGHT, DISPLAY_WIDTH, INIT_SPUR_GEAR_RADIUS, INIT_PINION_GEAR_RADIUS
from src.Constants import INIT_PEN_NIB
from bridge_pyjs.PygameBridge import output_surface
from bridge_pyjs.JsonParserBridge import JsonParser
from bridge_pyjs.ParseIntBridge import parse_int


class TestSpiroFileParser(unittest.TestCase):

    def setUp(self):
        """スピロファイルパーサーのテストに関わる準備"""
        self.a_spiro_model = SpiroModel(SpiroView)
        board_data = output_surface(self.a_spiro_model.a_main_board_surface)
        r, g, b = self.a_spiro_model.a_pinion_gear.pen_color()
        self.a_spiro_file_parser = SpiroFileParser(
            board_data,
            *self.a_spiro_model.a_main_board_surface_pos,
            *self.a_spiro_model.a_spur_gear.center(),
            self.a_spiro_model.a_spur_gear.radius(),
            *self.a_spiro_model.a_pinion_gear.center(),
            self.a_spiro_model.a_pinion_gear.radius(),
            self.a_spiro_model.is_circumscribe,
            *self.a_spiro_model.a_pinion_gear.pen().topleft,
            self.a_spiro_model.a_pinion_gear.pen().width,
            f"{r},{g},{b}"
        )

    def test_init(self):
        """スピロファイルパーサーのフィールドのテスト"""
        self.assertEqual(self.a_spiro_file_parser.a_board_data, output_surface(self.a_spiro_model.a_main_board_surface))
        self.assertEqual(self.a_spiro_file_parser.a_board_pos_x, -1 * (BOARD_WIDTH / 2 - DISPLAY_WIDTH / 2))
        self.assertEqual(self.a_spiro_file_parser.a_board_pos_y, -1 * (BOARD_HEIGHT / 2 - DISPLAY_HEIGHT / 2))
        self.assertEqual(self.a_spiro_file_parser.a_spur_gear_center_x, BOARD_WIDTH / 2)
        self.assertEqual(self.a_spiro_file_parser.a_spur_gear_center_y, BOARD_HEIGHT / 2)
        self.assertEqual(self.a_spiro_file_parser.a_spur_gear_radius, INIT_SPUR_GEAR_RADIUS)
        self.assertEqual(self.a_spiro_file_parser.a_pinion_gear_center_x, BOARD_WIDTH / 2 + INIT_PINION_GEAR_RADIUS)
        self.assertEqual(self.a_spiro_file_parser.a_pinion_gear_center_y, BOARD_HEIGHT / 2)
        self.assertEqual(self.a_spiro_file_parser.a_pinion_gear_radius, INIT_PINION_GEAR_RADIUS)
        self.assertEqual(self.a_spiro_file_parser.a_is_circumscrib, self.a_spiro_model.is_circumscribe)
        pen_x, pen_y = self.a_spiro_model.a_pinion_gear.pen().topleft
        self.assertEqual(self.a_spiro_file_parser.a_pen_pos_x, pen_x)
        self.assertEqual(self.a_spiro_file_parser.a_pen_pos_y, pen_y)
        self.assertEqual(self.a_spiro_file_parser.a_pen_nib, INIT_PEN_NIB)
        self.assertEqual(self.a_spiro_file_parser.a_pen_color, f"{0},{0},{0}")

    def test_encode(self):
        """json形式へのエンコードのテスト"""
        json_str = self.a_spiro_file_parser.encode()
        decode_data = JsonParser.decode(json_str)
        self.assertEqual(decode_data['board_data'], self.a_spiro_file_parser.a_board_data)
        self.assertEqual(parse_int(decode_data['board_pos_x']), self.a_spiro_file_parser.a_board_pos_x)
        self.assertEqual(parse_int(decode_data['board_pos_y']), self.a_spiro_file_parser.a_board_pos_y)
        self.assertEqual(parse_int(decode_data['spur_gear']['center_x']), self.a_spiro_file_parser.a_spur_gear_center_x)
        self.assertEqual(parse_int(decode_data['spur_gear']['center_y']), self.a_spiro_file_parser.a_spur_gear_center_y)
        self.assertEqual(parse_int(decode_data['spur_gear']['radius']), self.a_spiro_file_parser.a_spur_gear_radius)
        self.assertEqual(parse_int(decode_data['pinion_gear']['center_x']), self.a_spiro_file_parser.a_pinion_gear_center_x)
        self.assertEqual(parse_int(decode_data['pinion_gear']['center_y']), self.a_spiro_file_parser.a_pinion_gear_center_y)
        self.assertEqual(parse_int(decode_data['pinion_gear']['radius']), self.a_spiro_file_parser.a_pinion_gear_radius)
        self.assertEqual(decode_data['is_circumscrib'], self.a_spiro_file_parser.a_is_circumscrib)
        self.assertEqual(parse_int(decode_data['pen']['pos_x']), self.a_spiro_file_parser.a_pen_pos_x)
        self.assertEqual(parse_int(decode_data['pen']['pos_y']), self.a_spiro_file_parser.a_pen_pos_y)
        self.assertEqual(parse_int(decode_data['pen']['nib']), self.a_spiro_file_parser.a_pen_nib)
        self.assertEqual(decode_data['pen']['color'], self.a_spiro_file_parser.a_pen_color)

    def test_decode(self):
        """スピロデザインで使用できる形式へのデコードのテスト"""
        json_str = self.a_spiro_file_parser.encode()
        self.a_spiro_file_parser.decode(json_str)
        self.assertEqual(self.a_spiro_file_parser.a_board_data, output_surface(self.a_spiro_model.a_main_board_surface))
        self.assertEqual(self.a_spiro_file_parser.a_board_pos_x, -1 * (BOARD_WIDTH / 2 - DISPLAY_WIDTH / 2))
        self.assertEqual(self.a_spiro_file_parser.a_board_pos_y, -1 * (BOARD_HEIGHT / 2 - DISPLAY_HEIGHT / 2))
        self.assertEqual(self.a_spiro_file_parser.a_spur_gear_center_x, BOARD_WIDTH / 2)
        self.assertEqual(self.a_spiro_file_parser.a_spur_gear_center_y, BOARD_HEIGHT / 2)
        self.assertEqual(self.a_spiro_file_parser.a_spur_gear_radius, INIT_SPUR_GEAR_RADIUS)
        self.assertEqual(self.a_spiro_file_parser.a_pinion_gear_center_x, BOARD_WIDTH / 2 + INIT_PINION_GEAR_RADIUS)
        self.assertEqual(self.a_spiro_file_parser.a_pinion_gear_center_y, BOARD_HEIGHT / 2)
        self.assertEqual(self.a_spiro_file_parser.a_pinion_gear_radius, INIT_PINION_GEAR_RADIUS)
        self.assertEqual(self.a_spiro_file_parser.a_is_circumscrib, self.a_spiro_model.is_circumscribe)
        pen_x, pen_y = self.a_spiro_model.a_pinion_gear.pen().topleft
        self.assertEqual(self.a_spiro_file_parser.a_pen_pos_x, pen_x)
        self.assertEqual(self.a_spiro_file_parser.a_pen_pos_y, pen_y)
        self.assertEqual(self.a_spiro_file_parser.a_pen_nib, INIT_PEN_NIB)
        self.assertEqual(self.a_spiro_file_parser.a_pen_color, f"{0},{0},{0}")
