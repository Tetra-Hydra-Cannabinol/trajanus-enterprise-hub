"""
Document Hunter Module
Downloads PDFs from state DOT websites for traffic engineering guides
"""

import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime
import config


def sanitize_filename(name: str) -> str:
    """Clean filename for safe saving"""
    # Remove/replace invalid characters
    clean = re.sub(r'[<>:"/\\|?*]', '_', name)
    clean = re.sub(r'\s+', '_', clean)
    clean = clean[:100]  # Limit length
    return clean


def get_pdf_links(url: str, domain_filter: str = ".gov") -> list:
    """
    Scrape a page for PDF links.

    Args:
        url: Page URL to scrape
        domain_filter: Only include links from domains containing this string

    Returns:
        List of PDF URLs found
    """
    pdf_links = []

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        for link in soup.find_all("a", href=True):
            href = link["href"]

            # Make absolute URL
            full_url = urljoin(url, href)

            # Check if it's a PDF
            if full_url.lower().endswith(".pdf"):
                # Check domain filter
                if domain_filter in urlparse(full_url).netloc:
                    pdf_links.append({
                        "url": full_url,
                        "text": link.get_text(strip=True) or "Untitled"
                    })

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
    except Exception as e:
        print(f"Error parsing {url}: {e}")

    return pdf_links


def download_pdf(url: str, save_dir: str, prefix: str = "") -> str:
    """
    Download a PDF file.

    Args:
        url: PDF URL
        save_dir: Directory to save to
        prefix: Optional prefix for filename (e.g., state name)

    Returns:
        Path to saved file, or empty string on failure
    """
    try:
        # Create directory if needed
        os.makedirs(save_dir, exist_ok=True)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=60, stream=True)
        response.raise_for_status()

        # Get filename from URL or Content-Disposition
        filename = os.path.basename(urlparse(url).path)
        if not filename.endswith(".pdf"):
            filename = "document.pdf"

        # Add prefix and date
        date_str = datetime.now().strftime("%Y%m%d")
        if prefix:
            filename = f"{prefix}_{date_str}_{sanitize_filename(filename)}"
        else:
            filename = f"{date_str}_{sanitize_filename(filename)}"

        filepath = os.path.join(save_dir, filename)

        # Check if file already exists
        if os.path.exists(filepath):
            print(f"  Already exists: {filename}")
            return filepath

        # Download
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"  Downloaded: {filename}")
        return filepath

    except requests.RequestException as e:
        print(f"  Download error for {url}: {e}")
        return ""
    except Exception as e:
        print(f"  Error saving {url}: {e}")
        return ""


def hunt_documents(urls: dict = None) -> list:
    """
    Hunt for documents from DOT websites.

    Args:
        urls: Dict of state -> list of URLs (defaults to config.DOT_URLS)

    Returns:
        List of downloaded file paths
    """
    if urls is None:
        urls = config.DOT_URLS

    downloaded = []

    for state, state_urls in urls.items():
        print(f"\nHunting {state.upper()} DOT documents...")

        for url in state_urls:
            print(f"  Scanning: {url}")

            # Get PDF links from page
            pdf_links = get_pdf_links(url)
            print(f"  Found {len(pdf_links)} PDFs")

            # Download each PDF
            for pdf in pdf_links[:5]:  # Limit to 5 per page
                filepath = download_pdf(
                    pdf["url"],
                    config.DOWNLOAD_DIR,
                    prefix=state.upper()
                )
                if filepath:
                    downloaded.append(filepath)

    return downloaded


if __name__ == "__main__":
    print("=" * 60)
    print("Document Hunter Test")
    print("=" * 60)
    print(f"\nDownload directory: {config.DOWNLOAD_DIR}")
    print("\nTarget URLs:")
    for state, urls in config.DOT_URLS.items():
        print(f"  {state.upper()}:")
        for url in urls:
            print(f"    - {url}")

    print("\nTo run a full hunt, call hunt_documents()")
    print("This will scan DOT sites and download PDFs to the download directory.")

    # Optional: Test a single URL
    # test_url = "https://www.fdot.gov/planning/systems/programs/sm/accman"
    # print(f"\nTesting single URL: {test_url}")
    # links = get_pdf_links(test_url)
    # print(f"Found {len(links)} PDF links")
