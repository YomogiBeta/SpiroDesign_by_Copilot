#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Yomogiβ'
__version__ = '3.0.0'
__date__ = '2023/07/06 (Created: 2023/06/22 )'

from bridge_pyjs.JsonParserBridge import JsonParser
from bridge_pyjs.ParseIntBridge import parse_int
from bridge_pyjs.ExceptionBridge import exception
from bridge_pyjs.ui_call.ui_call import messagebox


class SpiroFileParser:

    def __init__(self,
                 board_data: str,
                 board_pos_x: int,
                 board_pos_y: int,
                 spur_gear_center_x: int,
                 spur_gear_center_y: int,
                 spur_gear_radius: int,
                 pinion_gear_center_x: int,
                 pinion_gear_center_y: int,
                 pinion_gear_radius: int,
                 is_circumscrib: bool,
                 pen_pos_x: int,
                 pen_pos_y: int,
                 pen_nib: int,
                 pen_color: str):
        self.a_board_data = board_data
        self.a_board_pos_x = board_pos_x
        self.a_board_pos_y = board_pos_y
        self.a_spur_gear_center_x = spur_gear_center_x
        self.a_spur_gear_center_y = spur_gear_center_y
        self.a_spur_gear_radius = spur_gear_radius
        self.a_pinion_gear_center_x = pinion_gear_center_x
        self.a_pinion_gear_center_y = pinion_gear_center_y
        self.a_pinion_gear_radius = pinion_gear_radius
        self.a_is_circumscrib = is_circumscrib
        self.a_pen_pos_x = pen_pos_x
        self.a_pen_pos_y = pen_pos_y
        self.a_pen_nib = pen_nib
        self.a_pen_color = pen_color

    def encode(self) -> str:
        """現在の状態をJson文字列にエンコードします。

        Returns:
            str: Json文字列.
        """
        result = {
            'file_version': __version__,
            'board_data': self.a_board_data,
            'board_pos_x': self.a_board_pos_x,
            'board_pos_y': self.a_board_pos_y,
            'is_circumscrib': self.a_is_circumscrib,
            'spur_gear': {
                'center_x': self.a_spur_gear_center_x,
                'center_y': self.a_spur_gear_center_y,
                'radius': self.a_spur_gear_radius
            },
            'pinion_gear': {
                'center_x': self.a_pinion_gear_center_x,
                'center_y': self.a_pinion_gear_center_y,
                'radius': self.a_pinion_gear_radius
            },
            'pen': {
                'pos_x': self.a_pen_pos_x,
                'pos_y': self.a_pen_pos_y,
                'nib': self.a_pen_nib,
                'color': self.a_pen_color
            }
        }
        return JsonParser.encode(result)

    @staticmethod
    def decode(json_str: str):
        """引数のjson文字列をデコードします。

        Args:
            json_str (str):
                SpiroFileParserでエンコードされたjson文字列
        """
        try:
            decode_data = JsonParser.decode(json_str)
            parser_major_version = __version__.split('.')[0]
            file_major_version = decode_data['file_version'].split('.')[0]

            if parser_major_version != file_major_version:
                messagebox("ファイルバージョンに互換性がありません")
                return None

            return SpiroFileParser(
                decode_data['board_data'],
                parse_int(decode_data['board_pos_x']),
                parse_int(decode_data['board_pos_y']),
                parse_int(decode_data['spur_gear']['center_x']),
                parse_int(decode_data['spur_gear']['center_y']),
                parse_int(decode_data['spur_gear']['radius']),
                parse_int(decode_data['pinion_gear']['center_x']),
                parse_int(decode_data['pinion_gear']['center_y']),
                parse_int(decode_data['pinion_gear']['radius']),
                decode_data['is_circumscrib'],
                parse_int(decode_data['pen']['pos_x']),
                parse_int(decode_data['pen']['pos_y']),
                parse_int(decode_data['pen']['nib']),
                decode_data['pen']['color']
            )
        except exception:  # web互換のためエラーの種類を指定せずにキャッチ
            messagebox("当アプリで生成された保存ファイルを指定する必要があります。もし指定している場合、保存されたファイルは破損している可能性があります。")
            return None
