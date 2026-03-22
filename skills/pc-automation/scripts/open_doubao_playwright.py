# 打开豆包网页并发送消息 - Playwright 版本（最快）

from playwright.sync_api import sync_playwright
import time

def send_doubao_message(message="你好"):
    """使用 Playwright 自动化豆包网页"""
    
    print("[INFO] Starting Playwright automation...")
    print(f"[INFO] Message: {message}")
    print()
    
    with sync_playwright() as p:
        # 1. 启动浏览器（Edge）
        print("  1. Launching browser...")
        browser = p.chromium.launch(headless=False, channel="msedge")
        
        # 2. 打开新页面
        print("  2. Opening new page...")
        page = browser.new_page()
        
        # 3. 访问豆包
        print("  3. Navigating to Doubao...")
        page.goto("https://www.doubao.com", wait_until="networkidle")
        
        # 4. 等待页面加载
        print("  4. Waiting for page to load...")
        page.wait_for_timeout(3000)
        
        # 5. 查找输入框（多种选择器尝试）
        print("  5. Finding input box...")
        input_box = None
        
        selectors = [
            "textarea[placeholder*='输入']",
            "textarea[placeholder*='消息']",
            "textarea",
            "[contenteditable='true']",
            ".input-box textarea",
            "#chat-input"
        ]
        
        for selector in selectors:
            try:
                input_box = page.query_selector(selector)
                if input_box:
                    print(f"     Found: {selector}")
                    break
            except:
                continue
        
        if input_box:
            # 6. 输入消息
            print("  6. Typing message...")
            input_box.fill(message)
            
            # 7. 查找发送按钮
            print("  7. Finding send button...")
            send_button = page.query_selector("button[class*='send'], .send-btn, [aria-label*='发送']")
            
            if send_button:
                print("  8. Clicking send button...")
                send_button.click()
            else:
                print("  8. Pressing Enter...")
                input_box.press("Enter")
            
            print()
            print("[SUCCESS] Message sent!")
        else:
            print("[ERROR] Could not find input box")
            print("[INFO] Trying keyboard fallback...")
            
            # 回退方案：用键盘导航
            for i in range(10):
                page.keyboard.press("Tab")
                time.sleep(0.1)
            
            page.keyboard.type(message)
            page.keyboard.press("Enter")
            print("[SUCCESS] Sent via keyboard fallback")
        
        # 保持浏览器打开几秒查看结果
        print()
        print("[INFO] Keeping browser open for 5 seconds...")
        time.sleep(5)
        
        browser.close()
        print("[DONE] Browser closed")

if __name__ == "__main__":
    send_doubao_message("你好")
