from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import streamlit as st




def get_image(vrm):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    url = f"https://totalcarcheck.co.uk/FreeCheck?regno={vrm}"
    img_url = ""

    try:
        driver.get(url)
        image = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "vehicleImage"))
        )
        if img_url:
            img_url = image.get_attribute("src")
            return img_url
        else:
            st.info("Image not found")
    except Exception as e:
        st.info(f"An error was encountered while fetching the image: {e}")
    
    finally:
        driver.quit()
