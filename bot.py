import asyncio
import csv
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def scrape_location(browser, query, location):
    context = await browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    stealth = Stealth()
    page = await context.new_page()
    await stealth.apply_stealth_async(page)
    
    full_query = f"{query} in {location}"
    print(f"Searching: {full_query}")
    results = []

    try:
        # সরাসরি গুগল ম্যাপস লিঙ্কে যাওয়া এবং ওয়েট স্ট্র্যাটেজি পরিবর্তন করা
        await page.goto("https://www.google.com/maps", wait_until="domcontentloaded", timeout=60000)
        
        # সার্চ বক্স আসা পর্যন্ত অপেক্ষা
        search_box = page.locator('input[name="q"]')
        await search_box.wait_for(state="visible", timeout=15000)
        await search_box.fill(full_query)
        await page.keyboard.press("Enter")

        # রেজাল্ট লোড হওয়ার জন্য অপেক্ষা
        await page.wait_for_selector(".Nv2PK", timeout=30000)

        # স্ক্রল করা
        scrollable_div = page.locator('div[role="feed"]')
        for _ in range(2): 
            await scrollable_div.evaluate('el => el.scrollTop = el.scrollHeight')
            await asyncio.sleep(3)

        listings = await page.locator(".Nv2PK").all()
        print(f"Found {len(listings)} listings in {location}. Extracting details...")

        for index, list_item in enumerate(listings[:10]): # টেস্টের জন্য ১০টি
            try:
                name_el = list_item.locator(".qBF1Pd")
                name = await name_el.inner_text() if await name_el.count() > 0 else "N/A"

                await list_item.click()
                await asyncio.sleep(5) # প্যানেল এবং নম্বর লোড হওয়ার জন্য সময়

                phone = "Not Available"
                # ফোন নম্বর বাটনের জন্য মাল্টিপল সিলেক্টর
                phone_selectors = [
                    'button[data-tooltip="Copy phone number"]',
                    'button[aria-label^="Phone:"]',
                    'button[data-item-id^="phone:tel:"]'
                ]
                
                for selector in phone_selectors:
                    phone_el = page.locator(selector)
                    if await phone_el.count() > 0:
                        raw_phone = await phone_el.first.get_attribute("aria-label")
                        if raw_phone:
                            phone = raw_phone.replace("Phone: ", "").strip()
                            break
                
                address = "N/A"
                address_el = page.locator('button[data-item-id="address"]')
                if await address_el.count() > 0:
                    address = await address_el.first.inner_text()

                results.append([location, name, phone, address])
                print(f"Done: {name} | Phone: {phone}")

            except Exception:
                continue

        return results

    except Exception as e:
        print(f"Error in {location}: {e}")
        return []
    finally:
        await context.close()

async def main():
    async with async_playwright() as p:
        # শুরুতে কাজ করছে কিনা দেখতে headless=False দিতে পারেন
        browser = await p.chromium.launch(headless=True) 
        
        locations = ["Tongi", "Uttara"]
        query = "Madrasa"

        tasks = [scrape_location(browser, query, loc) for loc in locations]
        all_data = await asyncio.gather(*tasks)

        flat_results = [item for sublist in all_data for item in sublist]

        with open('madrasa_leads_final.csv', mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(['Area', 'Madrasa Name', 'Phone Number', 'Address'])
            writer.writerows(flat_results)

        print(f"\nSUCCESS! Results saved to 'madrasa_leads_final.csv'")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())