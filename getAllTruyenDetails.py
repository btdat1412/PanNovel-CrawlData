import os
import requests
import json
import time
from bs4 import BeautifulSoup

def check_rate_limit(headers):
    if 'X-RateLimit-Remaining' in headers:
        remaining = int(headers['X-RateLimit-Remaining'])
        if remaining == 0:
            return False
    return True

def download_html(url, attempt=1):
    try:
        response = requests.get(url)
        if not check_rate_limit(response.headers):
            if attempt <= 3:  # Retry up to 3 times
                print("Rate limit reached. Waiting for 125 seconds...")
                time.sleep(125)
                return download_html(url, attempt + 1)
            else:
                print("Failed to download after retries. Skipping.")
                log_failed_download(url)
                return None
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Failed to download {url}. Error: {e}")
        return None

def save_html(content, directory, filename):
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)

def log_failed_download(url):
    failed_log_path = os.path.join('data', 'truyen-details', 'failed.json')
    try:
        failed_urls = []
        if os.path.exists(failed_log_path):
            with open(failed_log_path, 'r', encoding='utf-8') as file:
                failed_urls = json.load(file)
        failed_urls.append(url)
        with open(failed_log_path, 'w', encoding='utf-8') as file:
            json.dump(failed_urls, file, indent=4)
    except Exception as e:
        print(f"Error logging failed download: {e}")

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')

    # Find the base directory name (series name) to organize volumes
    series_name_tag = soup.find('span', class_='series-name')
    if series_name_tag:
        series_name = series_name_tag.text.strip()
        base_directory_path = os.path.join('data', 'truyen-details', series_name)

        # Iterate over each volume in the volume list
        volume_sections = soup.find_all('section', class_='volume-list')
        for volume_section in volume_sections:
            volume_title_tag = volume_section.find('span', class_='sect-title')
            if volume_title_tag:
                volume_title = volume_title_tag.text.strip()
                # Replace or handle characters that may not be suitable for directory names
                safe_volume_title = volume_title.replace('/', '_').replace('\\', '_')
                volume_directory_path = os.path.join(base_directory_path, safe_volume_title)

                if not os.path.exists(volume_directory_path):
                    os.makedirs(volume_directory_path, exist_ok=True)
                    print(f"Directory created for volume: {volume_title}")

                # Find all chapter links within the volume section
                links = volume_section.find_all('a', href=True, title=True)
                for link in links:
                    chapter_url = link['href']
                    if not chapter_url.startswith('http'):
                        chapter_url = 'https://ln.hako.vn' + chapter_url
                    chapter_title = link['title']
                    html_content = download_html(chapter_url)
                    if html_content:
                        filename = f"{chapter_title}.html".replace('/', '_')
                        save_html(html_content, volume_directory_path, filename)
                        print(f"Saved {chapter_title} content.")
                    else:
                        log_failed_download(chapter_url)

def process_all_html_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            filepath = os.path.join(directory, filename)
            process_html_file(filepath)

# Example usage
directory_path = 'data/truyen'  
process_all_html_files(directory_path)
