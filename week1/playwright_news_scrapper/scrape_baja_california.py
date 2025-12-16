# ----------------- VERSION PY SCRIPT -----------------------------------

# from playwright.sync_api import sync_playwright
# import json
# import time

# BASE_URL = "https://mexicoindustry.com/estado/baja-california"

# MAX_PAGES = 3
# OUTPUT_FILE = "baja_california_articles.json"
# HEADLESS = True  # keep False while debugging


# def scrape_articles(max_pages: int):
#     results = []
#     seen = set()

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=HEADLESS)
#         page = browser.new_page()
#         page.goto(BASE_URL, timeout=60000)

#         page_number = 1

#         while page_number <= max_pages:
#             print(f"\nScraping page {page_number}...")

#             # ✅ wait for real cards
#             page.wait_for_selector("div.list-post.news-article-vertical", timeout=60000)

#             cards = page.query_selector_all("div.list-post.news-article-vertical")
#             print(f"Found cards: {len(cards)}")

#             for card in cards:
#                 link_el = card.query_selector("div.list-post-content h3 a")
#                 date_el = card.query_selector("div.publication-date")

#                 if not link_el:
#                     continue

#                 title = link_el.inner_text().strip()
#                 url = link_el.get_attribute("href")
#                 date = date_el.inner_text().strip() if date_el else None

#                 if url in seen:
#                     continue
#                 seen.add(url)

#                 results.append({
#                     "title": title,
#                     "date": date,
#                     "url": url
#                 })

#             # pagination
#             next_button = page.query_selector('a[rel="next"]')
#             if not next_button:
#                 print("No more pages.")
#                 break

#             next_button.click()
#             time.sleep(2)
#             page_number += 1

#         browser.close()

#     return results


# if __name__ == "__main__":
#     articles = scrape_articles(MAX_PAGES)
#     print(articles)

#     # with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
#     #     json.dump(articles, f, ensure_ascii=False, indent=2)

#     # print(f"\nSaved {len(articles)} articles to {OUTPUT_FILE}")

# ----------------- VERSION JUPYTER --------------------------------

import json
import sys
from playwright.sync_api import sync_playwright

BASE_URL = "https://mexicoindustry.com/estado/baja-california"
HEADLESS = True

"""
def scrape_articles(max_pages: int):
    results = []
    seen = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()

        page_number = 1

        while page_number <= max_pages:
            print(f"\nScraping page {page_number}...", file=sys.stderr)

            page.goto(
                BASE_URL if page_number == 1 else f"{BASE_URL}/page/{page_number}",
                timeout=60000
            )

            page.wait_for_load_state("networkidle")
            page.wait_for_selector(
                "div.list-post.news-article-vertical",
                timeout=60000
            )

            cards = page.query_selector_all(
                "div.list-post.news-article-vertical"
            )

            print(f"Found cards: {len(cards)}", file=sys.stderr)

            for card in cards:
                link_el = card.query_selector("h3 a")
                date_el = card.query_selector("div.publication-date")

                if not link_el:
                    continue

                url = link_el.get_attribute("href")
                if url in seen:
                    continue
                seen.add(url)

                results.append({
                    "title": link_el.inner_text().strip(),
                    "date": date_el.inner_text().strip() if date_el else None,
                    "url": url
                })

            page_number += 1

        browser.close()

    return results
"""
    
def scrape_articles(max_pages: int):
    results = []
    seen = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()
        page.goto(BASE_URL, timeout=60000)

        page_number = 1

        while page_number <= max_pages:
            print(f"\nScraping page {page_number}...", file=sys.stderr)

            page.wait_for_selector(
                "div.list-post.news-article-vertical",
                timeout=60000
            )

            cards = page.query_selector_all(
                "div.list-post.news-article-vertical"
            )
            print(f"Found cards: {len(cards)}", file=sys.stderr)

            for card in cards:
                link_el = card.query_selector(
                    "div.list-post-content h3 a"
                )
                date_el = card.query_selector(
                    "div.publication-date"
                )

                if not link_el:
                    continue

                title = link_el.inner_text().strip()
                url = link_el.get_attribute("href")
                date = date_el.inner_text().strip() if date_el else None

                if url in seen:
                    continue
                seen.add(url)

                results.append({
                    "title": title,
                    "date": date,
                    "url": url
                })

            next_button = page.query_selector('a[rel="next"]')
            if not next_button:
                print("No more pages.")
                break

            # 🔥 THIS IS THE FIX
            with page.expect_navigation():
                next_button.click()

            page.wait_for_load_state("networkidle")
            page_number += 1

        browser.close()

    return results


if __name__ == "__main__":
    pages = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    data = scrape_articles(pages)

    # ✅ JSON ONLY
    sys.stdout.write(json.dumps(data, ensure_ascii=False))
