import requests
from pathlib import Path

# Base URL of the website with a placeholder for page numbers
base_url = 'https://ln.hako.vn/danh-sach?page={}'

# Base path where to save the HTML content, with a placeholder for page numbers
base_save_path = 'data/danh-sach/page{}.html'

# Ensure the base directory exists
Path('data/danh-sach').mkdir(parents=True, exist_ok=True)

for page_number in range(60, 70):  # Starting from 1 to 69
    # Format the URL and save path with the current page number
    url = base_url.format(page_number)
    save_path = Path(base_save_path.format(page_number))

    try:
        # Send a GET request to the website
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Save the HTML content to the file
            with open(save_path, 'w', encoding='utf-8') as file:
                file.write(response.text)
            print(f"HTML content of page {page_number} saved successfully at {save_path}")
        else:
            print(f"Failed to retrieve page {page_number}: Status code {response.status_code}")
    except Exception as e:
        print(f"An error occurred while retrieving page {page_number}: {e}")
