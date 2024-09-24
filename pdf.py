import json
import re

# Load the JSON data from a file
with open('scraped_content.json', 'r') as file:
    data = json.load(file)

# Define a function to remove consecutive newlines


def remove_consecutive_newlines(text):
    return re.sub(r'\n+', '\n', text)

# Define a function to format the data


def format_article(article):
    title = article.get('name', 'No title')
    link = article.get('link', 'No link')
    content = remove_consecutive_newlines(article.get('content', 'No content'))
    formatted = f"Title: {title}\n"
    formatted += f"Link: {link}\n"
    formatted += f"Content:\n{content}\n"
    formatted += "-" * 80 + "\n"  # Separator line between articles
    return formatted


# Process each article to clean up the content
for article in data:
    if 'content' in article:
        article['content'] = remove_consecutive_newlines(article['content'])

# Specify the output TXT file
output_filename = 'output.txt'

# Write the formatted data to the TXT file
with open(output_filename, 'w') as txt_file:
    for article in data:
        txt_file.write(format_article(article))

print(f"Data has been written to {output_filename}")
