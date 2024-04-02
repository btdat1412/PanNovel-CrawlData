import requests

def test_request(url):
    try:
        # Send a GET request to the specified URL
        response = requests.get(url)
        
        # Display the response headers and status code
        print("Headers:", response.headers)
        print("Status Code:", response.status_code)
        
        # Save the HTML content to a file
        with open('/Users/admin/Desktop/Stuff/Code/PanNovel/crawl//test/page.html', 'w', encoding='utf-8') as file:
            file.write(response.text)
        print("Content saved to /test/page.html")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # The specific URL to test
    url = 'https://ln.hako.vn/truyen/1-seirei-tsukai-no-blade-dance/c1-chuong-1-nguoi-la-tinh-linh-cua-ta'
    
    # Call the test_request function with the URL
    test_request(url)
