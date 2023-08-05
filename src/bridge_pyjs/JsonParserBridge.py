#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Yomogiβ'
__version__ = '1.0.0'
__date__ = '2023/06/22 (Created: 2023/06/22 )'

# Python
import json


class JsonParser:

    @staticmethod
    def encode(data):
        """引数のデータをjson形式に変換します。"""

        # Javascript
        # return JSON.stringify(data)

        # Python
        return json.dumps(data)

    @staticmethod
    def decode(json_str: str):
        """引数のjson文字列をデコードします。"""

        # Javascript
        # return JSON.parse(json_str)

        # Python
        return json.loads(json_str)
