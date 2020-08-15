from selenium.webdriver.chrome.options import Options
import EndDate

import sys

if len(sys.argv) != 3:
    print("Something is wrong.")
    print(" Is it a link to a course?")
    sys.exit(0)

options = Options()
options.add_argument("--disable-notifications")

file_URL = sys.argv[1]
file_to_save_result = sys.argv[2]
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




username = 'su-moodle-aidana2'
password = 'KmA.10kma'

setDate = EndDate.EndDate()

setDate.log_on(username, password)

courseURL = setDate.url_from_file(file_URL)


for i in range(len(courseURL)):
    #open course URL:
    setDate.open_course_url(courseURL[i])
    print("working on " + courseURL[i])
    #access Edid settings button
    setDate.edit_settings()
    # finds start dates
    start_day, start_month, start_year = setDate.finding_start_date()

    if start_year < 2019:
        # if checkbox is not enabled
        if setDate.driver.find_element_by_id("id_enddate_enabled").is_selected() == False:
            setDate.setting_end_date()
            print("The course didn't have an end data. The end date is enabled and changed to August, 2019")

        # if checkbox is already enabled, checks dates
        else:
            end_day, end_month, end_year = setDate.finding_end_date()

            # if end month is incorrect
            if end_year == 2019 & int(month_from_str(end_month)) > 8:
                setDate.setting_end_date_without_check()
                print("The end month was incorrect and it was successfully changed to August, 2019.\n")

            # if end year is incorrect
            elif end_year > 2019:
                setDate.setting_end_date_without_check()
                print("The end year was set incorrectly. The end date was successfully changed to August, 2019.\n")

            else:
                print("The end date was correct. Nothing is changed.\n")

    elif start_year == 2019:
        if int(month_from_str(start_month)) < 8:
            #if checkbox is not enabled
            if setDate.driver.find_element_by_id("id_enddate_enabled").is_selected() == False:
                setDate.setting_end_date()
                print("The course(2019) didn't have an end date. So, it was set to August, 2019")

            #if checkbox is enabled, checks if the end date is correctly set
            else:
                end_day, end_month, end_year = setDate.finding_end_date()
                #if end month is set incorrectly. After August 2019.
                if int(month_from_str(end_month)) > 8:
                    setDate.setting_end_date_without_check()
                    print("The end date of the course(2019) was incorrect. So, it was changed to August, 2019")

                else:
                    print("The end date was correct. Nothing is changed")
        #if it is Fall 2019
        else:
            print("The course is still running")

    #End date is correct
    else:
        print("The end date is fine")
        pass

#close file
setDate.driver.close()





