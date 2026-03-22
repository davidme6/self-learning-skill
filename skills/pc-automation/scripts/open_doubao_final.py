# 豆包自动化 - 最终版（可靠发送 + 捕获回复）

from playwright.sync_api import sync_playwright
import time
import sys

def send_doubao_and_get_reply(message="你猜猜我是谁"):
    """发送消息并等待豆包回复 - 最终可靠版"""
    
    print("=" * 60)
    print("Doubao Automation - Final Version")
    print("=" * 60)
    print(f"[INFO] Sending: {message}")
    print()
    
    reply_content = None
    
    try:
        with sync_playwright() as p:
            # 启动浏览器
            print("[1/7] Launching browser...")
            browser = p.chromium.launch(
                headless=False, 
                channel="msedge",
                args=[
                    "--disable-gpu",
                    "--no-sandbox",
                    "--disable-dev-shm-usage"
                ]
            )
            
            print("[2/7] Creating context and page...")
            context = browser.new_context(viewport={"width": 1920, "height": 1080})
            page = context.new_page()
            
            # 访问豆包
            print("[3/7] Going to doubao.com...")
            page.goto("https://www.doubao.com", wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(8000)  # 等页面完全加载
            
            # 找输入框
            print("[4/7] Finding input box...")
            input_box = page.locator("textarea[placeholder*='消息'], textarea[placeholder*='输入'], textarea").first
            
            if not input_box.is_visible(timeout=5000):
                print("[ERROR] Input box not found!")
                browser.close()
                return None
            
            print("     Input box found!")
            
            # 输入消息
            print("[5/7] Typing message...")
            input_box.click()
            page.wait_for_timeout(300)
            input_box.fill(message)
            page.wait_for_timeout(300)
            
            # 找发送按钮并点击
            print("[6/7] Sending message...")
            
            # 先试试找发送按钮
            send_btn = page.locator("button[class*='send'], [aria-label*='发送'], button[type='submit']").first
            
            try:
                if send_btn.is_visible(timeout=3000):
                    send_btn.click()
                    print("     Clicked send button")
                else:
                    input_box.press("Enter")
                    print("     Pressed Enter")
            except:
                input_box.press("Enter")
                print("     Pressed Enter (fallback)")
            
            # 等待并捕获回复
            print("[7/7] Waiting for reply (up to 90 seconds)...")
            print()
            
            page.wait_for_timeout(3000)  # 先等 3 秒让消息显示出来
            
            # 截图看看
            page.screenshot(path="doubao_after_send.png")
            print("     Screenshot saved: doubao_after_send.png")
            
            # 尝试找 AI 回复
            # 豆包的回复通常在对话历史里
            reply = None
            
            for attempt in range(18):  # 最多等 90 秒
                page.wait_for_timeout(5000)
                print(f"     Checking... {((attempt+1)*5)}s/90s")
                
                # 截图检查
                page.screenshot(path=f"doubao_check_{attempt+1}.png")
                
                # 尝试各种选择器
                selectors = [
                    ".message-ai .message-content",
                    ".assistant-message",
                    "[class*='assistant'] .content",
                    ".reply-content",
                    ".message-content",
                ]
                
                for sel in selectors:
                    try:
                        elements = page.locator(sel).all()
                        if elements:
                            last = elements[-1]
                            text = last.inner_text()
                            if text and len(text) > 10 and "豆包" not in text:
                                reply = text
                                print(f"     [OK] Reply found!")
                                break
                    except:
                        pass
                
                if reply:
                    break
            
            # 输出结果
            print()
            if reply:
                print("=" * 60)
                print("DOUBAO'S REPLY:")
                print("=" * 60)
                print(reply)
                print("=" * 60)
                reply_content = reply
            else:
                print("[INFO] No reply captured in 90 seconds")
                print("[INFO] Check screenshots: doubao_after_send.png, doubao_check_*.png")
            
            # 保持浏览器打开一会儿
            print()
            print("[INFO] Keeping browser open for 10 seconds...")
            time.sleep(10)
            browser.close()
            
            return reply_content
            
    except Exception as e:
        print()
        print("=" * 60)
        print(f"ERROR: {e}")
        print("=" * 60)
        return None

if __name__ == "__main__":
    reply = send_doubao_and_get_reply("你猜猜我是谁")
    sys.exit(0 if reply else 1)
