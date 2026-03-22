# 豆包自动化 - 精确点击发送按钮版

from playwright.sync_api import sync_playwright
import time
import sys

def send_doubao_and_get_reply(message="你猜猜我是谁"):
    """精确点击发送按钮"""
    
    print("=" * 60)
    print("Doubao Automation - Click Send Button")
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
            
            print("[4/8] Finding input box...")
            # 更精确的选择器
            input_box = page.locator("textarea")
            
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
            
            # 截图看看发送按钮位置
            page.screenshot(path="doubao_before_click.png")
            print("     Screenshot: doubao_before_click.png")
            
            # 找发送按钮 - 蓝色圆形按钮
            # 尝试多种选择器
            send_btn = None
            
            # 方法 1: 找蓝色发送按钮 (通常有 send 或 arrow 图标)
            try:
                send_btn = page.locator("button[class*='send'], button[aria-label*='发送']").first
                if send_btn.is_visible(timeout=3000):
                    print("     Found send button (method 1)")
                else:
                    send_btn = None
            except:
                send_btn = None
            
            # 方法 2: 找输入框右边的蓝色按钮
            if not send_btn:
                try:
                    # 找输入框容器里的按钮
                    send_btn = page.locator(".input-box button, .composer button, [class*='composer'] button").last
                    if send_btn.is_visible(timeout=3000):
                        print("     Found send button (method 2)")
                    else:
                        send_btn = None
                except:
                    send_btn = None
            
            # 方法 3: 找最后一个按钮（通常是发送）
            if not send_btn:
                try:
                    all_buttons = page.locator("button").all()
                    # 通常发送按钮是最后一个
                    send_btn = all_buttons[-1]
                    print("     Found send button (method 3 - last button)")
                except:
                    send_btn = None
            
            # 方法 4: 直接按坐标点击（最后手段）
            if not send_btn:
                print("     [WARN] Could not locate send button, trying Enter key...")
                input_box.press("Enter")
            else:
                # 点击发送
                print("     Clicking send button...")
                send_btn.click()
                print("     Clicked!")
            
            page.wait_for_timeout(1000)
            
            # 截图检查
            page.screenshot(path="doubao_after_click.png")
            print("     Screenshot: doubao_after_click.png")
            
            print("[7/8] Waiting for reply...")
            
            reply = None
            
            # 等待回复，最多 60 秒
            for attempt in range(12):
                page.wait_for_timeout(5000)
                print(f"     Waiting... {((attempt+1)*5)}s/60s")
                
                # 截图
                page.screenshot(path=f"doubao_wait_{attempt+1}.png")
                
                # 找回复消息
                try:
                    # 豆包的回复通常在对话气泡里
                    messages = page.locator(".message-content, .message-ai, .assistant-message, [class*='message']").all()
                    
                    if messages:
                        # 检查最后一条消息
                        last_msg = messages[-1]
                        text = last_msg.inner_text()
                        
                        # 排除用户自己的消息和空消息
                        if text and len(text) > 20 and message not in text:
                            reply = text
                            print(f"     [OK] Reply found!")
                            break
                except Exception as e:
                    print(f"     [DEBUG] Check failed: {e}")
                    continue
            
            print("[8/8] Extracting reply...")
            print()
            
            if reply:
                print("=" * 60)
                print("DOUBAO REPLIED:")
                print("=" * 60)
                print(reply)
                print("=" * 60)
                reply_content = reply
            else:
                print("[INFO] No reply captured")
                print("[INFO] Check screenshots for debugging")
            
            print()
            print("[INFO] Browser open for 10 more seconds...")
            time.sleep(10)
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
