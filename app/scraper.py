import sqlite3
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError

def init_db():
    conn = sqlite3.connect("price_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_title TEXT,
            price REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            url TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_to_db(product_title, price, url):
    conn = sqlite3.connect("price_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO prices (product_title, price, url) VALUES (?, ?, ?)", (product_title, price, url))
    conn.commit()
    conn.close()
    print(f"[DB] Saved: {product_title} - ₹{price} at {datetime.now()}")

def scrape_amazon_product(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ))
        page = context.new_page()

        try:
            print(f"[INFO] Visiting: {url}")
            page.goto(url, timeout=15000)

            if "captcha" in page.url:
                print("[BLOCKED] Captcha encountered.")
                return

            page.wait_for_selector("#productTitle", timeout=10000)
            product_title = page.locator("#productTitle").first.inner_text().strip()

            price_spans = page.locator(".a-price .a-offscreen").all_inner_texts()
            price = None
            for p in price_spans:
                if "₹" in p:
                    price = float(p.replace("₹", "").replace(",", "").strip())
                    break

            if product_title and price:
                save_to_db(product_title, price, url)
            else:
                print("[ERROR] Couldn't extract price/title.")

        except TimeoutError:
            print("[TIMEOUT] Page load failed.")
        except Exception as e:
            print(f"[ERROR] Scraping failed: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    init_db()
    
    product_url = "https://www.amazon.in/BSB-Cotton-Flower-Printed-Bedsheets/dp/B08YJT6FMN/ref=pd_bxgy_thbs_d_sccl_2/262-8216538-9800939?pd_rd_w=LgHPG&content-id=amzn1.sym.d1afc5d3-2e83-45f5-8382-2dc0d946ef8f&pf_rd_p=d1afc5d3-2e83-45f5-8382-2dc0d946ef8f&pf_rd_r=MTPVY547H4647F4H0K3Z&pd_rd_wg=FIooO&pd_rd_r=f3afc6d3-f5ac-4146-b2de-d836c0f04d3b&pd_rd_i=B08YJT6FMN&th=1"
    scrape_amazon_product(product_url)
