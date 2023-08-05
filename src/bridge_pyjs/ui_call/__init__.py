#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Yomogiβ'
__version__ = '1.0.1'
__date__ = '2023/06/16 (Created: 2023/04/30 )'

# Python
import tkinter
from .ui_call import askopenfilecontent, askcolorcode, askvalue, askquestion
__all__ = ['askopenfilecontent', 'askcolorcode', 'askvalue', 'askquestion']

# Javascript
# import bridge_pyjs.ui_call.ui_call as ui_call
# askopenfilecontent = ui_call.askopenfilecontent
# askcolorcode = ui_call.askcolorcode
# askvalue = ui_call.askvalue
# askquestion = ui_call.askquestion


def init():
    """uiをcallするのに必要な初期化処理を行います。pygameの初期化よりも先に呼び出す必要があります

    Returns:
        tkinter.Tk:
            tkinterのrootウィンドウ
    """
    # Javascript
    # return None

    # Python
    root = tkinter.Tk()
    root.withdraw()
    return root
