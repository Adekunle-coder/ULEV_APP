
import requests
from bs4 import BeautifulSoup
import streamlit as st

def get_image(vrm: str) -> str | None:
    
    url = f"https://totalcarcheck.co.uk/FreeCheck?regno={vrm}"

    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            )
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        img = soup.find("img", {"id": "vehicleImage"})

        if img and img.get("src"):
            return img["src"]

        st.info("Vehicle image not found on the page.")
        return None

    except requests.RequestException as e:
        st.warning(f"Request failed: {e}")
        return None
