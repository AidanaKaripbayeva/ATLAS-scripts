from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
from selenium import webdriver


class EndDate():

    def __init__(self):
        self.baseUrl = "https://learn.illinois.edu/"
        self.driver = webdriver.Firefox()
        self.driver.get(self.baseUrl)
        self.driver.implicitly_wait(1)

    def url_from_file(self, file_name):
        try:
            with open(file_name, 'r') as f:
                lines = f.readlines()
                courseURL = []
                for line in lines:
                    courseURL.append(line)

        except FileNotFoundError:
            print("Sorry, the file " + file_name + " does not exist.")

        return courseURL

    def log_on(self, id, password):
        self.driver.find_element_by_id('btnMoodle2').click()

        self.driver.find_element_by_id("username").send_keys(id)
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_id("password").send_keys(password)
        self.driver.find_element_by_id('loginbtn').click()

        time.sleep(2)

    def open_course_url(self, course_url):
        self.driver.get(course_url)

    def edit_settings(self):
        self.driver.find_element_by_id("action-menu-2-menubar").click()  # clicks on the action menu
        self.driver.find_element_by_xpath("//text()[.='Edit settings']/ancestor::a[1]").click()  # selects Edit Settings from the dropdown menu


    def finding_start_date(self):
        day_n = self.driver.find_element_by_name("startdate[day]")
        select = Select(day_n)
        day = select.first_selected_option.text
        month_n = self.driver.find_element_by_name("startdate[month]")
        select1 = Select(month_n)
        month = select1.first_selected_option.text
        year_n = self.driver.find_element_by_name("startdate[year]")
        select2 = Select(year_n)
        year = select2.first_selected_option.text
        return int(day), month, int(year)

    def finding_end_date(self):
        end_date = self.driver.find_element_by_name("enddate[day]")
        select1 = Select(end_date)
        day = select1.first_selected_option.text
        end_month = self.driver.find_element_by_name("enddate[month]")
        select2 = Select(end_month)
        month = select2.first_selected_option.text
        end_year = self.driver.find_element_by_name("enddate[year]")
        select3 = Select(end_year)
        year = select3.first_selected_option.text
        return int(day), month, int(year)

    def setting_end_date(self):
        try:
            self.driver.implicitly_wait(5)
            self.driver.find_element_by_xpath(
                "//text()[contains(.,'Enable')]/ancestor::label[1]").click()  # checks the box of enddate
        except NoSuchElementException:
            pass

        self.driver.find_element_by_xpath("//select[@name='enddate[day]']").send_keys(" 1")
        self.driver.find_element_by_xpath("//select[@name='enddate[month]']").send_keys("August")
        self.driver.find_element_by_xpath("//select[@name='enddate[year]']").send_keys("2019")
        self.driver.find_element_by_xpath("//input[@type='submit'][@name='saveanddisplay']").click()

    def setting_end_date_without_check(self):
        self.driver.find_element_by_xpath("//select[@name='enddate[day]']").send_keys("1")
        self.driver.find_element_by_xpath("//select[@name='enddate[month]']").send_keys("August")
        self.driver.find_element_by_xpath("//select[@name='enddate[year]']").send_keys("2019")
        self.driver.find_element_by_xpath("//input[@type='submit'][@name='saveanddisplay']").click()


