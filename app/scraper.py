from playwright.sync_api import sync_playwright

def scrape_amazon_product(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            print(f"[INFO] Visiting: {url}")
            page.goto(url, timeout=15000)

        
            page.wait_for_selector('span#productTitle', timeout=5000)

        
            name = page.locator('span#productTitle').first.inner_text().strip()
            price = "N/A"
            price_candidates = page.locator(".a-price .a-offscreen").all_inner_texts()
            for p in price_candidates:
                if "₹" in p:
                    price = p.strip()
                    break

            print(f"[RESULT] Name: {name}")
            print(f"[RESULT] Price: {price}")

        except Exception as e:
            print(f"[ERROR] {e}")
        finally:
            browser.close()
product_url = "https://www.amazon.in/BSB-Cotton-Flower-Printed-Bedsheets/dp/B08YJT6FMN?ref_=Oct_d_oup_d_1380448031_1&pd_rd_w=AA1ih&content-id=amzn1.sym.8f511bca-047d-43c0-a1e2-d03b2812a527&pf_rd_p=8f511bca-047d-43c0-a1e2-d03b2812a527&pf_rd_r=R1BS7CXKBXVJZTDRK59N&pd_rd_wg=4Nc3u&pd_rd_r=1e68f614-7947-423d-a2eb-22f686419076&pd_rd_i=B08YJT6FMN&th=1"
scrape_amazon_product(product_url)
