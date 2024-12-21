import requests
import sys
import time
import random

# Consistent User-Agent to match your actual setup
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

def fetch_page(url):
    """
    Fetches the HTML content of the given URL.
    
    Args:
        url (str): The URL of the page to fetch.
        
    Returns:
        str or None: The HTML content of the page if successful, otherwise None.
    """
    headers = {
        "User-Agent": USER_AGENT  # Use a consistent User-Agent
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("Page fetched successfully!")
            return response.text
        else:
            print(f"Failed to fetch the page: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def main():
    """
    Main function to fetch and display a snippet of HTML content.
    """
    if len(sys.argv) < 2:  # Check if a URL is provided as an argument
        print("Usage: python fetch_finn.py <URL>")
        return
    
    url = sys.argv[1]  # Take the URL from the command-line argument
    html_content = fetch_page(url)
    
    if html_content:
        print("\nSnippet of fetched HTML content:\n")
        print(html_content[:500])  # Print the first 500 characters to avoid overwhelming the console

        # Introduce a random delay to mimic human behavior
        delay = random.uniform(2, 5)
        print(f"\nWaiting for {delay:.2f} seconds before the next action...")
        time.sleep(delay)

if __name__ == "__main__":
    main()
