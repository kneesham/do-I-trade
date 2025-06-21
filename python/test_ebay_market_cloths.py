# Most popular brands of cloting to sell on ebay:

import re
import concurrent.futures
import threading
from time import sleep
from playwright.sync_api import Playwright, sync_playwright, expect

clothing_brands = ["Louis Vuitton",
                    "Nike",
                    "Lululemon",
                    "Patagonia",
                    "Eileen Fisher",
                    "Carhartt",
                    "Free People",
                    "Gucci",
                    "Pendleton",
                    "Arc'teryx",
                    "Levi's Vintage Denim",
                    "Anthropologie",
                    "Tommy Hilfiger",
                    "Dolce & Gabbana",
                    "Chanel",
                    "Fendi",
                    "Zara",
                    "Old Navy",
                    "Skechers",
                    "Ralph Lauren",
                    "The North Face",
                    "J.Crew",
                    "Banana Republic",
                    "Adidas"]


clothing_brands = ["Nike"]

EXCLUDE_TITLES = ["Shop on eBay"]


def get_sold_items_for_brand(brand: str, per_page: int = 240, n_retries: int = 0) -> list:
    """Get sold items for a specific brand using its own browser instance"""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            url = f"https://www.ebay.com/sch/i.html?_nkw={brand}&_sacat=11450&_from=R40&rt=nc&LH_Sold=1&LH_Complete=1&_ipg={per_page}"
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            
            titles = []

            title_elements = page.locator('li.s-item .s-item__title').all()[:per_page]
            
            for title_element in title_elements:
                if title_element.inner_text() in EXCLUDE_TITLES:
                    continue
                title_text = title_element.inner_text()
                titles.append(title_text)
            
            
            if len(titles) > 0:
                print(f"✓ Completed {brand}: Found {len(titles)} items")
                print(f"Removing {brand} from list as items found")
                clothing_brands.remove(brand)  # Remove brand from list if items found

            return titles
            
        except Exception as e:
            print(f"✗ Error with {brand}: {str(e)}")
            return []
        finally:
            context.close()
            browser.close()


def search_all_clothing_brands_multithreaded(clothing_brands: list[str], max_workers: int = 5, per_page: int = 240) -> dict:
    """Search all brands using multithreading"""
    results = {}
    
    print(f"Starting multithreaded search with {max_workers} workers...")
    print(f"Searching {len(clothing_brands)} brands\n")
    
    # Use ThreadPoolExecutor for concurrent execution
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_brand = {
            executor.submit(get_sold_items_for_brand, brand, per_page): 
            brand for brand in clothing_brands
        }
        
        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_brand):
            brand = future_to_brand[future]
            try:
                titles = future.result()
                results[brand] = titles

            except Exception as e:
                print(f"✗ Exception for {brand}: {str(e)}")
                results[brand] = []
    
    return results


if __name__ == "__main__":
    # Configure threading settings
    max_workers = 5  # Adjust based on your system capacity
    per_page = 240   # Items per brand to fetch
    
    print("=" * 50)
    print("EBAY CLOTHING BRAND RESEARCH - MULTITHREADED")
    print("=" * 50)
    
    # Run multithreaded search
    while clothing_brands != []:
        all_results = search_all_clothing_brands_multithreaded(clothing_brands, max_workers=max_workers, per_page=per_page)
    
    print("\n" + "=" * 50)
    print("SEARCH COMPLETE - SUMMARY")
    print("=" * 50)
    
    total_items = 0
    for brand, titles in all_results.items():
        item_count = len(titles)
        total_items += item_count
        print(f"{brand}: {item_count} items")
        print(titles)
    
    print(f"\nTotal items found across all brands: {total_items}")
    print(f"Brands searched: {len(all_results)}")

