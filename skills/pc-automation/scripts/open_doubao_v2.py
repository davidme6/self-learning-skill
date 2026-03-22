# 豆包自动化 - 使用 data-testid 精确定位

from playwright.sync_api import sync_playwright
import time
import sys

def send_doubao_and_get_reply(message="你猜猜我是谁"):
    """使用 data-testid 精确定位输入框"""
    
    print("=" * 60)
    print("Doubao Automation - Precise Locator")
    print("=" * 60)
    print(f"[INFO] Sending: {message}")
    print()
    
    reply_content = None
    
    try:
        with sync_playwright() as p:
            print("[1/8] Launching browser...")
            browser = p.chromium.launch(
                headless=False, 
                channel="msedge",
                args=["--disable-gpu", "--no-sandbox"]
            )
            
            print("[2/8] Creating page...")
            context = browser.new_context(viewport={"width": 1920, "height": 1080})
            page = context.new_page()
            
            print("[3/8] Going to doubao.com...")
            page.goto("https://www.doubao.com", wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(8000)
            
            print("[4/8] Finding input box (using data-testid)...")
            
            # 使用 data-testid 精确定位（从错误信息看到的）
            input_box = page.locator('[data-testid="chat_input_input"]')
            
            if not input_box.is_visible(timeout=5000):
                print("[ERROR] Input box not found!")
                browser.close()
                return None
            
            print("     Input box found!")
            
            print("[5/8] Typing message...")
            input_box.click()
            page.wait_for_timeout(500)
            input_box.fill(message)
            page.wait_for_timeout(500)
            
            print("[6/8] Clicking SEND BUTTON...")
            
            # 截图
            page.screenshot(path="doubao_before_send.png")
            
            # 找发送按钮 - 使用更精确的选择器
            send_btn = None
            
            # 方法 1: 找输入框容器内的发送按钮
            try:
                # 豆包的发送按钮通常在输入框右边，是个蓝色圆形按钮
                send_btn = page.locator('button[class*="send"], button[aria-label*="发送"], button[type="submit"]').first
                if send_btn.is_visible(timeout=3000):
                    print("     Found send button (method 1)")
                else:
                    send_btn = None
            except:
                send_btn = None
            
            # 方法 2: 找输入框同级的按钮
            if not send_btn:
                try:
                    send_btn = page.locator('.semi-input-textarea-autosize + button, .semi-input-textarea-autosize ~ button').first
                    if send_btn.is_visible(timeout=3000):
                        print("     Found send button (method 2)")
                    else:
                        send_btn = None
                except:
                    send_btn = None
            
            # 方法 3: 使用坐标点击（最后手段）
            if not send_btn:
                print("     [WARN] Send button not found, using Enter key...")
                input_box.press("Enter")
            else:
                print("     Clicking send button...")
                send_btn.click()
                print("     Clicked!")
            
            page.wait_for_timeout(1000)
            page.screenshot(path="doubao_after_send.png")
            print("     Screenshots saved")
            
            print("[7/8] Waiting for reply (up to 60 seconds)...")
            
            reply = None
            
            for attempt in range(12):
                page.wait_for_timeout(5000)
                print(f"     Waiting... {((attempt+1)*5)}s/60s")
                
                page.screenshot(path=f"doubao_check_{attempt+1}.png")
                
                # 找回复
                try:
                    # 尝试多种选择器
                    selectors = [
                        '.message-ai .message-content',
                        '.assistant-message',
                        '[class*="assistant"] .content',
                        '.reply-content',
                        '[data-testid*="message"]',
                    ]
                    
                    for sel in selectors:
                        try:
                            elements = page.locator(sel).all()
                            if elements:
                                last = elements[-1]
                                text = last.inner_text()
                                if text and len(text) > 20 and message not in text:
                                    reply = text
                                    print(f"     [OK] Reply found with: {sel}")
                                    break
                        except:
                            pass
                    
                    if reply:
                        break
                except Exception as e:
                    print(f"     [DEBUG] Check failed: {e}")
                    continue
            
            print("[8/8] Result...")
            print()
            
            if reply:
                print("=" * 60)
                print("DOUBAO REPLIED:")
                print("=" * 60)
                print(reply)
                print("=" * 60)
                reply_content = reply
            else:
                print("[INFO] No reply captured in 60 seconds")
                print("[INFO] Check screenshots: doubao_*.png")
            
            print()
            print("[INFO] ✅ DONE! Browser will stay OPEN for you to check.")
            print("[INFO] Close it manually when you're done.")
            print()
            
            # 保持浏览器打开，等待用户手动关闭
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n[INFO] User closed browser")
                browser.close()
            
            return reply_content
            
    except Exception as e:
        print()
        print("=" * 60)
        print(f"ERROR: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    reply = send_doubao_and_get_reply("你猜猜我是谁")
    sys.exit(0 if reply else 1)
