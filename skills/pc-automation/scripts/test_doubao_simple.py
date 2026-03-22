# 简单测试网页访问

from playwright.sync_api import sync_playwright
import time

print("Testing web access...")
print()

try:
    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=False, channel="msedge")
        
        print("Opening page...")
        page = browser.new_page()
        
        print("Going to doubao.com...")
        page.goto("https://www.doubao.com", timeout=30000)
        
        print("Waiting...")
        time.sleep(5)
        
        print("SUCCESS! Page loaded.")
        
        time.sleep(3)
        browser.close()
        
except Exception as e:
    print(f"FAILED: {e}")
