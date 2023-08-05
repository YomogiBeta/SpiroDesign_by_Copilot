#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PythonとJavascriptへのトランスコンパイル用Pythonコードが書かれたPythonファイル(bridge)の実装を切り替えるプログラム。
bridgeファイルには特定の機能の双方に依存した実装が記載されており、どちらかがコメントアウトされていない時、もう一方をコメントアウトする。
その切り替えを自動で行うプログラムである。
bridgeファイルを利用すると、Python実行時の依存実装とトランスコンパイル後のJavascript実行時の依存実装をプログラマが意識することなく利用できる。
"""

__author__ = 'Yomogiβ'
__version__ = '1.0.1'
__date__ = '2023/07/09 (Created: 2023/04/27 )'

import sys
import os


def is_target_comment(line: str, target: str) -> bool:
    """与えられた文字列がtargetであるかどうかを返す。

    Args:
        line (str): 対象の文字列。

    Returns:
        bool: targetである場合はTrue、それ以外の場合はFalse。
    """
    return target in line


def is_empty(line: str) -> bool:
    """与えられた文字列が空行であるかどうかを返す。

    Args:
        line (str): 対象の文字列。

    Returns:
        bool: 空行である場合はTrue、それ以外の場合はFalse。
    """
    return line.strip() == ""


def is_commented(line: str) -> bool:
    """与えられた文字列がコメントアウトされているかどうかを判定する。

    Args:
        line (str): 対象の文字列。

    Returns:
        bool: コメントアウトされている場合はTrue、それ以外の場合はFalse。
    """
    line = line.strip()
    return line.startswith("#")


def uncomment_target(file_path: str, target: str) -> None:
    """Pythonファイルからtargetの文字列を見つかった場合、空行が見つかるまでコメントアウトを外し、結果をファイルに上書き保存する。

    Args:
        file_path (str): 対象のファイルのパス。

    Returns:
        None.
    """
    # 読み込みモードでファイルを開く
    with open(file_path, 'r', encoding="utf-8") as f:
        lines = f.readlines()

    # 結果を書き込むためにファイルを開く
    with open(file_path, 'w', encoding="utf-8") as f:
        js_found = False
        for line in lines:
            if is_target_comment(line, target):
                js_found = True
            elif js_found and is_empty(line):
                js_found = False
            elif js_found:
                line = line.replace("# ", "", 1)
            f.write(line)


def add_comment(line: str) -> str:
    """ソースコードのインデントを維持しながらコメントをつける

    Args:
        line (str): コメントを追加する対象の文字列。

    Returns:
        str: コメントを追加した文字列。
    """
    index = len(line) - len(line.lstrip())
    return line[:index] + "# " + line[index:]


def comment_target(file_path: str, target: str):
    """Pythonファイルからtargetの文字列が見つかった場合、空行が見つかるまでコメントアウトをつけ、結果をファイルに上書き保存する。

    Args:
        file_path (str): 対象のファイルのパス。

    Returns:
        None.
    """
    # 読み込みモードでファイルを開く
    with open(file_path, 'r', encoding="utf-8") as f:
        lines = f.readlines()

    # 結果を書き込むためにファイルを開く
    with open(file_path, 'w', encoding="utf-8") as f:
        py_found = False
        for line in lines:
            if is_target_comment(line, target):
                py_found = True
            elif py_found and is_empty(line):
                py_found = False
            elif py_found & (not is_commented(line)):
                line = add_comment(line)
            f.write(line)


JAVASCRTIPT_COMMENT = "# Javascript"
PYTHON_COMMENT = "# Python"
if __name__ == "__main__":
    args = sys.argv
    _, path, target = args
    uncomment_text = ""
    comment_text = ""

    if target == "javascript":
        uncomment_text = JAVASCRTIPT_COMMENT
        comment_text = PYTHON_COMMENT
    elif target == "python":
        uncomment_text = PYTHON_COMMENT
        comment_text = JAVASCRTIPT_COMMENT
    else:
        raise ValueError("target error")

    if os.path.isfile(path):
        uncomment_target(path, uncomment_text)
        comment_target(path, comment_text)
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    uncomment_target(file_path, uncomment_text)
                    comment_target(file_path, comment_text)
    else:
        raise ValueError("File or directory not found")
