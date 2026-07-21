import json
from scripts.test_scraping_data import parse_chapter

# Let's test with playwright locally to get one page and check the output JSON
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        c = b.new_context()
        page = c.new_page()
        page.goto('https://genz.bible/John/3', wait_until='domcontentloaded')
        page.wait_for_timeout(2000)
        html = page.content()
        b.close()
        
    chunks = parse_chapter(html, "John", 3)
    print(json.dumps(chunks[:2], indent=2))
    
run()
