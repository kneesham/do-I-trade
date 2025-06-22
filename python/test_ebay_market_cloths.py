# Most popular brands of cloting to sell on ebay:

import re
import concurrent.futures
import threading
import pprint as pp
from time import sleep
from playwright.sync_api import Playwright, sync_playwright, expect
from collections import defaultdict


clothing_product_groups = {
    'Shoes/Sneakers': ['shoes', 'sneakers', 'trainers', 'footwear', 'running', 'basketball', 'tennis', 'cleats', 'boots'],
    'T-Shirts/Tops/Tank Tops': ['t-shirt', 'tee', 'top', 'tank top', 'tank', 'blouse', 'tunic'],
    'Shorts': ['shorts', 'short'],
    'Pants/Joggers/Sweatpants/Track Pants': ['pants', 'joggers', 'sweatpants', 'track pants', 'leggings', 'tights', 'trousers'],
    'Hoodies/Sweatshirts/Pullovers': ['hoodie', 'sweatshirt', 'pullover', 'sweater', 'fleece'],
    'Jackets/Windbreakers/Rain Jackets': ['jacket', 'windbreaker', 'rain jacket', 'coat', 'blazer', 'vest'],
    'Polo Shirts/Golf Shirts': ['polo', 'golf shirt', 'polo shirt'],
    'Skirts/Skorts/Boardskirts': ['skirt', 'skort', 'boardskirt'],
    'Socks': ['socks', 'sock', 'ankle socks', 'crew socks'],
    'Slides/Sandals': ['slides', 'sandals', 'flip flops', 'slippers'],
    'Rompers': ['romper', 'jumpsuit', 'playsuit'],
    'Duffle Bags/Handbags': ['duffle bag', 'handbag', 'bag', 'backpack', 'tote', 'purse', 'duffel'],
    'Hats/Caps': ['hat', 'cap', 'beanie', 'snapback', 'baseball cap', 'bucket hat'],
    'Key Chains/Accessories': ['keychain', 'key chain', 'accessories', 'wallet', 'belt', 'watch', 'jewelry'],
    'Cosmetics/Beauty Products': ['cosmetics', 'beauty', 'makeup', 'skincare', 'perfume', 'fragrance'],
    'Wallets/Small Leather Goods': ['wallet', 'cardholder', 'card holder', 'coin purse', 'money clip', 'card case'],
    'Belts': ['belt', 'buckle'],
    'Sunglasses/Eyewear': ['sunglasses', 'glasses', 'eyewear', 'shades'],
    'Jewelry/Watches': ['watch', 'jewelry', 'necklace', 'bracelet', 'earrings', 'ring', 'chain'],
    'Scarves/Wraps': ['scarf', 'scarf', 'wrap', 'shawl', 'bandana'],
    'Underwear/Lingerie': ['underwear', 'lingerie', 'bra', 'panties', 'briefs', 'boxers'],
    'Swimwear': ['swimsuit', 'bikini', 'swim', 'boardshorts', 'trunks'],
    'Dresses': ['dress', 'gown', 'sundress', 'maxi dress'],
    'Suits/Formal Wear': ['suit', 'tuxedo', 'formal', 'dress shirt', 'tie'],
    'Luggage/Travel': ['suitcase', 'luggage', 'travel bag', 'carry-on', 'garment bag'],
    'Phone Cases/Tech Accessories': ['phone case', 'case', 'tech', 'airpods', 'tablet'],
    'Gloves': ['gloves', 'mittens'],
    'Boots': ['boots', 'ankle boots', 'combat boots', 'hiking boots', 'rain boots'],
    'Activewear/Athletic': ['activewear', 'athletic', 'yoga', 'workout', 'sports bra', 'compression'],
    'Vintage/Rare Items': ['vintage', 'rare', 'limited edition', 'collector'],
    'Gift Cards/Certificates': ['gift card', 'certificate', 'voucher']
}

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


# clothing_brands = ["Nike"]

EXCLUDE_TITLES = ["Shop on eBay"]

def serialize_price_to_float(price_str):
    """Convert price string to float, handling various formats"""
    if not price_str or price_str == 'N/A':
        return 0.0
    
    # Remove $ and clean the string
    cleaned = str(price_str).replace('$', '').replace(',', '').strip()
    
    # Handle price ranges (take the lower price)
    if ' to ' in cleaned:
        lower_price = cleaned.split(' to ')[0].strip()
        try:
            return float(lower_price)
        except ValueError:
            return 0.0
    
    # Handle "or Best Offer" or similar text
    if ' or ' in cleaned.lower():
        price_part = cleaned.split(' or ')[0].strip()
        try:
            return float(price_part)
        except ValueError:
            return 0.0
    
    # Handle regular prices
    try:
        return float(cleaned)
    except ValueError:
        # Extract first number if string contains other text
        import re
        numbers = re.findall(r'\d+\.?\d*', cleaned)
        if numbers:
            try:
                return float(numbers[0])
            except ValueError:
                return 0.0
        return 0.0
    
def flatten_and_consolidate_categories(categorize_items_summaries, num_items_per_brand: int = 100):
    """Flatten all brand categories into a single consolidated summary"""
    consolidated = {}
    
    for brand_summary in categorize_items_summaries:
        for category, items in brand_summary.items():
            if category not in consolidated:
                consolidated[category] = {
                    'items': [],
                    'total_items': 0,
                    'total_price': 0.0,
                    'brands': set()
                }
            
            # Extract items (excluding the summary dictionaries)
            actual_items = [item for item in items if isinstance(item, dict) and 'title' in item]
            summary_items = [item for item in items if isinstance(item, dict) and ('average_price' in item or 'total_items' in item)]
            
            # Add items to consolidated category
            consolidated[category]['items'].extend(actual_items)
            consolidated[category]['total_items'] += len(actual_items)
            consolidated[category]['total_price'] += sum(item['price'] for item in actual_items)
            
            # Track which brands contribute to this category
            # You'd need to pass brand info, but for now we can infer from the loop
    
    # Calculate final averages and create summary
    final_summary = {}
    for category, data in consolidated.items():
        if data['total_items'] > 0:
            final_summary[category] = {
                'total_items': data['total_items'],
                'average_price': round(data['total_price'] / data['total_items'], 2),
                'total_value': round(data['total_price'], 2),
                'all_items': data['items'][:num_items_per_brand]
            }
    
    return final_summary


def categorize_items(items):
    groups = defaultdict(list)
    
    for item in items:
        title_lower = item['title'].lower()
        categorized = False
        
        # Check each category
        for category, keywords in clothing_product_groups.items():
            if any(keyword in title_lower for keyword in keywords):
                groups[category].append(item)
                categorized = True
                break
        
        # If no category found, put in 'Other Nike Items'
        if not categorized:
            groups['Other Items'].append(item)
    
    for category in groups:
        # Sort items in each category by title
        groups[category] = sorted(groups[category], key=lambda x: x['title'].lower())
        groups[category].append({"average_price": round(sum(item['price'] for item in groups[category]) / len(groups[category]),2) if groups[category] else 0.0})
        groups[category].append({"total_items": len(groups[category]) - 1 })

    
    return dict(groups)

def get_sold_items_for_brand(brand: str, per_page: int = 240, n_retries: int = 0) -> list:
    """Get sold items for a specific brand using its own browser instance"""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            url = f"https://www.ebay.com/sch/i.html?_nkw={brand}&_sacat=11450&_from=R40&rt=nc&LH_Sold=1&LH_Complete=1&_ipg={per_page}"
            page.goto(url)
            
            listings = []

            sold_items = page.locator('li.s-item').all()[:per_page]

            
            for item in sold_items:
                title = item.locator('.s-item__title').first.text_content()
                price = item.locator('.s-item__price').first.text_content()
                link = item.locator('.s-item__link').first.get_attribute('href')
                short_link = re.search(r'/itm/(\d+)', link)


                if title in EXCLUDE_TITLES:
                    continue


                if short_link:
                    item_id = short_link.group(1)
                    link = f"https://www.ebay.com/itm/{item_id}"


                listings.append({"title":title, "price": serialize_price_to_float(price), "link": link})
                
                
            
            
            if len(listings) > 0:
                print(f"✓ Completed {brand}: Found {len(listings)} items")
                clothing_brands.remove(brand)  # Remove brand from list if items found

            return listings
            
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
    
    max_workers = 5  
    per_page = 240   
    total_items = 0
    total_brands =  len(clothing_brands)
    categorize_items_summaries = []
    # Initialize the list of clothing brands to search
    
    print("=" * 50)
    print("EBAY CLOTHING BRAND RESEARCH - MULTITHREADED")
    print("=" * 50)
    
    
    while clothing_brands != []:
    # Run multithreaded search while there are still brands to search
        
        all_results = search_all_clothing_brands_multithreaded(clothing_brands, max_workers=max_workers, per_page=per_page)
        # Store the results of the found items
        
        for brand, sale_info in all_results.items():
            # For each of the brands, get the sale info
            
            item_count = len(sale_info)
            total_items += item_count
            # Update the total number of items found
            
            print(f"{brand}: {item_count} items")

            categorize_items_info = categorize_items(sale_info)
            categorize_items_summaries.append(categorize_items_info)
            # Categorize the items found for each brand
    
    print("\n" + "=" * 50)
    print("SEARCH COMPLETE - SUMMARY")
    print("=" * 50)

    # Flatten and consolidate all categories
    consolidated_summary = flatten_and_consolidate_categories(categorize_items_summaries, num_items_per_brand=100)
    
    # Sort by total items descending
    sorted_categories = sorted(consolidated_summary.items(), 
                             key=lambda x: x[1]['total_items'], 
                             reverse=True)
    
    # Print the consolidated summary
    pp.pprint(sorted_categories)
    
    
    print(f"\nTotal items found across all brands: { total_items }")
    print(f"Brands searched: { total_brands }")
