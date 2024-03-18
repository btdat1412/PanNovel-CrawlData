from bs4 import BeautifulSoup
import json
from pathlib import Path

# Base path for the HTML files and JSON output
base_html_path = 'data/danh-sach/page{}.html'
output_json_path = Path('data/truyen/truyen-href.json')

# Ensure the output directory exists
output_json_path.parent.mkdir(parents=True, exist_ok=True)

# Initialize a list to hold all extracted links
all_truyen_links = []

# Loop through all pages
for page_num in range(1, 70):  # From page 1 to 69
    html_path = Path(base_html_path.format(page_num))
    
    # Proceed only if the HTML file exists
    if html_path.exists():
        with open(html_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            
            # Find all <div> elements with the specified class
            divs = soup.find_all('div', class_='thumb_attr series-title')
            
            for div in divs:
                # Extract the href attribute of the <a> tag within each <div>
                a_tag = div.find('a')
                if a_tag and a_tag.has_attr('href'):
                    all_truyen_links.append(a_tag['href'])
    else:
        print(f"HTML file for page {page_num} does not exist.")

# Save the accumulated links to a JSON file
with open(output_json_path, 'w', encoding='utf-8') as json_file:
    json.dump(all_truyen_links, json_file, indent=4, ensure_ascii=False)

print(f"All extracted links saved to {output_json_path}")
