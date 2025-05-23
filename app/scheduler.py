Placeholder for periodic scraping using APScheduler

from apscheduler.schedulers.blocking import BlockingScheduler
from amazon_scraper import scrape_amazon_data
import datetime

def job():
    print(f"[{datetime.datetime.now()}] Running scheduled job...")
    scrape_amazon_data()

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    # Run every 30 seconds (for testing)
    scheduler.add_job(job, 'interval', seconds=30)
    print("[INFO] Scheduler started. Scraper will run every 30 seconds (test mode).")
    scheduler.start()
