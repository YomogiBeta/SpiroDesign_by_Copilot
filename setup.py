import sys
import os
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["tkinter", "pygame", "numpy"],
    "excludes": ["autopep8",
                 "pep8-naming",
                 "transcrypt",
                 "cx_Freeze",
                 "unittest",
                 "email",
                 "html",
                 "http",
                 "xml",
                 "xmlrpc",
                 "urll",
                 "radon"],
    'include_files': ["resource"],
    "path": sys.path + [f"{os.getcwd()}/src"],
}

bdist_mac_options = {
    "iconfile": "resource/spirodesign.ico",
    "bundle_name": "SpiroDesign_by_Copilot",
}

bdist_dmg_options = {
    "volume_label": "SpiroDesign Installer",
    "applications_shortcut": True,
}

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="SpiroDesign_by_Copilot",
    version="1.0.0",
    description="Project Copilot's SpiroDesign by standalone",
    options={"build_exe": build_exe_options, "bdist_mac": bdist_mac_options, "bdist_dmg": bdist_dmg_options},
    executables=[Executable("src/main.py",
                            icon="resource/spirodesign.ico",
                            base=base,
                            shortcut_name="SpiroDesign_by_Copilot",
                            shortcut_dir="DesktopFolder")],
)
