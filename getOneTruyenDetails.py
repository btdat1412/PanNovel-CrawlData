import os
import requests
from bs4 import BeautifulSoup

def download_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except Exception as e:
        print(f"Failed to download {url}. Error: {e}")
        return None

def save_html(content, directory, filename):
    os.makedirs(directory, exist_ok=True)  # Create directory if it doesn't exist
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')

    # Extract series name and create directory
    series_name_tag = soup.find('span', class_='series-name')
    if series_name_tag:
        series_name = series_name_tag.text.strip()
        directory_path = os.path.join('data', 'truyen-details', series_name)
    else:
        print("Series name not found.")
        return

    # Find all chapters within the volume list
    chapter_names = soup.find_all('div', class_='chapter-name')
    if chapter_names:
        for chapter_name in chapter_names:
            link = chapter_name.find('a', href=True, title=True)  # Find the 'a' tag inside the 'chapter-name' div
            if link:
                chapter_url = link['href']
                if not chapter_url.startswith('http'):
                    chapter_url = 'https://ln.hako.vn' + chapter_url
                chapter_title = link['title']
                html_content = download_html(chapter_url)
                if html_content:
                    # Replace slashes in chapter title to avoid path issues
                    filename = f"{chapter_title}.html".replace('/', '_')
                    save_html(html_content, directory_path, filename)
                    print(f"Saved {chapter_title} content.")
    else:
        print("No chapter names found.")

# Example usage
html_file = '/Users/admin/Desktop/Stuff/Code/PanNovel/crawl/data/truyen/1-seirei-tsukai-no-blade-dance.html'  # Update this path to your specific HTML file
# process_html_file(html_file)
url = 'https://ln.hako.vn/truyen/1-seirei-tsukai-no-blade-dance/c2-chuong-2-hoc-vien-tinh-linh-areishia'

# Sending a GET request to the URL
response = requests.get(url)

# Checking if the request was successful
if response.status_code == 200:
    html_content = response.text
    # Optionally, save the HTML content to a file
    with open('webpage.html', 'w', encoding='utf-8') as file:
        file.write(html_content)
    print('Download successful and content saved to webpage.html.')
else:
    print('Failed to retrieve the webpage. Status code:', response.status_code)