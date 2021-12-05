import json
import operator
import time
import csv
from re import sub
from decimal import Decimal

from selenium import webdriver


from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def test_condo():
    driver = webdriver.Chrome()
    driver.get('https://condos.ca/')
    driver.maximize_window()
    time.sleep(2)

    driver.find_element(By.XPATH, "//div[@class='styles___AreaLabel-sc-1nhiula-4 GgENq']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//input[contains(@class, 'react-autosuggest')]").send_keys('Toronto')
    driver.find_element(By.XPATH, "//div[text()='Toronto' and contains(@class, 'hvYQvK')]").click()
    time.sleep(3)
    price_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'dHPUdq')]")
    price_list = []

    for element in price_elements:
        temp = element.text
        value = Decimal(sub(r'[^\d.]', '', temp))
        price_list.append(value)
    price_list.sort(reverse=True)

    print("Printing the price in descending order")
    for i in range(len(price_list)):
        print(price_list[i])

    # Clicking on fifth element as asked. index starts from 1 so used 5.
    driver.find_element(By.XPATH, "(//address[contains(@class, 'gTwVlm')])[5]").click()
    driver.switch_to.window(driver.window_handles[1])
    wait = WebDriverWait(driver, 10)

    wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(@class, 'ccBSix')]")))
    time.sleep(2)
    json_file_name = driver.find_element(By.XPATH, "//h1[contains(@class, 'ccBSix')]").text
    json_file_name = json_file_name + '.json'
    print("JSON File to be used is: " + json_file_name)
    element = driver.find_element(By.XPATH, "//div[contains(@class, 'heNzJh')]")
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.XPATH, "//div[text()='Rooms']"))
    print('scroll done')
    time.sleep(1)
    element.click()

    no_of_rows = len(
        driver.find_elements(By.XPATH, "//table[@class='styles___RoomsTable-sc-tgjfhg-1 efdrQR']/tbody/tr"))

    name = driver.find_elements(By.XPATH, "//table[@class='styles___RoomsTable-sc-tgjfhg-1 efdrQR']/tbody/tr/td[1]")
    size = driver.find_elements(By.XPATH, "//table[@class='styles___RoomsTable-sc-tgjfhg-1 efdrQR']/tbody/tr/td[2]")
    feature = driver.find_elements(By.XPATH, "//table[@class='styles___RoomsTable-sc-tgjfhg-1 efdrQR']/tbody/tr/td[3]")
    property_details = {'rooms': []}

    for i in range(no_of_rows):
        property_details['rooms'].append({
            'name': name[i].text,
            'size': size[i].text,
            'feature': feature[i].text
        })

    with open(json_file_name, 'w') as outfile:
        json.dump(property_details, outfile)


def test_steam_powered():
    # f = open('games.csv', 'w', newline='')
    # writer = csv.writer(f)
    # writer.writerow(['Game Name', 'Release Date', 'Price', 'Price Category'])

    driver = webdriver.Chrome()
    driver.set_page_load_timeout(10)
    driver.implicitly_wait(10)
    driver.get('https://store.steampowered.com/')
    driver.maximize_window()
    driver.find_element(By.XPATH, "//span[contains(@class, 'top_sellers')]").click()
    time.sleep(2)
    title_elements = driver.find_elements(By.XPATH, "//span[@class='title']")

    print("Printing the game names from the Top Seller section in console")
    for element in title_elements:
        print(element.text)
    release_date_elements = driver.find_elements(By.XPATH, "//div[@class='col search_released responsive_secondrow']")
    price_elements = driver.find_elements(By.XPATH,
                                          "//div[@class='col search_price discounted responsive_secondrow' or @class='col search_price  responsive_secondrow']")

    row_count = len(title_elements)
    print(row_count)
    games = []

    for i in range(row_count):
        temp = []
        category = "on regular price"
        if price_elements[i].get_attribute("class").__contains__('discounted'):
            category = "on sale"
        temp.append(title_elements[i].text)
        temp.append(release_date_elements[i].text)
        temp.append(price_elements[i].text)
        temp.append(category)
        games.append(temp)
        # writer.writerow(temp)
    sorted_data = sorted(games, key=operator.itemgetter(0), reverse=False)
    # print(sorted_data)
    with open('games.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Game Name', 'Release Date', 'Price', 'Price Category'])
        writer.writerows(sorted_data)

