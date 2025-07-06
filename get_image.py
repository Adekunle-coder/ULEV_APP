import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import streamlit as st


def get_image(vrm):
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = uc.Chrome(options=options)

    url = f"https://totalcarcheck.co.uk/FreeCheck?regno={vrm}"
    img_url = ""

    try:
        driver.get(url)
        # Use WebDriverWait to wait for the image to load
        image = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "vehicleImage"))
        )
        img_url = image.get_attribute("src")
        return img_url

    except Exception as e:
        st.info(f"An error was encountered while fetching the image: {e}")
    
    finally:
        driver.quit()
