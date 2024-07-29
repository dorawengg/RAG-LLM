import requests
from bs4 import BeautifulSoup
import pdfkit
import os

# Define the base URL to scrape
base_url = "https://emedicine.medscape.com"
url = f"{base_url}/emergency_medicine"

# Send a GET request to the URL
response = requests.get(url)
response.raise_for_status()  # Check for request errors

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all relevant links (adjust the selector as needed)
topic_sections = soup.find_all('div', class_='topic-section')

# Create a list to hold all the article links
article_links = []

# Extract links from the topic sections
for section in topic_sections:
    links = section.find_all('a', href=True)
    for link in links:
        article_links.append(base_url + link['href'])

# Define a function to scrape and save content as a PDF


def save_as_pdf(url, output_pdf):
    # Send a GET request to the article URL
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the main content (adjust the selector as needed)
    # Adjust the class or tag as needed
    main_content = soup.find('div', class_='content')

    # Create an HTML file to convert to PDF
    html_file = "temp.html"
    with open(html_file, "w", encoding='utf-8') as file:
        file.write(str(main_content))

    # Convert the HTML file to a PDF
    pdfkit.from_file(html_file, output_pdf)

    # Clean up the temporary HTML file
    os.remove(html_file)

    print(f"PDF saved as {output_pdf}")


# Iterate over all article links and save each as a PDF
for i, link in enumerate(article_links):
    pdf_filename = f"emedicine_article_{i+1}.pdf"
    save_as_pdf(link, pdf_filename)
