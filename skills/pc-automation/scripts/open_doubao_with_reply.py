# 豆包自动化 - 带回复捕获

from playwright.sync_api import sync_playwright
import time
import sys

def send_doubao_and_get_reply(message="你猜猜我是谁"):
    """发送消息并等待豆包回复"""
    
    print("=" * 60)
    print("Doubao Automation - With Reply Capture")
    print("=" * 60)
    print(f"[INFO] Message: {message}")
    print()
    
    reply_content = None
    
    try:
        with sync_playwright() as p:
            # 1. 启动浏览器
            print("[1/9] Launching browser...")
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
            print("[2/9] Creating browser context...")
            context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            
            # 3. 打开页面
            print("[3/9] Opening new page...")
            page = context.new_page()
            
            # 4. 访问豆包
            print("[4/9] Navigating to doubao.com...")
            try:
                page.goto("https://www.doubao.com", wait_until="domcontentloaded", timeout=60000)
            except Exception as e:
                print(f"     [WARN] Navigation warning: {e}")
            
            # 5. 等待页面稳定
            print("[5/9] Waiting for page to stabilize...")
            page.wait_for_timeout(10000)
            
            # 6. 查找输入框
            print("[6/9] Finding input box...")
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
                except:
                    continue
            
            if not input_box:
                print("[ERROR] Could not find input box!")
                print("[INFO] May need manual login first.")
                browser.close()
                return None
            
            # 7. 输入并发送
            print("[7/9] Typing and sending message...")
            input_box.click()
            page.wait_for_timeout(500)
            input_box.fill(message)
            page.wait_for_timeout(500)
            
            # 发送
            send_button = page.query_selector("button[class*='send'], .send-btn, [aria-label*='发送'], button[type='submit']")
            if send_button:
                send_button.click()
            else:
                input_box.press("Enter")
            
            print("     Message sent! Waiting for Doubao's reply...")
            
            # 8. 等待豆包回复（最长 60 秒）
            print("[8/9] Waiting for reply (up to 60 seconds)...")
            print()
            
            reply_selectors = [
                ".message-ai",
                ".assistant-message",
                "[class*='assistant']",
                "[class*='reply']",
                ".message-content",
                "div[class*='message']:last-of-type"
            ]
            
            reply_element = None
            max_wait = 60
            check_interval = 2
            
            for i in range(0, max_wait, check_interval):
                page.wait_for_timeout(check_interval * 1000)
                print(f"     Waiting... {i+check_interval}s/{max_wait}s")
                
                # 尝试找回复
                for selector in reply_selectors:
                    try:
                        elements = page.query_selector_all(selector)
                        if elements:
                            # 找最后一个（最新的回复）
                            last_element = elements[-1]
                            # 检查是否包含"AI"或"助手"相关标记
                            if last_element.is_visible():
                                reply_element = last_element
                                print(f"     [OK] Found reply with: {selector}")
                                break
                    except:
                        continue
                
                if reply_element:
                    break
            
            # 9. 提取回复内容
            print("[9/9] Extracting reply content...")
            
            if reply_element:
                try:
                    # 截图
                    page.screenshot(path="doubao_reply.png")
                    print("     Reply screenshot saved: doubao_reply.png")
                    
                    # 尝试提取文本
                    reply_text = reply_element.inner_text()
                    if reply_text and len(reply_text) > 5:
                        reply_content = reply_text
                        print()
                        print("=" * 60)
                        print("DOUBAO'S REPLY:")
                        print("=" * 60)
                        print(reply_content)
                        print("=" * 60)
                    else:
                        # 文本太短，可能没提取到
                        print("     [WARN] Text extraction returned short/empty result")
                        print("     Check screenshot: doubao_reply.png")
                        
                        # 尝试找所有消息元素
                        all_messages = page.query_selector_all(".message-content, .message-ai, .assistant-message")
                        print(f"     Found {len(all_messages)} message elements")
                        
                        for idx, msg in enumerate(all_messages[-3:]):  # 最后 3 条
                            try:
                                text = msg.inner_text()
                                if text and len(text) > 10:
                                    print(f"     Message {idx}: {text[:100]}...")
                            except:
                                pass
                except Exception as e:
                    print(f"     [ERROR] Extract failed: {e}")
                    page.screenshot(path="doubao_reply.png")
            else:
                print("[WARN] No reply detected within 60 seconds")
                print("[INFO] Check screenshot: doubao_reply.png")
                page.screenshot(path="doubao_reply.png")
            
            print()
            print("[INFO] Browser will stay open for 10 seconds...")
            time.sleep(10)
            browser.close()
            print("[DONE] Browser closed")
            
            return reply_content
            
    except Exception as e:
        print()
        print("=" * 60)
        print(f"FAILED: {e}")
        print("=" * 60)
        return None

if __name__ == "__main__":
    reply = send_doubao_and_get_reply("你猜猜我是谁")
    
    if reply:
        print()
        print("✅ Reply captured successfully!")
        sys.exit(0)
    else:
        print()
        print("⚠️ Reply not captured (check screenshots)")
        sys.exit(1)
