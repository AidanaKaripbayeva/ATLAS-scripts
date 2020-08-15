import os #os module imported here
import classCheck
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

import sys

if len(sys.argv) != 4:
    print(
        "Arguments:\n1 - courses link file name\n2 - config file name\n3 - log file name to write results\n")
    print("This program will not run without all arguments provided.\n")
    print(
        "1) Courses File Name - this is a text file containing the course link.")
    print("\n2) Config File Name - this is a text file containing the start and end dates.")
    print("\tThe first line should say 'start MONTH DATE YEAR'. Year should be four digits.")
    print("\t\tExample: 'start March 28 2018'.")
    print(
        "\tThe second line is the same, but with the first word 'end'.\n\tTime is not specified -- the survey will open at midnight the morning of the start date and close \n\tat the end of the day on the end date.")
    print("\n\tA properly formatted config file would look like this:")
    print("\t\tstart March 28 2018")
    print("\t\tend May 30 2018")
    print(
        "\n3) Log File Name - a new file will be created and log entries will be written to it.\n\tIf an existing file is provided, results will be appended to the end.")
    print(
        "\nExample final call: \n\n\tpython allCheck.py courseLinks.txt ConfigFile.txt LogFile.txt")
    sys.exit(0)



file_links = sys.argv[1]
file_config = sys.argv[2]
file_to_save_result = sys.argv[3]
result_to_file = []


def month_from_str(x):
    if x == "January":
        return 1
    if x == "February":
        return 2
    if x == "March":
        return 3
    if x == "April":
        return 4
    if x == "May":
        return 5
    if x == "June":
        return 6
    if x == "July":
        return 7
    if x == "August":
        return 8
    if x == "September":
        return 9
    if x == "October":
        return 10
    if x == "November":
        return 11
    if x == "December":
        return 12
    #error_exit("The month " + x + " is not a valid month, please check your config file!")

#username and password
username = ''
password = ''


# open and parse config file. The config file should be formatted as follows:
# start October 21 2019
# end December 22 2019
config = open(file_config)
start_line = config.readline()
end_line = config.readline()
print("start: ", start_line)
print("end: ", end_line)

# start and end should each have month as [1], date as [2], and year as [3]
start = start_line.split(" ")
start_day = start[2]
start_month = start[1]
start_year = start[3]
print(start_day, start_month, start_year)
end = end_line.split(" ")
end_month = end[1]
end_day = end[2]
end_year = end[3]


check = classCheck.classCheck()

courseURL = check.url_from_file(file_links)

print("number of courses = ", len(courseURL))
check.log_on(username, password)



for i in range(len(courseURL)):
    # open course URL:
    check.open_course_url(courseURL[i])
    print("working on ", courseURL[i])
    result_to_file.append("\n\n" + "Working on " + courseURL[i] + "\n")

    page_id_location = check.driver.find_element_by_xpath("//html[1]/body[1]")
    page_id = page_id_location.get_attribute('id')
    side_button = check.driver.find_element_by_id(page_id).find_element_by_id("page-wrapper").find_element_by_class_name("fixed-top.navbar.navbar-light.bg-white.navbar-expand.moodle-has-zindex").find_element_by_class_name("d-inline-block.mr-3").find_element_by_class_name("btn.nav-link.float-sm-left.mr-1.btn-light.bg-gray")
    yes = side_button.get_attribute("aria-expanded")
    if yes=='false':
        side_button.click()

    # clicks on Tools and Report

    if check.driver.find_elements_by_class_name("list-group-item.list-group-item-action.toggler"):
        print("found a css name")
        elems = check.driver.find_elements_by_class_name("list-group-item.list-group-item-action.toggler")
        for e in elems:
            e.click()

    # clicks on date reports
    check.driver.find_element_by_link_text("Dates Report").click()

    collapse = check.driver.find_elements_by_class_name("collapseexpand")
    for c in collapse:
        c.click()

    all_spans = check.driver.find_elements_by_class_name("custom-select")
    for span in all_spans:
        id = span.get_attribute('name')
        #assigns a daya
        if "day" in id:
            select = Select(span)
            found_day = select.first_selected_option.text
        # assigns month and check its correctness with the day
        if "month" in id:
            select = Select(span)
            found_month = select.first_selected_option.text
            # if the month is correct but date is not
            if int(month_from_str(found_month)) >= int(month_from_str(start_month)) and int(month_from_str(found_month)) <= int(month_from_str(end_month)):
                if int(month_from_str(found_month)) == int(month_from_str(start_month)):
                    if int(found_day) < int(start_day):
                        print("invalid day: " + found_month + "\t" + found_day + " . Start date of the Activity is earlier than start date of the course")
                        result_to_file.append(
                            "invalid day: " + found_month + "\t" + found_day + " . Start date of the Activity is earlier than start date of the course")
                if int(month_from_str(found_month)) == int(month_from_str(end_month)):
                    if int(found_day) > int(end_day):
                        print(
                            "invalid day: " + found_month + "\t" + found_day + " . End date of the Activity is later than the end date of the course")
                        result_to_file.append("invalid day: " + found_month + "\t" + found_day + " . End date of the Activity is later than the end date of the course")
            # if month is incorrect
            else:
                print(
                    "invalid month: " + found_month + ". It should be between " + start_month + "\t and \t" +
                        end_month)
                result_to_file.append("invalid month: " + found_month + ". It should be between " + start_month + "\t and \t" +
                        end_month)
        #assigns year
        if "year" in id:
            select = Select(span)
            found_year = select.first_selected_option.text
            # if year is incorrect
            if int(found_year) != int(start_year):
                print("invalid year: " + str(found_year) + ". It should be " + start_year)
                result_to_file.append("invalid year: " + str(found_year) + ". It should be " + start_year)


    with open(file_to_save_result, 'a') as f_obj:
        for line in result_to_file:
            f_obj.write("%s\n" % line)

    result_to_file = []


check.driver.close()



