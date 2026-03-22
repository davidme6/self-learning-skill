# 豆包自动化 - 改进版（带调试和更长等待）

from playwright.sync_api import sync_playwright
import time
import sys

def send_doubao_message(message="你猜猜我是谁"):
    """改进版：更长的等待时间 + 调试信息"""
    
    print("=" * 60)
    print("Doubao Automation - Improved Version")
    print("=" * 60)
    print(f"[INFO] Message: {message}")
    print()
    
    try:
        with sync_playwright() as p:
            # 1. 启动浏览器 - 添加更多参数防止崩溃
            print("[1/8] Launching browser...")
            browser = p.chromium.launch(
                headless=False, 
                channel="msedge",
                args=[
                    "--disable-gpu",
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-blink-features=AutomationControlled"
                ]
            )
            
            # 2. 创建上下文
            print("[2/8] Creating browser context...")
            context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            
            # 3. 打开页面
            print("[3/8] Opening new page...")
            page = context.new_page()
            
            # 4. 访问豆包
            print("[4/8] Navigating to doubao.com...")
            print("     (This may take a while, please wait...)")
            
            try:
                page.goto("https://www.doubao.com", wait_until="networkidle", timeout=60000)
            except Exception as e:
                print(f"     [WARN] Navigation warning: {e}")
                print("     Continuing anyway...")
            
            # 5. 等待页面稳定
            print("[5/8] Waiting for page to stabilize...")
            for i in range(10):
                page.wait_for_timeout(1000)
                print(f"     Waiting... {i+1}/10")
            
            # 6. 截图看看页面状态
            print("[6/8] Taking screenshot for debugging...")
            screenshot_path = "doubao_debug.png"
            page.screenshot(path=screenshot_path)
            print(f"     Screenshot saved: {screenshot_path}")
            
            # 7. 查找输入框
            print("[7/8] Finding input box...")
            input_box = None
            
            selectors = [
                "textarea[placeholder*='输入']",
                "textarea[placeholder*='消息']",
                "textarea[placeholder]",
                "[contenteditable='true']",
                ".input-box textarea",
                "#chat-input",
                "textarea"
            ]
            
            for selector in selectors:
                try:
                    input_box = page.query_selector(selector)
                    if input_box:
                        print(f"     [OK] Found with: {selector}")
                        break
                except Exception as e:
                    print(f"     [SKIP] {selector}: {e}")
                    continue
            
            if not input_box:
                print()
                print("[ERROR] Could not find input box!")
                print("[INFO] Check the screenshot: doubao_debug.png")
                print("[INFO] You may need to login manually first.")
                print()
                print("[KEEPING BROWSER OPEN]")
                print("Close it manually when done.")
                
                # 保持浏览器打开让用户手动操作
                print("Browser will stay open for 60 seconds...")
                time.sleep(60)
                browser.close()
                return False
            
            # 8. 输入并发送
            print("[8/8] Typing and sending message...")
            input_box.click()
            page.wait_for_timeout(500)
            input_box.fill(message)
            page.wait_for_timeout(500)
            
            # 尝试点击发送按钮
            send_button = page.query_selector("button[class*='send'], .send-btn, [aria-label*='发送'], button[type='submit']")
            
            if send_button:
                send_button.click()
                print("     [OK] Clicked send button")
            else:
                input_box.press("Enter")
                print("     [OK] Pressed Enter")
            
            # 等待消息发送
            print("     Waiting for message to send...")
            page.wait_for_timeout(5000)
            
            # 再截一张图
            page.screenshot(path="doubao_success.png")
            print("     Success screenshot saved: doubao_success.png")
            
            print()
            print("=" * 60)
            print("SUCCESS! Message sent to Doubao")
            print("=" * 60)
            print()
            print("[INFO] Browser will stay open for 15 seconds...")
            print("Check the screenshots if something went wrong.")
            time.sleep(15)
            
            browser.close()
            print("[DONE] Browser closed")
            
            return True
            
    except Exception as e:
        print()
        print("=" * 60)
        print(f"FAILED: {e}")
        print("=" * 60)
        return False

if __name__ == "__main__":
    success = send_doubao_message("你猜猜我是谁")
    sys.exit(0 if success else 1)
