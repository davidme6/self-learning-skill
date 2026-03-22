# Playwright 豆包自动化 - 带重试和错误处理

from playwright.sync_api import sync_playwright, TimeoutError
import time
import sys

def send_doubao_message(message="你猜猜我是谁"):
    """使用 Playwright 自动化豆包网页，带重试机制"""
    
    print("=" * 60)
    print("Doubao Automation - Playwright")
    print("=" * 60)
    print(f"[INFO] Message: {message}")
    print()
    
    max_retries = 2
    retry_count = 0
    
    while retry_count <= max_retries:
        try:
            with sync_playwright() as p:
                # 1. 启动浏览器
                print(f"[{retry_count + 1}/{max_retries + 1}] Launching browser...")
                browser = p.chromium.launch(
                    headless=False, 
                    channel="msedge",
                    args=["--disable-blink-features=AutomationControlled"]
                )
                
                # 2. 打开新页面
                print("  Opening new page...")
                page = browser.new_page()
                
                # 设置视口
                page.set_viewport_size({"width": 1920, "height": 1080})
                
                # 3. 访问豆包
                print("  Navigating to https://www.doubao.com...")
                page.goto("https://www.doubao.com", wait_until="domcontentloaded", timeout=30000)
                
                # 4. 等待页面加载
                print("  Waiting for page to stabilize...")
                page.wait_for_timeout(5000)
                
                # 5. 查找输入框
                print("  Finding input box...")
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
                            print(f"  [OK] Found with: {selector}")
                            break
                    except:
                        continue
                
                if not input_box:
                    raise Exception("Could not find input box")
                
                # 6. 输入消息
                print(f"  Typing: {message}...")
                input_box.click()
                page.wait_for_timeout(500)
                input_box.fill(message)
                page.wait_for_timeout(500)
                
                # 7. 发送
                print("  Sending message...")
                send_button = page.query_selector("button[class*='send'], .send-btn, [aria-label*='发送'], button[type='submit']")
                
                if send_button:
                    send_button.click()
                    print("  [OK] Clicked send button")
                else:
                    input_box.press("Enter")
                    print("  [OK] Pressed Enter")
                
                # 8. 等待消息发送
                print("  Waiting for message to send...")
                page.wait_for_timeout(3000)
                
                print()
                print("=" * 60)
                print("SUCCESS! Message sent to Doubao")
                print("=" * 60)
                
                # 保持浏览器打开查看结果
                print()
                print("[INFO] Browser will close in 10 seconds...")
                time.sleep(10)
                
                browser.close()
                print("[DONE] Browser closed")
                
                return True
                
        except Exception as e:
            error_msg = str(e)
            print()
            print(f"[ERROR] Attempt {retry_count + 1} failed: {error_msg}")
            
            retry_count += 1
            
            if retry_count <= max_retries:
                print("[INFO] Retrying in 3 seconds...")
                time.sleep(3)
            else:
                print()
                print("=" * 60)
                print("FAILED after all retries")
                print("=" * 60)
                print()
                print("Possible causes:")
                print("  1. Network/proxy issue")
                print("  2. Website structure changed")
                print("  3. Login required")
                print()
                return False

if __name__ == "__main__":
    success = send_doubao_message("你猜猜我是谁")
    sys.exit(0 if success else 1)
