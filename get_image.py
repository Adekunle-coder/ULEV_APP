from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import streamlit as st
import time

def get_image(vrm):
    options = Options()
    # options.add_argument("--headless")  # Keep visible for better bot evasion
    
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)

    # Mask navigator.webdriver to undefined
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        '''
    })

    base_url = "https://totalcarcheck.co.uk"
    check_url = f"{base_url}/FreeCheck?regno={vrm}"
    img_url = ""

    try:
        # Step 1: Open base url to set cookies with domain
        driver.get(base_url)
        time.sleep(2)  # wait a bit to load

        # Step 2: Set the cookies one by one for the domain
        # Parse your cookie string into Selenium cookies format:
        cookie_str = "zero-chakra-ui-color-mode=light-zero; AMP_MKTG_8f1ede8e9c=JTdCJTIycmVmZXJyZXIlMjIlM0ElMjJodHRwcyUzQSUyRiUyRnd3dy5nb29nbGUuY29tJTJGJTIyJTJDJTIycmVmZXJyaW5nX2RvbWFpbiUyMiUzQSUyMnd3dy5nb29nbGUuY29tJTIyJTdE; AMP_8f1ede8e9c=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI1MjgxOGYyNC05ZGQ3LTQ5OTAtYjcxMC01NTY0NzliMzAwZmYlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzA4MzgxNTQ4ODQzJTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcwODM4MjE1NTQ2MCUyQyUyMmxhc3RFdmVudElkJTIyJTNBNiU3RA=="
        for cookie_pair in cookie_str.split(';'):
            if '=' in cookie_pair:
                name, value = cookie_pair.strip().split('=', 1)
                try:
                    driver.add_cookie({'name': name, 'value': value, 'domain': 'totalcarcheck.co.uk', 'path': '/'})
                except Exception as e:
                    st.warning(f"Failed to add cookie {name}: {e}")

        # Step 3: Now navigate to the target page with VRM
        driver.get(check_url)

        wait = WebDriverWait(driver, 5)
        image = wait.until(EC.presence_of_element_located((By.ID, "vehicleImage")))
        if image:
            img_url = image.get_attribute("src")
            return img_url
        else:
            st.info("Image not found")

    except Exception as e:
        st.info(f"An error was encountered while fetching the image: {e}")
    finally:
        driver.quit()
