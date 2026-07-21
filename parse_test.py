from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def test_parse():
    with sync_playwright() as p:
        b = p.chromium.launch()
        context = b.new_context(user_agent="Mozilla/5.0 (compatible; bot/1)", bypass_csp=True)
        page = context.new_page()
        page.goto("https://genz.bible/John/3", wait_until="domcontentloaded")
        page.wait_for_timeout(2000)
        html = page.content()
        context.close()
        b.close()
        
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
        print(f"Genz paras: {len(genz_els)}, KJV paras: {len(kjv_els)}")
test_parse()
