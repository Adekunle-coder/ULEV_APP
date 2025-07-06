from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os
import streamlit as st

def get_image(vrm):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # This is the Chromium path on Streamlit Cloud
    if os.path.exists("/usr/bin/chromium-browser"):
        options.binary_location = "/usr/bin/chromium-browser"
    elif os.path.exists("/usr/bin/chromium"):
        options.binary_location = "/usr/bin/chromium"
    else:
        st.error("Chromium binary not found on this system.")
        return

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        url = f"https://totalcarcheck.co.uk/FreeCheck?regno={vrm}"
        driver.get(url)
        image = driver.find_element(By.ID, "vehicleImage")
        if image:
            return image.get_attribute("src")
    except Exception as e:
        st.warning(f"Error while fetching vehicle image: {e}")
    finally:
        driver.quit()
