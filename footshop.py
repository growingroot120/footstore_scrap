from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import json

# Setup Chrome options
chrome_options = Options()
# chrome_options.add_argument('--headless')  # Run in headless mode
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--start-maximized')  # Start Chrome maximized

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

for page in range(10, 11):
    jsonFile = open(rf'D:\Working\freelancer\2024\07_19_srilangka_fix\test.json', 'w', encoding='utf-8')
    url = f'https://www.footshop.fr/fr/25_nike/categories-baskets-boots-claquettes/page-{page}'

    driver.get(url)

    # Wait for the products to load
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'Products_product_1JtLQ')))
    
    try:
        cookie_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')))
        cookie_button.click()
    except Exception as e:
        print(f"Cookie consent button error: {e}")

    data = []
    product_links = [product.find_element(By.CLASS_NAME, 'Product_text_2wCMF').get_attribute('href') for product in driver.find_elements(By.CLASS_NAME, 'Products_product_1JtLQ')]

    for href in product_links:
        try:
            driver.get(href)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ProductFeatures_wrapper_3TGar')))

            # Extract the description HTML
            desrption_html = driver.find_element(By.CLASS_NAME, 'ProductFeatures_wrapper_3TGar').get_attribute('outerHTML')

            # Extract JSON data from the script tag
            script_tag = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//script[@type="application/json" and @data-hypernova-key="ProductDetail"]'))
            )
            script_content = script_tag.get_attribute('innerHTML')
            json_str = script_content.lstrip('<!--').rstrip('-->')

            json_data = json.loads(json_str)
            json_data['body_html'] = desrption_html

            data.append(json_data)

            # Navigate back to the product list page
            driver.back()
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'Products_product_1JtLQ')))

        except Exception as e:
            print(f"An error occurred: {e}")

    json.dump(data, jsonFile, indent=4)
    jsonFile.close()

    print(f'done {page}')

    driver.quit()
