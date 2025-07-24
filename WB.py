import os
import re
import textwrap
import requests
import streamlit as st
import zipfile
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from tqdm import tqdm

visited = set()
report = []
OUTPUT_DIR = "pages"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def sanitize_filename(name):
    return re.sub(r'[^\w\-]', '_', name)[:50] or "page"

def is_valid_url(url, base_domain):
    parsed = urlparse(url)
    return (parsed.scheme in ['http', 'https'] and parsed.netloc == base_domain and url not in visited)

def scrape_page(url, index, progress_callback=None):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, timeout=10, headers=headers)
        if response.status_code != 200:
            return None

        visited.add(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup(['script', 'style']):
            tag.decompose()

        title = soup.title.string.strip() if soup.title and soup.title.string else f"Page {index}"
        text = soup.get_text(separator=' ', strip=True)
        wrapped_text = textwrap.fill(text, width=100)

        # Markdown report section
        report_section = f"""
## {index}. {title}

**URL**: [{url}]({url})

**Content:**

{wrapped_text}

---

"""
        report.append(report_section)

        # Save individual txt file
        filename = f"{index:02d}_{sanitize_filename(title)}.txt"
        full_path = os.path.join(OUTPUT_DIR, filename)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(f"Title: {title}\nURL: {url}\n\n{wrapped_text or 'No visible content found.'}")

        if progress_callback:
            progress_callback(index)

        return soup
    except Exception as e:
        st.error(f"Error scraping {url}: {e}")
        return None

def crawl(base_url, max_pages, progress_callback=None):
    base_domain = urlparse(base_url).netloc
    queue = [base_url]
    index = 1
    while queue and len(visited) < max_pages:
        url = queue.pop(0)
        if url not in visited:
            soup = scrape_page(url, index, progress_callback)
            if soup:
                index += 1
                for tag in soup.find_all("a", href=True):
                    link = urljoin(url, tag['href'])
                    if is_valid_url(link, base_domain):
                        queue.append(link)

def save_report(filename="scraped_report.md"):
    if report:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("# Website Scraping Report\n\n")
            f.writelines(report)
        return filename
    return None

def zip_text_files():
    zip_path = "pages_output.zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in os.listdir(OUTPUT_DIR):
            if file.endswith(".txt"):
                zipf.write(os.path.join(OUTPUT_DIR, file), arcname=file)
    return zip_path

# ------------------ STREAMLIT UI --------------------

st.set_page_config(page_title="Web Scraper App", layout="centered")
st.title("🌐 Website Scraper")

with st.form("scraper_form"):
    url = st.text_input("Enter website URL", value="https://example.com")
    max_pages = st.number_input("Number of pages to scrape", min_value=1, max_value=50, value=5)
    submit = st.form_submit_button("Scrape Website")

if submit:
    visited.clear()
    report.clear()
    for file in os.listdir(OUTPUT_DIR):
        os.remove(os.path.join(OUTPUT_DIR, file))

    with st.spinner("Scraping in progress..."):
        progress_bar = st.progress(0)

        def update_progress(i):
            progress_bar.progress(min(i / max_pages, 1.0))

        crawl(url, max_pages, progress_callback=update_progress)

    st.success("Scraping completed.")

    # Display Markdown content
    markdown_report = save_report()
    if markdown_report:
        with open(markdown_report, "r", encoding="utf-8") as f:
            st.markdown(f.read())

        with open(markdown_report, "rb") as f:
            st.download_button("📄 Download Markdown Report", f, file_name="scraped_report.md")

    # Zip and offer download of .txt files
    zip_path = zip_text_files()
    with open(zip_path, "rb") as f:
        st.download_button(" Download All Text Files (.zip)", f, file_name="scraped_pages.zip")
