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
    # topic_heads = driver.find_elements(By.CLASS_NAME, 'topic-head')
    # for head in topic_heads:
    #     try:
    #         ul = wait.until(EC.visibility_of(
    #             head.find_element(By.XPATH, './following-sibling::ul')))
    #         links = ul.find_elements(By.TAG_NAME, 'a')
    #         for link in links:
    #             href = link.get_attribute('href')
    #             if href:
    #                 scraped_data.append(
    #                     {"name": link.text, "link": href, "content": ""})
    #     except Exception as e:
    #         print(f"Error processing topic head: {str(e)}")

    scraped_data = [
        {
            "name": "Hyperthyroidism and Thyrotoxicosis",
            "link": "https://emedicine.medscape.com/article/121865-overview",
            "content": ""
        },
        {
            "name": "Hyperthyroidism, Thyroid Storm, and Graves Disease",
            "link": "https://emedicine.medscape.com/article/767130-overview",
            "content": ""
        },
        {
            "name": "Hypertriglyceridemia",
            "link": "https://emedicine.medscape.com/article/126568-overview",
            "content": ""
        },
        {
            "name": "Hypokalemia in Emergency Medicine",
            "link": "https://emedicine.medscape.com/article/767448-overview",
            "content": ""
        },
        {
            "name": "Hyponatremia in Emergency Medicine",
            "link": "https://emedicine.medscape.com/article/767624-overview",
            "content": ""
        },
        {
            "name": "Hypoparathyroidism in Emergency Medicine",
            "link": "https://emedicine.medscape.com/article/767744-overview",
            "content": ""
        },
        {
            "name": "Hypophosphatemia in Emergency Medicine",
            "link": "https://emedicine.medscape.com/article/767955-overview",
            "content": ""
        },
        {
            "name": "Hypopituitarism (Panhypopituitarism)",
            "link": "https://emedicine.medscape.com/article/122287-overview",
            "content": ""
        },
        {
            "name": "Hypothyroidism",
            "link": "https://emedicine.medscape.com/article/122393-overview",
            "content": ""
        },
        {
            "name": "Hypothyroidism and Myxedema Coma",
            "link": "https://emedicine.medscape.com/article/768053-overview",
            "content": ""
        },
        {
            "name": "Iodine Deficiency",
            "link": "https://emedicine.medscape.com/article/122714-overview",
            "content": ""
        },
        {
            "name": "Localized Lipodystrophy",
            "link": "https://emedicine.medscape.com/article/123125-overview",
            "content": ""
        },
        {
            "name": "Metabolic Acidosis in Emergency Medicine",
            "link": "https://emedicine.medscape.com/article/768268-overview",
            "content": ""
        },
        {
            "name": "Obesity",
            "link": "https://emedicine.medscape.com/article/123702-overview",
            "content": ""
        },
        {
            "name": "Polygenic Hypercholesterolemia",
            "link": "https://emedicine.medscape.com/article/121424-overview",
            "content": ""
        },
        {
            "name": "Scurvy",
            "link": "https://emedicine.medscape.com/article/125350-overview",
            "content": ""
        },
        {
            "name": "Thyroid Dysfunction Induced by Amiodarone Therapy",
            "link": "https://emedicine.medscape.com/article/129033-overview",
            "content": ""
        },
        {
            "name": "Type Ia Glycogen Storage Disease",
            "link": "https://emedicine.medscape.com/article/119318-overview",
            "content": ""
        },
        {
            "name": "Type Ib Glycogen Storage Disease",
            "link": "https://emedicine.medscape.com/article/119412-overview",
            "content": ""
        },
        {
            "name": "Type II Glycogen Storage Disease (Pompe Disease)",
            "link": "https://emedicine.medscape.com/article/119506-overview",
            "content": ""
        },
        {
            "name": "Type III Glycogen Storage Disease (Forbes-Cori Disease)",
            "link": "https://emedicine.medscape.com/article/119597-overview",
            "content": ""
        },
        {
            "name": "Type IV Glycogen Storage Disease",
            "link": "https://emedicine.medscape.com/article/119690-overview",
            "content": ""
        },
        {
            "name": "Type V Glycogen Storage Disease",
            "link": "https://emedicine.medscape.com/article/119777-overview",
            "content": ""
        },
        {
            "name": "Type VI Glycogen Storage Disease",
            "link": "https://emedicine.medscape.com/article/119873-overview",
            "content": ""
        },
        {
            "name": "Type VII Glycogen Storage Disease",
            "link": "https://emedicine.medscape.com/article/119947-overview",
            "content": ""
        },
        {
            "name": "Vitamin A Deficiency",
            "link": "https://emedicine.medscape.com/article/126004-overview",
            "content": ""
        },
        {
            "name": "Acrodynia",
            "link": "https://emedicine.medscape.com/article/1088639-overview",
            "content": ""
        },
        {
            "name": "Altitude Illness - Cerebral Syndromes",
            "link": "https://emedicine.medscape.com/article/768478-overview",
            "content": ""
        },
        {
            "name": "Altitude Illness - Pulmonary Syndromes",
            "link": "https://emedicine.medscape.com/article/773065-overview",
            "content": ""
        },
        {
            "name": "Animal Bites in Emergency Medicine",
            "link": "https://emedicine.medscape.com/article/768875-overview",
            "content": ""
        },
        {
            "name": "Barotrauma",
            "link": "https://emedicine.medscape.com/article/768618-overview",
            "content": ""
        },
        {
            "name": "Bedbug Bites",
            "link": "https://emedicine.medscape.com/article/1088931-overview",
            "content": ""
        },
        {
            "name": "Black Heel (Calcaneal Petechiae)",
            "link": "https://emedicine.medscape.com/article/1087469-overview",
            "content": ""
        },
        {
            "name": "Brown Recluse Spider Envenomation",
            "link": "https://emedicine.medscape.com/article/772295-overview",
            "content": ""
        },
        {
            "name": "Brown Snake Envenomation",
            "link": "https://emedicine.medscape.com/article/772066-overview",
            "content": ""
        },
        {
            "name": "Caterpillar Envenomation",
            "link": "https://emedicine.medscape.com/article/772949-overview",
            "content": ""
        },
        {
            "name": "Centipede Envenomation",
            "link": "https://emedicine.medscape.com/article/769448-overview",
            "content": ""
        },
        {
            "name": "Chemical Burns",
            "link": "https://emedicine.medscape.com/article/769336-overview",
            "content": ""
        },
        {
            "name": "Cnidaria Envenomation",
            "link": "https://emedicine.medscape.com/article/769538-overview",
            "content": ""
        },
        {
            "name": "Cobra Envenomation",
            "link": "https://emedicine.medscape.com/article/771918-overview",
            "content": ""
        },
        {
            "name": "Conidae",
            "link": "https://emedicine.medscape.com/article/769638-overview",
            "content": ""
        },
        {
            "name": "Copperhead and Cottonmouth Envenomation",
            "link": "https://emedicine.medscape.com/article/771329-overview",
            "content": ""
        },
        {
            "name": "Coral Snake Envenomation",
            "link": "https://emedicine.medscape.com/article/771701-overview",
            "content": ""
        },
        {
            "name": "Rectus Sheath Hematoma",
            "link": "https://emedicine.medscape.com/article/776871-overview",
            "content": ""
        },
        {
            "name": "Absence Seizures",
            "link": "https://emedicine.medscape.com/article/1183858-overview",
            "content": ""
        },
        {
            "name": "Breech Delivery",
            "link": "https://emedicine.medscape.com/article/797690-overview",
            "content": ""
        }, {
            "name": "Early Pregnancy Loss",
            "link": "https://emedicine.medscape.com/article/266317-overview",
            "content": ""
        }, {
            "name": "Lacrimal Gland Tumors",
            "link": "https://emedicine.medscape.com/article/1210619-overview",
            "content": ""
        }, {
            "name": "Emergent Management of Croup (Laryngotracheobronchitis)",
            "link": "https://emedicine.medscape.com/article/800866-overview",
            "content": ""
        }, {
            "name": "CBRNE - Opioids/Benzodiazepines Poisoning",
            "link": "https://emedicine.medscape.com/article/834190-overview",
            "content": ""
        }
    ]

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
