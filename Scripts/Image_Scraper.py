import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

# === INDSTILLINGER ============================================================
DIR = Path("./images")
DIR.mkdir(exist_ok=True)

REQUEST_TIMEOUT = 10        # sekunder
PAUSE_BETWEEN_IMAGES = 0.2  # taktforsinkelse så vi er høflige
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ImageHarvester/1.0)"}

DOWNLOADED_URL_LIST = []
# ==============================================================================


def sanitize_filename(url: str) -> str:
    """
    Trækker filnavnet ud af en URL og fjerner evt. query-string.
    Får vi et tomt navn (fx når billedet hedder '/'), returneres 'index'.
    """
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path) or "index"
    return filename.split("?")[0]


def download_file(url: str, dest: Path) -> bool:
    """
    Henter en fil og gemmer den til 'dest'.
    Returnerer True ved succes, ellers False.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        dest.write_bytes(response.content)
        return True
    except Exception as exc:
        print(f"      ✘ Kunne ikke hente {url}: {exc}")
        return False


def scrape_page(page_url: str) -> None:
    """
    Finder alle billeder på en enkelt side og gemmer dem.
    """

    global DOWNLOADED_URL_LIST

    try:
        html = requests.get(page_url, headers=HEADERS, timeout=REQUEST_TIMEOUT).text
    except Exception as exc:
        print(f"   ✘ Fejlede ved indlæsning af {page_url}: {exc}")
        return

    soup = BeautifulSoup(html, "html.parser")
    images = soup.find_all("img")

    for img in images:
        src = img.get("data-src") or img.get("src")
        if not src or src.startswith("data:"):
            continue  # spring base64/data-URI over
        img_url = urljoin(page_url, src)
        filename = sanitize_filename(img_url)
        dest = DIR / filename

        # Undgå navnekollisioner
        if dest.exists():
            stem, ext = dest.stem, dest.suffix
            counter = 1
            while dest.exists():
                dest = DIR / f"{stem}_{counter}{ext}"
                counter += 1

        if img_url in DOWNLOADED_URL_LIST or img_url.endswith(".webp"):
            continue

        if download_file(img_url, dest):
            print(f"      ✓ {dest.name} gemt")
            DOWNLOADED_URL_LIST.append(img_url)
            time.sleep(PAUSE_BETWEEN_IMAGES)


def main(json_path: str) -> None:
    print(f"🔍 Læser URL-liste fra {json_path}")
    with open(json_path, "r", encoding="utf-8") as fp:
        data = json.load(fp)

    urls = [entry["loc"] for entry in data.get("urlset", {}).get("url", [])]
    print(f"🔗 Fundet {len(urls)} sider\n")

    for i, page_url in enumerate(urls, start=1):
        print(f"[{i}/{len(urls)}] Henter billeder fra {page_url}")
        scrape_page(page_url)
        print()

    print("✅ Færdig!")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Brug: python download_images.py <sti/til/sitemap.json>")
        sys.exit(1)
    main(sys.argv[1])
