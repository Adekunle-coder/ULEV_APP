import cloudscraper
from bs4 import BeautifulSoup
import streamlit as st

def get_image(vrm):
    url = f"https://totalcarcheck.co.uk/FreeCheck?regno={vrm}"
    
    scraper = cloudscraper.create_scraper(browser={'custom': 'ScraperBot/1.0'})
    
    try:
        response = scraper.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        img = soup.find("img", {"id": "vehicleImage"})
        if img and img.get("src"):
            return img["src"]
        else:
            st.info("Image not found.")
    except Exception as e:
        st.warning(f"Error while fetching image: {e}")
        return None
