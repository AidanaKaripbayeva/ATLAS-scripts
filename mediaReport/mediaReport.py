import os #os module imported here
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from prettytable import PrettyTable

baseUrl = 'https://www.reddit.com/r/UIUC/'

option = Options()
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")

# Pass the argument 1 to allow and 2 to block
option.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 1
})

driver = webdriver.Chrome(options=option)

driver.get(baseUrl)
driver.implicitly_wait(1)
keywords = ['online class']

for keyword in keywords:
    driver.find_element_by_id("header-search-bar").send_keys(keyword)
    driver.find_element_by_id("header-search-bar").send_keys(Keys.RETURN)
    driver.find_elements_by_xpath("//p[text()='r/UIUC']")[0].click()
    driver.find_element_by_id("search-results-time").click()
    driver.find_element_by_xpath("//span[text()='Past Week']").click()
    driver.find_element_by_id("search-results-sort").click()
    driver.find_elements_by_xpath("//text()[.='Top']/ancestor::button[1]")[0].click()
    driver.implicitly_wait(3)

    all_spans = driver.find_elements_by_class_name("SQnoC3ObvgnGjWt90zD9Z._2INHSNB8V5eaWp4P0rY_mE")
    print(all_spans)
    hrefList = []
    for span in all_spans:
        hrefList.append(span.get_attribute('href'))

    x = PrettyTable()
    x.field_names = ['Content', 'Link', 'Reaction']
    for href in hrefList:
        driver.get(href)
        messages = driver.find_elements_by_class_name('_1qeIAgB0cPwnLhDF9XSiJM')
        content = []
        for message in messages:
            content.append(message.text)
        x.add_row([content, href, 'none'])
        print(x)
        break


