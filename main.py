from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from pathlib import Path
import threading
import os

from teams_translator.teams_reader import read_teams_subtitles
from teams_translator.openai_translator import translate_with_openai
from teams_translator.config import Settings

def setup_driver():
    options = EdgeOptions()
    options.add_argument("--remote-allow-origins=*")
    options.add_argument("start-maximized")

    # 设置用户数据目录
    profile_path = Path.home() / ".teams_translator_edge"
    profile_path.mkdir(parents=True, exist_ok=True)
    options.add_argument(f"--user-data-dir={profile_path}")

    # 启动 Edge
    driver = webdriver.Edge(
        service=EdgeService(EdgeChromiumDriverManager().install()),
        options=options
    )
    return driver

def main():
    config = Settings().get()

    # 创建 output 文件夹
    os.makedirs("output", exist_ok=True)

    teams_driver = setup_driver()

    teams_driver.get(config["teams"]["url"])

    input("请在浏览器中手动登录 Teams 和 ChatGPT，然后按回车继续...")

    threading.Thread(
        target=read_teams_subtitles,
        args=(
            teams_driver,
            config["teams"]["captions_file"],
            config["teams"]["fetch_interval"]
        ),
        daemon=True
    ).start()

    # threading.Thread(
    #     target=translate_with_openai,
    #     args=(
    #         openai_driver,
    #         config.get("teams.captions_file"),
    #         config.get("openai.translated_file"),
    #         config.get("openai.translation_interval")
    #     ),
    #     daemon=True
    # ).start()

    input("翻译进行中，按任意键退出程序...")

if __name__ == "__main__":
    main()
