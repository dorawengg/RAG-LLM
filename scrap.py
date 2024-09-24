from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fpdf import FPDF
from selenium.common.exceptions import TimeoutException, NoSuchElementException


# Initialize Chrome with WebDriver Manager
options = Options()
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)
driver.get('https://emedicine.medscape.com/emergency_medicine')

# Setup WebDriverWait
wait = WebDriverWait(driver, 1)

# Attempt to click the "Log In" link
try:
    # Using PARTIAL_LINK_TEXT to find the login link if the full text isn't a match
    login_link = wait.until(EC.element_to_be_clickable(
        (By.PARTIAL_LINK_TEXT, "Log In")))
    login_link.click()
    print("Navigated to login page.")
except Exception as e:
    print("Failed to find or click the 'Log In' link:", str(e))
    driver.quit()  # Exit if login cannot be initiated

wait = WebDriverWait(driver, 5)

# Email and Password credentials
email_xpath = '//*[@id="loginForm"]/div[1]/div[1]/div/div/input'
password_xpath = '//*[@id="password"]/div/input'

# Wait for the email input to be visible and clear any pre-filled data, then send the email
wait.until(EC.visibility_of_element_located((By.XPATH, email_xpath))).clear()
driver.find_element(By.XPATH, email_xpath).send_keys('dweng2210@gmail.com')

# Wait for the password input to be visible, clear any pre-filled data, then send the password
wait.until(EC.visibility_of_element_located(
    (By.XPATH, password_xpath))).clear()
driver.find_element(By.XPATH, password_xpath).send_keys('ILikeMedScape123!')


wait = WebDriverWait(driver, 1)

# Attempt to click the "Log In" link
try:
    driver.find_element(
        By.XPATH, '//*[@id="loginForm"]/div[2]/button').click()
except Exception as e:
    print("Failed to find or click the 'Log In' button:", str(e))
    driver.quit()  # Exit if login cannot be initiated

# Setup PDF document
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

wait = WebDriverWait(driver, 1)

# Click the expand button to reveal topics
expand_button_xpath = '//*[@id="bodypadding"]/div[3]/div[1]/div[4]/span'
wait.until(EC.element_to_be_clickable((By.XPATH, expand_button_xpath))).click()

wait = WebDriverWait(driver, 1)
# Collect all links under each 'topic-head'
all_links = []
topic_heads = driver.find_elements(By.CLASS_NAME, 'topic-head')
for head in topic_heads:
    try:
        ul = wait.until(EC.visibility_of(
            head.find_element(By.XPATH, './following-sibling::ul')))
        links = ul.find_elements(By.TAG_NAME, 'a')
        for link in links:
            all_links.append(link.get_attribute('href'))
    except Exception as e:
        print(f"Error processing topic head: {str(e)}")

# Visit each link and interact with lists, then scrape content
for link in all_links[:2]:
    driver.get(link)
    print(link)
    try:
        # get the header
        header = driver.find_element(By.TAG_NAME, 'h1')
        header_text = header.text
        print(header_text)

        # click through the side nav
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

        # Later, loop through the collected hrefs to navigate
        for href in hrefs:
            try:
                driver.get(href)  # Navigate to the href
                print(f"Clicked on: {href}")
                # Perform actions on the page or wait if necessary
                # Wait for the page to load or for dynamic content
                wait = WebDriverWait(driver, 1)
                content = driver.find_element(
                    By.ID, 'drugdbmain')
                print(content.text)
            except Exception as e:
                print(f"Error navigating to {href}: {str(e)}")

    except Exception as e:
        print(f"Error scraping {link}: {str(e)}")


# Output PDF
pdf.output("scraped_content.pdf")
driver.quit()
