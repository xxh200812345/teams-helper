from selenium.webdriver.common.by import By
import time

from teams_translator.config import Settings

def translate_with_openai(driver, input_file, output_file, interval=10):
    last_lines = []
    while True:
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            new_lines = [line for line in lines if line not in last_lines]
            last_lines.extend(new_lines)

            for line in new_lines:
                if line.strip():
                    input_box = driver.find_element(By.TAG_NAME, 'textarea')
                    input_box.clear()
                    input_box.send_keys(line.strip())
                    input_box.send_keys("\n")
                    time.sleep(5)

                    responses = driver.find_elements(By.CSS_SELECTOR, '.prose p')
                    if responses:
                        translated = responses[-1].text.strip()
                        with open(output_file, 'a', encoding='utf-8') as out:
                            out.write(translated + "\n")
        except Exception as e:
            print(f"[Translator] Error: {e}")
        time.sleep(interval)

def read_teams_subtitles(driver, output_file, interval=5):
    seen = set()
    config = Settings().get()
    

    while True:
        try:
            # 找字幕容器
            list_container = driver.find_element(By.XPATH, ".//div[@data-tid='closed-caption-v2-virtual-list-content']")

            # 获取每一条字幕项（以包含 author 的 span 向上找父div为基准）
            caption_blocks = list_container.find_elements(By.XPATH, ".//span[@data-tid='author']/ancestor::div[1]")

            with open(output_file, 'a', encoding='utf-8') as f:
                for block in caption_blocks:
                    try:
                        author = block.find_element(By.XPATH, ".//span[@data-tid='author']").text.strip()
                        text = block.find_element(By.XPATH, ".//span[@data-tid='closed-caption-text']").text.strip()
                        pair = f"{author}: {text}"
                        if pair not in seen:
                            seen.add(pair)
                            f.write(pair + '\n')
                            print(pair)
                    except Exception:
                        continue

        except Exception as e:
            print(f"[Teams Reader] Error: {e}")

        time.sleep(interval)
