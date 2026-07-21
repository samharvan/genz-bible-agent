from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
def test():
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        c = b.new_context(user_agent="Mozilla/5.0")
        page = c.new_page()
        page.goto('https://genz.bible/John/3', wait_until='domcontentloaded')
        page.wait_for_timeout(2000)
        html = page.content()
        b.close()
    soup = BeautifulSoup(html, 'html.parser')
    genz_container, kjv_container = None, None
    for card in soup.select('.MuiCardContent-root'):
        text = card.get_text().strip()
        if text.startswith('Gen Z:'): genz_container = card
        elif text.startswith('KJV:'): kjv_container = card
    if genz_container and kjv_container:
        genz_els = genz_container.select('p')
        kjv_els = kjv_container.select('p')
        print(len(genz_els), len(kjv_els))
        for g, k in zip(genz_els[:2], kjv_els[:2]):
            print('G:', g.get_text()[:40])
            print('K:', k.get_text()[:40])
test()
