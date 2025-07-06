from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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
        image = driver.find_element(By.ID, "vehicleImage")
        if image:
            img_url = image.get_attribute("src")
            return img_url
        else:
            st.info("Image not found")
    except Exception as e:
        st.info(f"An error was encountered while fetching the image: {e}")
    
    finally:
        driver.quit()
