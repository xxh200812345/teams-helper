from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from pathlib import Path
import threading
import os
from datetime import datetime

from .teams_reader import read_teams_subtitles
from .openai_translator import translate_with_openai
from .config import Settings

def setup_driver():
    options = EdgeOptions()
    options.add_argument("--remote-allow-origins=*")
    options.add_argument("start-maximized")

    # 设置用户数据目录
    profile_path = Path.home() / ".teams_translator_edge"
    profile_path.mkdir(parents=True, exist_ok=True)
    options.add_argument(f"--user-data-dir={profile_path}")

    # 使用本地驱动而不是在线下载
    config = Settings().get()
    driver_path = Path(config["driver"]["edge"]["executable_path"])

    driver = webdriver.Edge(
        service=EdgeService(str(driver_path)),
        options=options
    )
    return driver

def run():
    config = Settings().get()
    os.makedirs("output", exist_ok=True)

    teams_driver = setup_driver()
    teams_driver.get(config["teams"]["url"])

    input("请在浏览器中手动登录 Teams 和 ChatGPT，然后按回车继续...")

    # 获取当前时间并格式化为字符串（例：20250702_2315）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    translated_file = config["teams"]["captions_file"].format(timestamp=timestamp)

    threading.Thread(
        target=read_teams_subtitles,
        args=(
            teams_driver,
            translated_file,
            config["teams"]["fetch_interval"]
        ),
        daemon=True
    ).start()



    # # 若后续启用翻译线程：
    # threading.Thread(
    #     target=translate_with_openai,
    #     args=(
    #         openai_driver,
    #         config["teams"]["captions_file"],
    #         config["openai"]["translated_file"],
    #         config["openai"]["translation_interval"]
    #     ),
    #     daemon=True
    # ).start()

    input("翻译进行中，按任意键退出程序...")
