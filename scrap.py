from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Initialize the WebDriver with ChromeDriverManager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the URL
driver.get('https://emedicine.medscape.com/emergency_medicine')

# Find the button by class name and click it
try:
    expand_button = driver.find_element(By.CLASS_NAME, 'topic-expand')
    expand_button.click()
    print("Button clicked successfully!")
except Exception as e:
    print("Error in clicking the button:", str(e))

# Close the driver when done
driver.quit()
