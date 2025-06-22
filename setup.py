from cx_Freeze import setup, Executable
import sys
import os

# 判断平台，用于图标或其他平台特定设置
base = None
if sys.platform == "win32":
    base = "Console"  # 或 "Win32GUI" 如果你不想显示控制台窗口

build_exe_options = {
    "packages": [
        "os", "sys", "time", "selenium", "webdriver_manager", "yaml"
    ],
    "includes": [],
    "include_files": [
        "settings.yaml"    # 配置文件
    ],
    "excludes": [
        "tkinter", "unittest", "email", "html", "http", "xmlrpc"
    ],
    "optimize": 2
}

setup(
    name="TeamsRealTimeTranslator",
    version="1.0",
    description="Real-time subtitle translator for Microsoft Teams using ChatGPT",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)]
)
