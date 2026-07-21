from playwright.sync_api import sync_playwright

def find_api():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        def handle_response(response):
            # Check for data endpoints, json files, etc
            if "json" in response.url or "/api/" in response.url or "genz" in response.url.lower():
                print(f"[{response.status}] {response.url} ({response.headers.get('content-type', '')})")

        page.on("response", handle_response)
        page.goto("https://genz.bible/Genesis/1")
        page.wait_for_timeout(3000)
        browser.close()

if __name__ == "__main__":
    find_api()
