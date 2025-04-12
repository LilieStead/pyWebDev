from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Function to scrape product details
def get_amazon_product_details(url):
    # Set up Selenium options for headless browsing (optional)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Uncomment this to run without opening a browser window
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration for headless mode

    # Set up WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Open the product page
    driver.get(url)

    # Wait for the page to load
    time.sleep(3)  # You might need to increase this sleep time depending on the page load time

    # Get the product title
    try:
        title = driver.find_element(By.ID, "productTitle").text
    except:
        title = "Title not found"

    # Get the product price
    try:
        price = driver.find_element(By.ID, "priceblock_ourprice").text
    except:
        try:
            price = driver.find_element(By.ID, "priceblock_dealprice").text
        except:
            try:
                price = driver.find_element(By.CLASS_NAME, "a-price-whole").text
            except:
                price = "Price not found"

    # Get the product description
    try:
        description = driver.find_element(By.ID, "productDescription").text
    except:
        # If description isn't directly found, extract bullet points
        description = ""
        try:
            bullet_points = driver.find_elements(By.CSS_SELECTOR, "#feature-bullets ul li span")
            description = "\n".join([b.get_attribute('innerText') for b in bullet_points])
        except:
            description = "Description not found"

    # Close the browser
    driver.quit()

    # Return product details
    return {
        "title": title,
        "price": price,
        "description": description,
    }

# Testing
# url = "https://www.amazon.co.uk/dp/B07VYZY4B2/ref=sspa_dk_detail_0?pd_rd_i=B07VYZY4B2&pd_rd_w=gQkzb&content-id=amzn1.sym.b0e623ee-d52c-45f6-bb59-f1032539acce&pf_rd_p=b0e623ee-d52c-45f6-bb59-f1032539acce&pf_rd_r=4KFDAZ1PWQ79DEG93KC4&pd_rd_wg=vcZgw&pd_rd_r=a6638269-88cb-4689-b789-6c3cbbfcb750&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWxfdGhlbWF0aWM&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExTFk5UVowSDRWRUVWJmVuY3J5cHRlZElkPUExMDA5NzgxMVlQNFFIN1EwSE1aMiZlbmNyeXB0ZWRBZElkPUEwNDkwNTY2MjNGWUwzRjhHSlNBMCZ3aWRnZXROYW1lPXNwX2RldGFpbF90aGVtYXRpYyZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU&th=1"  # Replace with any Amazon product URL
# details = get_amazon_product_details(url)
# print(details)
