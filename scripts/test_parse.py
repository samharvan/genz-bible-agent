from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0", bypass_csp=True)
        page = context.new_page()
        page.goto("https://genz.bible/John/3", wait_until="domcontentloaded")
        page.wait_for_timeout(2000)
        html = page.content()
        browser.close()
        
    soup = BeautifulSoup(html, "html.parser")
    genz_container = None
    kjv_container = None
    
    for card in soup.select(".MuiCardContent-root"):
        text = card.get_text().strip()
        if text.startswith("Gen Z:"):
            genz_container = card
        elif text.startswith("KJV:"):
            kjv_container = card
            
    print(f"Gen Z Container found: {genz_container is not None}")
    print(f"KJV Container found: {kjv_container is not None}")
    
    if genz_container and kjv_container:
        genz_els = genz_container.select("p")
        kjv_els = kjv_container.select("p")
        print(f"GenZ paragraphs: {len(genz_els)}")
        print(f"KJV paragraphs: {len(kjv_els)}")
        
        for g_el, k_el in zip(genz_els[:2], kjv_els[:2]):
            print("G:", g_el.get_text())
            print("K:", k_el.get_text())
            print("---")

test()
