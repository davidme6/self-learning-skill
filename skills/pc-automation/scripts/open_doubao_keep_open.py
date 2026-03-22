# 豆包自动化 - 最终版（保持浏览器打开）

from playwright.sync_api import sync_playwright
import time
import sys

def send_doubao_and_get_reply(message="你猜猜我是谁"):
    """发送消息并保持浏览器打开"""
    
    print("=" * 60)
    print("Doubao Automation - Keep Browser Open")
    print("=" * 60)
    print(f"[INFO] Sending: {message}")
    print()
    
    try:
        with sync_playwright() as p:
            print("[1/6] Launching browser...")
            browser = p.chromium.launch(
                headless=False, 
                channel="msedge",
                args=["--disable-gpu", "--no-sandbox"]
            )
            
            print("[2/6] Creating page...")
            context = browser.new_context(viewport={"width": 1920, "height": 1080})
            page = context.new_page()
            
            print("[3/6] Going to doubao.com...")
            page.goto("https://www.doubao.com", wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(5000)
            
            print("[4/6] Finding input box...")
            input_box = page.locator('[data-testid="chat_input_input"]')
            
            if not input_box.is_visible(timeout=5000):
                print("[ERROR] Input box not found!")
                return None
            
            print("     Input box found!")
            
            print("[5/6] Typing and sending message...")
            input_box.click()
            page.wait_for_timeout(300)
            input_box.fill(message)
            page.wait_for_timeout(300)
            
            # 尝试点击发送按钮
            send_btn = None
            try:
                send_btn = page.locator('button[type="submit"], button[aria-label*="发送"]').first
                if send_btn.is_visible(timeout=2000):
                    send_btn.click()
                    print("     Clicked send button")
                else:
                    input_box.press("Enter")
                    print("     Pressed Enter")
            except:
                input_box.press("Enter")
                print("     Pressed Enter (fallback)")
            
            print("[6/6] Waiting for reply (up to 30 seconds)...")
            page.wait_for_timeout(3000)
            
            # 等待回复
            for i in range(6):
                page.wait_for_timeout(5000)
                print(f"     Waiting... {((i+1)*5)}s/30s")
                
                # 尝试找回复
                try:
                    messages = page.locator('.message-ai .message-content, .assistant-message').all()
                    if messages:
                        last = messages[-1]
                        text = last.inner_text()
                        if text and len(text) > 20:
                            print()
                            print("=" * 60)
                            print("DOUBAO REPLIED:")
                            print("=" * 60)
                            print(text)
                            print("=" * 60)
                            break
                except:
                    pass
            
            print()
            print("=" * 60)
            print("DONE! Browser will STAY OPEN for you to check.")
            print("=" * 60)
            print()
            print("Check the browser window to see if Doubao replied!")
            print("Close the browser manually when you're done.")
            print()
            
            # 保持浏览器打开，等待用户手动关闭
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n[INFO] Closing browser...")
                browser.close()
            
    except Exception as e:
        print()
        print("=" * 60)
        print(f"ERROR: {e}")
        print("=" * 60)

if __name__ == "__main__":
    send_doubao_and_get_reply("你猜猜我是谁")
