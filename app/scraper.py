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



--Handle edge cases (redirects, blocked requests, unavailable pages).
--Run it locally for 1-2 product links. 
from playwright.sync_api import sync_playwright, TimeoutError
import time

def scrape_amazon_product(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ))
        page = context.new_page()

        try:
            print(f"\n[INFO] Visiting: {url}")
            page.goto(url, timeout=20000)

            # Check for captcha
            if "captcha" in page.url or "sorry" in page.url:
                print("[WARNING] Blocked by captcha or Amazon bot protection.")
                return

            # Wait for product title
            page.wait_for_selector('span#productTitle', timeout=7000)

            # Get title
            name = page.locator('span#productTitle').first.inner_text().strip()

            # Try all visible price elements
            price = "N/A"
            price_candidates = page.locator(".a-price .a-offscreen").all_inner_texts()
            for p in price_candidates:
                if "₹" in p:
                    price = p.strip()
                    break

            print(f"[RESULT] Name: {name}")
            print(f"[RESULT] Price: {price}")

        except TimeoutError:
            print("[ERROR] Page took too long to load or product unavailable.")
        except Exception as e:
            print(f"[ERROR] {e}")
        finally:
            browser.close()

product_urls = [
    "https://www.amazon.in/Titan-Analog-Brown-Womens-Watch-2656WL01/dp/B09B9QZH8N/ref=sr_1_7?dib=eyJ2IjoiMSJ9.uXLht9jiqx8MI2bzJqy0i59z35ZHTET80AVqJ31bupKbwHj2AJAEyyHudhfk5nHeyEV6AOv2yQt0VKNrb0umLF1qoEtSP61TOGrR9bXaPAbVk4TLtKXK5Z69K-Vr1_x9Hly79OhU7qx4c7lVfVWsb4DfBIK-cHoWQ0EKX-U9RYsS53eE0QHUW6FR1Br29Uqxt1K8yhUB2-J-QvezhhaP6YGn8qw06_95wn5PCVfdHX-ukG16jrPjTeCyaqsXqjV3q4sUz6LlWDMK9-JDhBwvLyccqK5dAzbl_RK4mSxrskA.X3QvobivK6PW2JzO6iqUnP5pvwrOBHhCjiERfScSWWw&dib_tag=se&pf_rd_i=2563505031&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_s=merchandised-search-16&qid=1747921399&refinements=p_n_feature_fourteen_browse-bin%3A11142592031%2Cp_89%3ATitan&rnid=3837712031&s=watches&sr=1-7",
    "https://www.amazon.in/Titan-Raga-Analog-Womens-Watch-2642WM01/dp/B08HCLZPTG/ref=sr_1_3?dib=eyJ2IjoiMSJ9.uXLht9jiqx8MI2bzJqy0i59z35ZHTET80AVqJ31bupKbwHj2AJAEyyHudhfk5nHeyEV6AOv2yQt0VKNrb0umLF1qoEtSP61TOGrR9bXaPAbVk4TLtKXK5Z69K-Vr1_x9Hly79OhU7qx4c7lVfVWsb4DfBIK-cHoWQ0EKX-U9RYsS53eE0QHUW6FR1Br29Uqxt1K8yhUB2-J-QvezhhaP6YGn8qw06_95wn5PCVfdHX-ukG16jrPjTeCyaqsXqjV3q4sUz6LlWDMK9-JDhBwvLyccqK5dAzbl_RK4mSxrskA.X3QvobivK6PW2JzO6iqUnP5pvwrOBHhCjiERfScSWWw&dib_tag=se&pf_rd_i=2563505031&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_s=merchandised-search-16&qid=1747921399&refinements=p_n_feature_fourteen_browse-bin%3A11142592031%2Cp_89%3ATitan&rnid=3837712031&s=watches&sr=1-3&th=1"  # Change to any valid Amazon product
]

for url in product_urls:
    scrape_amazon_product(url)
    time.sleep(2)  
    

