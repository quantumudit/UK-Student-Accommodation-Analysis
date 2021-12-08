from requests_html import HTMLSession
from urllib.parse import urljoin
from datetime import datetime, timezone

ROOT_URL = 'https://www.accommodationforstudents.com'

all_properties = []
all_page_links = []

session = HTMLSession()

def generate_page_links() -> None:
    """
    This function generates the page links which then can be leveraged to scrape properties data using 'scrape_content()' function
    """
    
    url = 'https://www.accommodationforstudents.com/search-results?location=any&beds=1&searchType=any&price=&lettingPeriod=academicYear&geo=false&page=1'
    response = session.get(url)
    
    total_pages = int(response.html.find('div.PaginationWithStyles__pagination--3EdR0 a:nth-last-child(2)', first=True).text)
    
    for pgno in range(1, total_pages+1):
        page_url = f'https://www.accommodationforstudents.com/search-results?location=any&beds=1&searchType=any&price=&lettingPeriod=academicYear&geo=false&page={pgno}'
        all_page_links.append(page_url)
    return

def scrape_content(page_url: str) -> None:
    """
    This function scrapes individual properties from the given page URL.
    Args:
        url (str): page URL to scrape properties
    Returns:
        It returns nothing but adds individual properties into the 'all_properties' list
    """
    
    print('\n')
    print(f'Scraping properties from: {page_url}')
    
    utc_timezone = timezone.utc
    current_utc_timestamp = datetime.now(utc_timezone).strftime('%d-%b-%Y %H:%M:%S')
    
    response = session.get(page_url)
    content = response.html.find('div#property-grid article')
    
    for property in content:
        
        try:
            property_link = urljoin(ROOT_URL, property.find('a.property-card__link', first=True).attrs.get('href'))
        except:
            property_link = urljoin(ROOT_URL, property.find('a.student-halls-card__link', first=True).attrs.get('href'))
        
        try:
            property_type = property.find('div.property-card__title-wrapper strong', first=True).text
        except:
            property_type = property.find('div.student-halls-card__title-wrapper strong', first=True).text
        
        try:   
            property_address = property.find('div.address.property-card__address p.address__location span.address__text', first=True).text
        except:
            property_address = property.find('div.address.student-halls-card__address p.address__location span.address__text', first=True).text
        
        try:
            property_image = property.find('span.property-card__media-wrapper div.property-card__media img', first=True).attrs.get('data-src')
        except:
            property_image = property.find('div.student-halls-card__media img', first=True).attrs.get('data-src')
        
        
        property_price_from = property.find('div.property-terms span.property-terms__costs span.property-terms__from', first=True).text 
        property_price_amount = property.find('div.property-terms span.property-terms__costs span.property-terms__price', first=True).text
        property_price_duration = property.find('div.property-terms span.property-terms__costs span.property-terms__duration', first=True).text
        
        property_price = property_price_from+" "+property_price_amount+" "+property_price_duration
        
        try:
            property_extras = property.find('div.property-terms span.property-terms__extras',first=True).text
        except:
            property_extras= ""
        
        property_details = {
            'property_type': property_type,
            'property_address': property_address,
            'property_price': property_price,
            'property_extras': property_extras,
            'property_image': property_image,
            'property_details_link': property_link,
            'last_updated_at_UTC': current_utc_timestamp
        }
        
        all_properties.append(property_details)
    return

# Testing the scraper template #
# ---------------------------- #

if __name__ == '__main__':
    
    generate_page_links()
    
    print('\n')
    print(f'Total pages to scrape: {len(all_page_links)}')
    print('\n')
    
    page_url = 'https://www.accommodationforstudents.com/search-results?location=any&beds=1&searchType=any&price=&lettingPeriod=academicYear&geo=false&page=269'
    
    scrape_content(page_url)
    
    print('\n')
    print(f'Total properties scraped: {len(all_properties)}')
    print('\n')
    print(all_properties)