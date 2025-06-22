from selenium.webdriver.common.by import By
import time
from teams_translator.config import Settings


def read_teams_subtitles(driver, output_file, interval=5):
    seen = set()
    config = Settings().get()
    xpath = config["teams"]["xpath"]

    while True:
        try:
            list_elem = driver.find_element(By.XPATH, xpath["list"])
            blocks = list_elem.find_elements(By.XPATH, f"{xpath['author']}/ancestor::div[2]")

            with open(output_file, 'a', encoding='utf-8') as f:
                for block in blocks[:-1]:  # 不处理最后一条
                    try:
                        author = block.find_element(By.XPATH, xpath["author"]).text.strip()
                        text = block.find_element(By.XPATH, xpath["text"]).text.strip()
                        line = f"{author}: {text}"
                        if line not in seen:
                            seen.add(line)
                            print(line)
                            f.write(line + "\n")
                    except Exception:
                        continue
        except Exception as e:
            print(f"[Teams Reader] Error: {{e}}")

        time.sleep(interval)
