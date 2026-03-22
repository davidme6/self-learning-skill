# -*- coding: utf-8 -*-
# 豆包自动化 - 发送消息

from playwright.sync_api import sync_playwright
import time
import sys

# 强制 UTF-8 输出
sys.stdout.reconfigure(encoding='utf-8')

def main():
    message = "你猜猜我是谁"
    
    print("Starting Doubao automation...")
    print(f"Message: {message}")
    print()
    
    try:
        with sync_playwright() as p:
            # 启动浏览器
            print("1. Launching browser...")
            browser = p.chromium.launch(headless=False, channel="msedge")
            
            # 打开页面
            print("2. Opening new page...")
            page = browser.new_page()
            page.set_viewport_size({"width": 1920, "height": 1080})
            
            # 访问豆包
            print("3. Going to doubao.com...")
            page.goto("https://www.doubao.com", wait_until="domcontentloaded", timeout=30000)
            
            # 等待
            print("4. Waiting for page...")
            page.wait_for_timeout(5000)
            
            # 找输入框
            print("5. Finding input box...")
            selectors = [
                "textarea[placeholder]",
                "textarea",
                "[contenteditable='true']"
            ]
            
            input_box = None
            for selector in selectors:
                try:
                    input_box = page.query_selector(selector)
                    if input_box:
                        print(f"   Found: {selector}")
                        break
                except:
                    continue
            
            if not input_box:
                print("ERROR: No input box found")
                time.sleep(5)
                browser.close()
                return False
            
            # 输入消息
            print(f"6. Typing message...")
            input_box.click()
            page.wait_for_timeout(300)
            input_box.fill(message)
            page.wait_for_timeout(300)
            
            # 发送
            print("7. Sending...")
            send_btn = page.query_selector("button[type='submit'], .send-btn")
            if send_btn:
                send_btn.click()
                print("   Clicked send button")
            else:
                input_box.press("Enter")
                print("   Pressed Enter")
            
            # 等待发送
            print("8. Waiting...")
            page.wait_for_timeout(3000)
            
            print()
            print("SUCCESS! Message sent.")
            print()
            print("Browser will close in 10 seconds...")
            time.sleep(10)
            
            browser.close()
            print("Done.")
            return True
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
