from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup Selenium with ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URL you want to fetch
url = 'https://ln.hako.vn/truyen/1-seirei-tsukai-no-blade-dance/c2-chuong-2-hoc-vien-tinh-linh-areishia'

# Open the URL
driver.get(url)

# Wait for JavaScript to load. Adjust the sleep time as necessary.
time.sleep(5)

# Get the rendered page HTML
html_content = driver.page_source

# Optionally, save the HTML content to a file
with open('webpage.html', 'w', encoding='utf-8') as file:
    file.write(html_content)

print('Download successful and content saved to webpage.html.')

# Don't forget to close the browser
driver.quit()
