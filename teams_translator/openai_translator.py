from selenium.webdriver.common.by import By
import pyautogui
import time

from teams_translator.config import Settings

import time
import pyautogui
import pyperclip

def translate_with_openai(bw, input_file, output_file, interval=10):
    last_lines_no = 0

    while True:
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            new_lines = lines[last_lines_no:]
            last_lines_no = len(lines)

            if new_lines:
                # 组织翻译文本并复制到剪切板
                text_to_translate = ''.join(new_lines).strip() + "：总结，用中文回复"
                pyperclip.copy(text_to_translate)

                # 切换到 ChatGPT 页面
                bw.switch_to.window(bw.window_handles[0])
                time.sleep(1)

                # 将输入框激活并粘贴内容
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.5)
                pyautogui.press('enter')
                print("[Translator] 内容发送成功")

                # 等待 ChatGPT 回复完成（粗略估算）
                time.sleep(10)

                # 查找“复制”按钮图标，重复尝试直到找到
                copy_btn_path = "copy_button.png"  # 你需准备这个图像模板
                copied = False
                for _ in range(10):
                    pos = pyautogui.locateCenterOnScreen(copy_btn_path, confidence=0.8)
                    if pos:
                        pyautogui.moveTo(pos)
                        pyautogui.click()
                        time.sleep(0.5)
                        translated = pyperclip.paste()
                        with open(output_file, 'a', encoding='utf-8') as f:
                            f.write(translated + "\n")
                        print("[Translator] 翻译写入成功")
                        copied = True
                        break
                    else:
                        time.sleep(1)

                if not copied:
                    print("[Translator] 未找到复制按钮，跳过")

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
