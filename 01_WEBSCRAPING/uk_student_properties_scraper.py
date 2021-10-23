import pandas as pd
import datetime
import pyfiglet
from concurrent.futures import ThreadPoolExecutor
from fx_uk_student_properties_scraper_template import *

def main() -> None:
    """
    This function loops though each of the page and scrapes all the student properties
    """    
    with ThreadPoolExecutor() as executor:
        executor.map(scrape_content, all_page_links)
    return

def load_data() -> None:
    """
    This function loads the scraped data into a CSV file
    """
    
    whisky_df = pd.DataFrame(all_properties)
    whisky_df.to_csv('uk_student_properties_data.csv', index=False)
    return

if __name__ == '__main__':
    
    scraper_title = "UK STUDENT ACCOMMODATION PROPERTIES SCRAPER"
    ascii_art_title = pyfiglet.figlet_format(scraper_title, font='small')
    
    start_time = datetime.datetime.now()
    
    print('\n\n')
    print(ascii_art_title)
    print('Scraping student properties across UK...')
    
    generate_page_links()
    
    print(f'Total pages to scrape:{len(all_page_links)}')
    print('Scraping student property details from each page...')
    print('\n')
    
    main()
    
    end_time = datetime.datetime.now()
    scraping_time = end_time - start_time
    
    print('\n')
    print('All properties scraped...')
    print(f'Time spent on scraping: {scraping_time}')
    print(f'Total properties collected: {len(all_properties)}')
    print('\n')
    print('Loading data into CSV...')
    
    load_data()
    
    print('Data Exported to CSV...')
    print('Webscraping completed !!!')