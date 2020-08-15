from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
from selenium import webdriver


class classCheck():

    def __init__(self):
        self.baseUrl = "https://learn.illinois.edu/"
        self.driver = webdriver.Firefox()
        self.driver.get(self.baseUrl)
        self.driver.implicitly_wait(1)

    def url_from_file(self, file_name):
        try:
            with open(file_name, 'r' "urtf8") as f:
                content = f.readlines()

                 # you may also want to remove whitespace characters like `\n` at the end of each line
                links = [x.strip() for x in content]

        except FileNotFoundError:
            print("Sorry, the file " + file_name + " does not exist.")

        return links

    def log_on(self, id, password):
        self.driver.find_element_by_id('btnMoodle2').click()

        self.driver.find_element_by_id("username").send_keys(id)
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_id("password").send_keys(password)
        self.driver.find_element_by_id('loginbtn').click()

        time.sleep(2)

    def open_course_url(self, course_url):
        self.driver.get(course_url)
