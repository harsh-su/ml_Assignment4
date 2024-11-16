import os
import requests
from bs4 import BeautifulSoup
import time

class ImageDownloader:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.saved_folder = 'images'
        # Using Bing images instead of Google as it's more reliable for scraping
        self.base_url = 'https://www.bing.com/images/search'

    def create_folder(self):
        if not os.path.exists(self.saved_folder):
            os.makedirs(self.saved_folder)

    def get_image_urls(self, query, num_images):
        params = {
            'q': query,
            'form': 'HDRSC2',
            'first': 1
        }

        print('Searching for images...')
        response = requests.get(self.base_url, headers=self.headers, params=params)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find image elements
        image_urls = []
        for img in soup.find_all('img', class_='mimg'):
            if 'src' in img.attrs:
                url = img['src']
                if url.startswith('http'):
                    image_urls.append(url)
                    if len(image_urls) >= num_images:
                        break

        return image_urls

    def download_images(self, urls, query):
        if not urls:
            print("No images found!")
            return

        print(f"Found {len(urls)} images. Starting download...")
        
        for i, url in enumerate(urls):
            try:
                response = requests.get(url, headers=self.headers)
                if response.status_code == 200:
                    # Create a valid filename
                    image_name = os.path.join(self.saved_folder, f"{query}_{i+1}.jpg")
                    with open(image_name, 'wb') as f:
                        f.write(response.content)
                    print(f"Downloaded image {i+1}/{len(urls)}")
                    time.sleep(0.5)  # Add delay to avoid being blocked
            except Exception as e:
                print(f"Error downloading image {i+1}: {str(e)}")
                continue

    def run(self):
        try:
            self.create_folder()
            query = input('What are you looking for? ')
            num_images = int(input('How many images do you want? '))
            
            image_urls = self.get_image_urls(query, num_images)
            self.download_images(image_urls, query)
            
            if image_urls:
                print("\nDownload completed! Check the 'images' folder.")
                print(f"Location: {os.path.abspath(self.saved_folder)}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    downloader = ImageDownloader()
    downloader.run()