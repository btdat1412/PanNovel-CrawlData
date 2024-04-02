import requests
import time
import os
import json

def check_rate_limit(headers):
    """Check the X-RateLimit-Remaining in the headers."""
    if 'X-RateLimit-Remaining' in headers:
        remaining = int(headers['X-RateLimit-Remaining'])
        if remaining == 0:
            return False
    return True

def download_html(url):
    """Download the HTML content for a given URL."""
    try:
        response = requests.get(url)
        if not check_rate_limit(response.headers):
            print("Rate limit reached. Waiting for 125 seconds...")
            time.sleep(125)  # Wait for the rate limit to reset
            return download_html(url)  # Retry after waiting
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except Exception as e:
        print(f"Failed to download {url}. Error: {e}")
        return None

def save_html(content, filename):
    """Save HTML content to a file."""
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

def log_failed_download(url):
    """Log the URL of a failed download to a JSON file."""
    failed_log_path = "data/truyen/failed.json"
    try:
        if os.path.exists(failed_log_path):
            with open(failed_log_path, 'r+', encoding='utf-8') as file:
                failed_urls = json.load(file)
                failed_urls.append(url)
                file.seek(0)
                json.dump(failed_urls, file, indent=4)
        else:
            with open(failed_log_path, 'w', encoding='utf-8') as file:
                json.dump([url], file, indent=4)
    except Exception as e:
        print(f"Error logging failed download: {e}")

def main():
    base_url = "https://ln.hako.vn"
    json_path = "data/truyen/truyen-href.json"

    # Create directories if they don't exist
    os.makedirs(os.path.dirname(json_path), exist_ok=True)

    # Load URLs from the JSON file
    with open(json_path, 'r', encoding='utf-8') as file:
        urls = json.load(file)

    for url_suffix in urls:
        url = f"{base_url}{url_suffix}"
        filename = f"data/truyen/{url_suffix.split('/')[-1]}.html"
        
        # Check if the HTML file already exists
        if os.path.exists(filename):
            print(f"{filename} already exists. Skipping download.")
            continue

        html_content = download_html(url)
        if html_content:
            save_html(html_content, filename)
            print(f"Saved HTML content to {filename}.")
        else:
            print(f"Failed to save content from {url}.")
            log_failed_download(url)

if __name__ == "__main__":
    main()
