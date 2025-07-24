#  WebWhisperer: A Recursive Web Scraper with Streamlit Dashboard

##  1. Introduction

**WebWhisperer** is a powerful recursive web scraping tool built with Python. It scrapes a given website (along with all its internal links) and extracts readable text content, saving it in a structured format. The project provides both a command-line interface and a user-friendly **Streamlit** dashboard for live interaction.

>  **Note**: This project is still under development. Additional features such as PDF export, image scraping, and improved content parsing will be added in the future.

---

##  2. Libraries Used

The project uses the following Python libraries:

- `os`: File and directory operations
- `requests`: For HTTP requests
- `bs4` (BeautifulSoup): HTML parsing
- `urllib.parse`: URL normalization and validation
- `streamlit`: To build the interactive web interface
- `re`: Regular expressions for cleaning HTML
- `datetime`: For timestamping the report files

---

##  3. System Architecture & Components

The scraper follows a simple yet effective recursive crawling pattern:

###  Key Features:

- **Recursive Crawling**: Collects data from the main URL and all its subpages.
- **Content Extraction**: Removes scripts, styles, and non-visible content.
- **Markdown & Text Reports**: Saves all content in a well-formatted `.md` and `.txt` structure.
- **Streamlit UI**: Lets users input a URL, view logs, and download reports easily.

###  Flow:

1. **User Input**: URL is provided via Streamlit or CLI.
2. **Scraper Engine**:
   - Visits the main page.
   - Finds internal links.
   - Extracts visible content from each page.
   - Skips duplicates and external domains.
3. **File Output**:
   - Saves one combined Markdown file (`scraped_report.md`).
   - Saves individual text files in a `pages/` folder for each subpage.

---

##  4. How the Code Works

### Main Functions:

- `scrape_website(url, visited)`: 
  - Recursively scrapes all valid subpages.
  - Extracts only visible text content.
  
- `extract_text(soup)`:
  - Removes `<script>`, `<style>`, and other non-visible tags.
  - Returns cleaned text for each page.

- `save_report(url, contents)`:
  - Saves all scraped data in a formatted `.md` file.
  - Also saves per-page `.txt` files in a `pages/` folder.

### Streamlit App:

- Takes URL input from the user.
- Displays scraping logs and messages.
- On submit, calls the scraper and generates reports.
- Streamlit GUI makes scraping accessible to non-programmers.
- Run 'streamlit run WB.py' in your terminal to run the file locally on your device after downloading the file

---

