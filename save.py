import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Initialize Chrome with WebDriver Manager
options = Options()
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)
driver.get('https://emedicine.medscape.com/emergency_medicine')

# Setup WebDriverWait
wait = WebDriverWait(driver, 1)

# Initialize the dictionary to store scraped data
scraped_data = []

try:
    # Attempt to click the "Log In" link
    try:
        login_link = wait.until(EC.element_to_be_clickable(
            (By.PARTIAL_LINK_TEXT, "Log In")))
        login_link.click()
        print("Navigated to login page.")
    except Exception as e:
        print("Failed to find or click the 'Log In' link:", str(e))
        driver.quit()
        exit()

    wait = WebDriverWait(driver, 5)

    # Email and Password credentials
    email_xpath = '//*[@id="loginForm"]/div[1]/div[1]/div/div/input'
    password_xpath = '//*[@id="password"]/div/input'

    # Wait for the email input to be visible and clear any pre-filled data, then send the email
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, email_xpath))).clear()
    driver.find_element(By.XPATH, email_xpath).send_keys('dweng2210@gmail.com')

    # Wait for the password input to be visible, clear any pre-filled data, then send the password
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, password_xpath))).clear()
    driver.find_element(By.XPATH, password_xpath).send_keys(
        'ILikeMedScape123!')

    wait = WebDriverWait(driver, 1)

    # Attempt to click the "Log In" button
    try:
        driver.find_element(
            By.XPATH, '//*[@id="loginForm"]/div[2]/button').click()
    except Exception as e:
        print("Failed to find or click the 'Log In' button:", str(e))
        driver.quit()
        exit()

    wait = WebDriverWait(driver, 1)

    # Click the expand button to reveal topics
    expand_button_xpath = '//*[@id="bodypadding"]/div[3]/div[1]/div[4]/span'
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, expand_button_xpath))).click()

    wait = WebDriverWait(driver, 1)

    # Collect all links under each 'topic-head'
    topic_heads = driver.find_elements(By.CLASS_NAME, 'topic-head')
    for head in topic_heads:
        try:
            ul = wait.until(EC.visibility_of(
                head.find_element(By.XPATH, './following-sibling::ul')))
            links = ul.find_elements(By.TAG_NAME, 'a')
            for link in links:
                href = link.get_attribute('href')
                if href:
                    scraped_data.append(
                        {"name": link.text, "link": href, "content": ""})
        except Exception as e:
            print(f"Error processing topic head: {str(e)}")

    # Visit each link and interact with lists, then scrape content
    for entry in scraped_data:
        try:
            driver.get(entry["link"])
            print(entry["link"])

            # Get the header
            header = driver.find_element(By.TAG_NAME, 'h1')
            header_text = header.text
            print(header_text)

            # Click through the side nav
            nav = driver.find_element(
                By.XPATH, '//*[@id="leftcol"]/div[3]/div/div[2]')
            navs = nav.find_elements(By.TAG_NAME, 'a')
            hrefs = []
            for n in navs:
                print(n.text)  # Print the text of the link for debugging
                try:
                    href = n.get_attribute('href')
                    if href and href != "#a1":  # Check if href is not the specific unwanted value
                        hrefs.append(href)  # Append to the list
                        print(href)  # Print the full URL for debugging
                except Exception as e:
                    print(f"Error finding href: {str(e)}")

            # Scrape content
            for href in hrefs:
                try:
                    driver.get(href)  # Navigate to the href
                    print(f"Clicked on: {href}")
                    # Wait for the page to load or for dynamic content
                    wait = WebDriverWait(driver, 1)
                    content = driver.find_element(By.ID, 'drugdbmain')
                    # Append content to the existing text
                    entry["content"] += content.text + "\n\n"
                except Exception as e:
                    print(f"Error navigating to {href}: {str(e)}")

        except Exception as e:
            print(f"Error scraping {entry['link']}: {str(e)}")

finally:
    # Output JSON regardless of success or failure
    with open("scraped_content.json", "w") as f:
        json.dump(scraped_data, f, indent=4)
    driver.quit()
