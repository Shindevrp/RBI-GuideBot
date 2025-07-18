import os
import requests
from bs4 import BeautifulSoup

DATA_DIR = "data"
RBI_RULES_URL = "https://www.rbi.org.in/Scripts/Regulations.aspx"

os.makedirs(DATA_DIR, exist_ok=True)

def download_rbi_pdfs():
    response = requests.get(RBI_RULES_URL)
    soup = BeautifulSoup(response.content, "html.parser")
    pdf_links = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if href.lower().endswith(".pdf"):
            if href.startswith("http"):
                pdf_links.append(href)
            else:
                pdf_links.append("https://www.rbi.org.in" + href)
    print(f"Found {len(pdf_links)} PDF links.")
    for url in pdf_links:
        filename = os.path.join(DATA_DIR, url.split("/")[-1])
        try:
            r = requests.get(url)
            with open(filename, "wb") as f:
                f.write(r.content)
            print(f"Downloaded: {filename}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")

if __name__ == "__main__":
    download_rbi_pdfs()
