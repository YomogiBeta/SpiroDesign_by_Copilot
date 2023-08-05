#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Yomogiβ'
__version__ = '1.0.0'
__date__ = '2023/07/14 (Created: 2023/07/14 )'

import subprocess
import os
import sys

EXEXUTE_SUCCSESS_CODE = 0


def run_radon_metric(metric, file_path):
    """radonを実行する。

    Args:
        metric (str): 実行するメトリクス。
        file_path (str): 対象のファイルのパス。
    """
    options = "-s" + " -a" if metric == 'cc' else ''
    command = f"radon {metric} {options} {file_path} "
    result = subprocess.run(command, capture_output=True, text=True, shell=True)

    if result.returncode == EXEXUTE_SUCCSESS_CODE:
        output = result.stdout
        return output
    else:
        error = result.stderr
        return error


if __name__ == '__main__':

    _, path, metric, execulde = sys.argv
    execulde = execulde.split(",")
    if os.path.isfile(path):
        if path.endswith(".py"):
            run_radon_metric(metric, path)
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            current_dir = os.path.basename(root)
            if current_dir in execulde:
                continue
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    result = run_radon_metric(metric, file_path)
                    if result != "":
                        print(result)
