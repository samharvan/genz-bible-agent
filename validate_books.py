from playwright.sync_api import sync_playwright
import urllib.parse

def validate():
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        page = b.new_page(bypass_csp=True)
        page.goto('https://genz.bible', wait_until='domcontentloaded')
        page.wait_for_timeout(2000)
        
        links = page.eval_on_selector_all('a[href]', 'elements => elements.map(el => el.getAttribute("href"))')
        found_books = set()
        for href in links:
            if href and href.startswith('/'):
                parts = href.strip('/').split('/')
                if len(parts) >= 1:
                    book_candidate = urllib.parse.unquote(parts[0])
                    if book_candidate and (book_candidate[0].isupper() or book_candidate[0].isdigit()):
                        found_books.add(book_candidate)
        b.close()
    return sorted(list(found_books))

found = validate()
print("Books found on website:", len(found))
print(found)
