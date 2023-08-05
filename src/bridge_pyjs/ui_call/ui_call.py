#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python
from tkinter import filedialog
from tkinter import colorchooser
from tkinter import messagebox as tk_messagebox
import os
import platform
from bridge_pyjs.ui_call.ScaleDialog import ScaleDialog

__author__ = 'Yomogiβ'
__version__ = '1.0.6'
__date__ = '2023/07/09 (Created: 2023/05/01 )'


def askopenfilecontent(callback, accept="", mode="r") -> None:
    """ファイルダイアログを開き、選択されたファイルの内容を引数のコールバック関数に渡す

    Args:
        callback (Callable[[str], None]):
            ファイルの内容を引数に取るコールバック関数
        accept (str, optional):
            受け付けるファイルの拡張子。 ex (*.txt) (*.txt;*.csv) . デフォルトは "" .
        mode (str, optional):
            ファイルを開くモード. デフォルトは "r" .
    """

    # Python
    target_file = filedialog.askopenfilename(filetypes=[(accept, accept)])
    if target_file == "":
        return
    with open(target_file, mode, encoding="utf-8") as f:
        content = f.read()
        callback(content)

    # Javascript
    # fileinput = document.getElementById('file_selector')
    # accept = accept.replace("*", "").replace(";", ",")
    # fileinput.accept = accept
    # fileinput.click()

    # Javascript
    # def file_select(e):
        # reader = __new__(FileReader())
        # reader.readAsText(e.target.files[0])
        # reader.addEventListener('load', lambda: callback(reader.result))
        # e.target.value = ""
        # fileinput.removeEventListener('change', file_select)

    # Javascript
    # fileinput.addEventListener('change', file_select)


def colorcode_to_rgb(colorcode: str) -> tuple[int, int, int]:
    """16進数のカラーコードをRGB値に変換する

    Args:
        colorcode (str):
            16進数のカラーコード

    Returns:
        tuple[int, int, int]:
            RGB値
    """

    # Python
    colorcode = colorcode[1:]
    if len(colorcode) != 6:
        raise ValueError("Invalid color code")

    # Python
    red = int(colorcode[0:2], 16)
    green = int(colorcode[2:4], 16)
    blue = int(colorcode[4:6], 16)

    # Javascript
    # colorcode = colorcode[1:]
    # if len(colorcode) != 6:
        # raise ValueError("Invalid color code")

    # Javascript
    # red = parseInt(colorcode[0:2], 16)
    # green = parseInt(colorcode[2:4], 16)
    # blue = parseInt(colorcode[4:6], 16)

    return red, green, blue


def askcolorcode(callback) -> tuple[int, int, int]:
    """カラーを尋ねるダイアログを開き、入力されたカラーを引数のコールバック関数に渡す

    Args:
        callback (Callable[[tuple[int,int,int]], None]):
            RGBを引数に取るコールバック関数
    """

    # Python
    color_code = colorchooser.askcolor()
    if color_code == "":
        return
    callback(color_code[0])

    # Javascript
    # colorinput = document.getElementById('color_selector')
    # colorinput.click()

    # Javascript
    # def color_select(e):
        # print(e.target.value)
        # callback(colorcode_to_rgb(e.target.value))
        # colorinput.removeEventListener('change', color_select)

    # Javascript
    # colorinput.addEventListener('change', color_select)


def download_content(content, filename: str, mode='w') -> None:
    """コンテンツの内容をfilenameとしてローカルのダウンロードに保存する

    Args:
        content (bytes | buffer):
            保存するコンテンツの内容
        filename (str):
            保存するファイル名
        mode (str, optional):
            ファイルを開くモード. デフォルトは "w" .
    """

    # Python
    if platform.system() == "Windows":
        download_dir = os.path.join(os.environ["USERPROFILE"], "Downloads")
        if not os.path.exists(download_dir):
            os.mkdir(download_dir)
    else:
        download_dir = os.path.join(os.environ["HOME"], "Downloads")
    save_path = os.path.join(download_dir, filename)
    with open(save_path, mode, encoding="utf-8") as f:
        f.write(content)

    # Javascript
    # downLoadLink = document.createElement("a")
    # downLoadLink.download = filename
    # downLoadLink.href = URL.createObjectURL(__new__(Blob([content], {type: "text.plain"})))
    # downLoadLink.dataset.downloadurl = ["text/plain", downLoadLink.download, downLoadLink.href].join(":")
    # downLoadLink.click()


def askvalue(master, callback, init_value=1.0) -> None:
    """スライドバーを開き、数値を引数のコールバック関数に渡す

    Args:
        callback (Callable[[float], None]):
            数値を引数に取るコールバック関数
    """

    # Python
    ScaleDialog(master, callback, init_value)

    # Javascript
    # slider_panel = document.getElementById('slider-panel')
    # slider_button = document.getElementById('slider-decide-button')
    # slider = document.getElementById('slider')
    # slider_label = document.getElementById('slider-label')
    # slider_panel.showModal()
    # slider.value = str(init_value)
    # slider_label.textContent = str(init_value)

    # Javascript
    # def select_value(e):
        # slider_panel.close()
        # callback(parseFloat(slider.value))

    # Javascript
    # def remove_button_event_listener(e):
        # slider_button.removeEventListener('click', select_value)
        # slider_panel.removeEventListener('close', remove_button_event_listener)

    # Javascript
    # slider_button.addEventListener('click', select_value)
    # slider_panel.addEventListener('close', remove_button_event_listener)


def messagebox(message: str) -> None:
    """メッセージボックスを開き、メッセージを表示する"""

    # Python
    tk_messagebox.showinfo(title="", message=message)

    # Javascript
    # window.alert(message)


def askquestion(question: str) -> None:
    """ユーザーにYes/Noの質問を問いかけるダイアログを表示する"""

    # Python
    result = tk_messagebox.askquestion(title="", message=question)
    return result == "yes"

    # Javascript
    # return window.confirm(question)
