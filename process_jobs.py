import csv
import sys
from bs4 import BeautifulSoup
from fetch_finn import fetch_page  # Import the fetch_page function

def parse_jobs(html):
    """
    Parses job listings from the given HTML content.
    
    Args:
        html (str): The HTML content of the page.
        
    Returns:
        list of dict: Extracted job information.
    """
    soup = BeautifulSoup(html, "html.parser")
    jobs = []
    articles = soup.find_all("article", class_="sf-search-ad")
    
    for article in articles:
        try:
            # Extract job title and URL
            h2_tag = article.find("h2", class_="h4")
            job_title = h2_tag.text.strip()
            job_url = h2_tag.find("a")["href"]
            
            # Extract employer and positions
            employer_tag = article.find("div", class_="flex flex-col text-xs")
            employer = employer_tag.find_all("span")[0].text.strip()
            positions = employer_tag.find_all("span")[1].text.strip()
            
            # Extract finnkode from job_url
            finnkode = job_url.split("finnkode=")[-1]
            
            # Append job information with placeholders for additional fields
            jobs.append({
                "finnkode": finnkode,
                "job_title": job_title,
                "job_url": job_url,
                "employer": employer,
                "positions": positions,
                "stillingstittel": None,  # Placeholder for job title (detailed)
                "deadline": None,        # Placeholder for application deadline
                "sted": None,            # Placeholder for location
                "bransje": None,         # Placeholder for industry
                "stillingsfunksjon": None  # Placeholder for job function
            })
        except Exception as e:
            print(f"Error parsing article: {e}")
    
    return jobs

def read_existing_jobs(filename="jobs.csv"):
    """
    Reads existing jobs from the CSV file.
    
    Args:
        filename (str): The CSV file name.
        
    Returns:
        set: A set of existing finnkode values.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return {row["finnkode"] for row in reader}
    except FileNotFoundError:
        # If the file doesn't exist, return an empty set
        return set()

def save_new_jobs(jobs, filename="jobs.csv"):
    """
    Saves only new jobs to the CSV file.
    
    Args:
        jobs (list of dict): Job information.
        filename (str): The CSV file name.
    """
    fieldnames = [
        "finnkode", "job_title", "job_url", "employer", "positions",
        "stillingstittel", "deadline", "sted", "bransje", "stillingsfunksjon"
    ]

    existing_finnkodes = read_existing_jobs(filename)
    new_jobs = [job for job in jobs if job["finnkode"] not in existing_finnkodes]
    
    if new_jobs:
        with open(filename, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:  # Write header only if the file is empty
                writer.writeheader()
            writer.writerows(new_jobs)
        print(f"Added {len(new_jobs)} new jobs to {filename}.")
    else:
        print("No new jobs to add.")

def main():
    """
    Main function to parse and save jobs.
    """
    if len(sys.argv) < 2:
        print("Usage: python process_jobs.py <URL>")
        return
    
    url = sys.argv[1]  # Take the URL from the command-line argument
    html_content = fetch_page(url)
    
    if html_content:
        jobs = parse_jobs(html_content)
        if jobs:
            save_new_jobs(jobs)
        else:
            print("No jobs found.")
    else:
        print("Failed to fetch the page.")

if __name__ == "__main__":
    main()
