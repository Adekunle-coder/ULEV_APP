
import requests
from bs4 import BeautifulSoup
import streamlit as st

def get_image(vrm: str) -> str | None:

    import requests

    accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
    accept_language = "en-GB,en;q=0.6"
    cookie = "zero-chakra-ui-color-mode=light-zero; AMP_MKTG_8f1ede8e9c=JTdCJTIycmVmZXJyZXIlMjIlM0ElMjJodHRwcyUzQSUyRiUyRnd3dy5nb29nbGUuY29tJTJGJTIyJTJDJTIycmVmZXJyaW5nX2RvbWFpbiUyMiUzQSUyMnd3dy5nb29nbGUuY29tJTIyJTdE; AMP_8f1ede8e9c=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI1MjgxOGYyNC05ZGQ3LTQ5OTAtYjcxMC01NTY0NzliMzAwZmYlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzA4MzgxNTQ4ODQzJTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcwODM4MjE1NTQ2MCUyQyUyMmxhc3RFdmVudElkJTIyJTNBNiU3RA=="
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

    custom_headers = {
        "User-Agent": user_agent,
        "Accept": accept,
        "Accept-Language": accept_language,
        "Cookie": cookie,
    }
    
    url = f"https://totalcarcheck.co.uk/FreeCheck?regno={vrm}"

    try:
        # headers = {
        #     "User-Agent": (
        #         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        #         "AppleWebKit/537.36 (KHTML, like Gecko) "
        #         "Chrome/114.0.0.0 Safari/537.36"
        #     )
        # }

        response = requests.get(url, headers=custom_headers, timeout=10)
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
