
import os
import sys
from teams_translator.runner import run

# 切换当前目录为程序所在目录
os.chdir(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__))

if __name__ == "__main__":
    run()
