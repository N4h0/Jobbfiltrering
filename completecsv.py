import csv
import os
import time
import random
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def fetch_page_with_selenium(url):
    """
    Uses Selenium to render and fetch the fully loaded HTML content of a job page.

    Args:
        url (str): The URL of the job page.

    Returns:
        str: The fully rendered HTML content.
    """
    service = Service("C:\chromedriver-win64\chromedriver.exe")  # Update this to your actual ChromeDriver path
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        time.sleep(5)  # Wait for the page to fully load
        return driver.page_source
    finally:
        driver.quit()

def extract_job_details(html):
    """
    Extracts detailed job information from the job page HTML.

    Args:
        html (str): The HTML content of the job detail page.

    Returns:
        dict: Extracted details including stillingstittel, deadline, sted, bransje, and stillingsfunksjon.
    """
    soup = BeautifulSoup(html, "html.parser")
    details = {
        "stillingstittel": None,
        "deadline": None,
        "sted": None,
        "bransje": None,
        "stillingsfunksjon": None
    }

        # Extracting stillingstittel from the h2 tag with class 't2' or 'md:t1'
    title_tag = soup.find("h2", class_=["t2", "md:t1"])
    if title_tag:
        details["stillingstittel"] = title_tag.text.strip()
    else:
        print("Could not find the <h2> tag for job title.")

    # Extracting deadline from the ul list items
    try:
        deadline_tag = soup.find("li", class_="flex flex-col")
        if deadline_tag and "Frist" in deadline_tag.text:
            span_tag = deadline_tag.find("span", class_="font-bold")
            if span_tag:
                details["deadline"] = span_tag.text.strip()
    except Exception as e:
        print(f"Error extracting deadline: {e}")
    # Extracting 'sted', 'bransje', and 'stillingsfunksjon' from specific list items
    try:
        ul_tag = soup.find("ul", class_="space-y-10")
        if ul_tag:
            for li in ul_tag.find_all("li"):
                text = li.text.strip()
                if "Sted:" in text:
                    details["sted"] = text.split("Sted:")[1].strip()
                if "Bransje:" in text:
                    details["bransje"] = ', '.join(link.text for link in li.find_all("a"))
                if "Stillingsfunksjon:" in text:
                    details["stillingsfunksjon"] = ', '.join(link.text for link in li.find_all("a"))
    except Exception as e:
        print(f"Error extracting ul tag: {e}")
        
    return details


def update_csv_with_details(csv_filename="jobs.csv"):
    """
    Loops through the CSV file and updates missing details for jobs without a deadline.

    Args:
        csv_filename (str): The CSV file name.
    """
    updated_rows = []
    with open(csv_filename, "r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        print("Lol hallo")
        for row in reader:
            if not row.get("deadline"):
                print(f"Processing job: {row['job_url']}")
                joburl = row.get("job_url", "unknown")
                html_content = fetch_page_with_selenium(joburl)

                if html_content:
                    print("Extracting job details...")
                    details = extract_job_details(html_content)
                    row.update(details)

                updated_rows.append(row)

    with open(csv_filename, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    print(f"CSV file '{csv_filename}' updated successfully.")

def main():
    csv_filename = "jobs.csv"
    if not os.path.exists(csv_filename):
        print(f"File {csv_filename} not found.")
        return

    update_csv_with_details(csv_filename)

if __name__ == "__main__":
    main()
