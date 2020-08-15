import os #os module imported here
import EndDate
from selenium.common.exceptions import NoSuchElementException
import sys

if len(sys.argv) != 3:
    print("Something is wrong.")
    sys.exit(0)


file_to_save_result = sys.argv[1]
file_no_access = sys.argv[2]
result_to_file = []
no_access = []



location = os.getcwd() # get present working directory location here
counter = 0 #keep a count of all files found
csvfiles = [] #list to store all csv files found at location
otherfiles = [] #list to keep any other file that do not match the criteria


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


username = ''
password = ''

setDate = EndDate.EndDate()

setDate.log_on(username, password)


for file in os.listdir(location):
    try:
        if file.endswith(".csv"):
            print("csv file found: ", file)
            csvfiles.append(str(file))
            counter = counter+1
            courseURL = setDate.url_from_file(file)
            result_to_file.append("\n" + "\n" + file + "\t" + "is found" )

            for i in range(len(courseURL)):
                # open course URL:
                setDate.open_course_url(courseURL[i])
                print("working on " + courseURL[i])
                result_to_file.append("\n" + "Working on " + courseURL[i])

                # access Edit settings button

                try:
                    inputElement = setDate.driver.find_element_by_id("action-menu-2-menubar") # clicks on the action menu
                    setDate.driver.execute_script("arguments[0].click();", inputElement)
                    Element2 = setDate.driver.find_element_by_xpath("//text()[.='Edit settings']/ancestor::a[1]") # selects Edit Settings from the dropdown menu
                    setDate.driver.execute_script("arguments[0].click();", Element2)
                    start_day, start_month, start_year = setDate.finding_start_date()

                    if start_year < 2019:
                        # if checkbox is not enabled
                        if setDate.driver.find_element_by_id("id_enddate_enabled").is_selected() == False:
                            setDate.setting_end_date()
                            print("The course didn't have an end date. The end date is enabled and changed to August, 2019")
                            result_to_file.append("Course's start date is " + str(start_month) + ", " + str(start_year) + " and checkbox wasn't enabled. Thus, the end date was changed successfully. ")

                        # if checkbox is already enabled, checks dates
                        else:
                            end_day, end_month, end_year = setDate.finding_end_date()

                            # if end month is incorrect
                            if end_year == 2019 & int(month_from_str(end_month)) > 8:
                                setDate.setting_end_date_without_check()
                                print("The end month was incorrect and it was successfully changed to August, 2019.")
                                result_to_file.append("Course's start date is " + str(start_month) + "," + str(start_year) + "  and end date was " + str(end_month) + ", "
                                        + str(end_year) + " which is incorrect. So, the end date was changed successfully.")


                            # if end year is incorrect
                            elif end_year > 2019:
                                setDate.setting_end_date_without_check()
                                print("The end year was set incorrectly. The end date was successfully changed to August, 2019.")
                                result_to_file.append(
                                    "Course's start date is " + str(start_month) + "," + str(start_year) + " and end date was " + str(end_month) + ", "
                                    + str(end_year) + " which is incorrect. So, the end date was changed successfully.")
                            else:
                                print("The end date was correct. Nothing is changed.")
                                result_to_file.append(
                                    "Course's start date is " + str(start_month) + "," + str(start_year) + " and end date is " + str(end_month) + ", "
                                    + str(end_year) + " which is correct. So, nothing is changed.")

                    elif start_year == 2019:
                        if int(month_from_str(start_month)) < 8:
                            # if checkbox is not enabled
                            if setDate.driver.find_element_by_id("id_enddate_enabled").is_selected() == False:
                                setDate.setting_end_date()
                                print("The course(2019) didn't have an end date. So, it was set to August, 2019")
                                result_to_file.append(
                                    "Course's start date is " + str(start_month) + ", " + str(start_year) + ", and the checkbox was not enabled. So, the end date was set up successfully.")

                            # if checkbox is enabled, checks if the end date is correctly set
                            else:
                                end_day, end_month, end_year = setDate.finding_end_date()
                                # if end month is set incorrectly. After August 2019.
                                if int(month_from_str(end_month)) > 8 & end_year == 2019 :
                                    setDate.setting_end_date_without_check()
                                    print(
                                        "The end date of the course(2019) was incorrect. So, it was changed to August, 2019")
                                    result_to_file.append(
                                        "Course's start date is " + str(start_month) + ", " + str(start_year) + ", and end date was " + str(end_month) + ", "
                                        + str(end_year) + " which is incorrect. So, the end date was changed successfully. ")
                                elif end_year > 2019:
                                    setDate.setting_end_date_without_check()
                                    print(
                                        "The end year was set incorrectly. The end date was successfully changed to August, 2019.")
                                    result_to_file.append(
                                        "Course's start date is " + str(start_month) + "," + str(
                                            start_year) + " and end date was " + str(end_month) + ", "
                                        + str(
                                            end_year) + " which is incorrect. So, the end date was changed successfully.")


                                else:
                                    print("The end date was correct. Nothing is changed")
                                    result_to_file.append(
                                        "Course's start date is " + str(start_month) + ", " + str(start_year) + "  and end date was " + str(end_month) + ", "
                                        + str(end_year) + ". So everything is correct and nothing is changed")
                        # if it is Fall 2019
                        else:
                            print("The course is still running")
                            result_to_file.append(
                                "Course's start date is " + str(start_month) + ", " + str(start_year) + ",  and end date was " + str(end_month) + ", "
                                + str(end_year) + " So the course is till running. ")

                    # End date is correct
                    else:
                        print("The end date is fine")
                        result_to_file.append(
                            "Course's start date is " + str(start_month) + ", " + str(start_year) + " and end date was " + str(end_month) + ", "
                            + str(end_year) + ". Everything is good. ")

                    with open(file_to_save_result, 'a') as f_obj:
                        for line in result_to_file:
                            f_obj.write("%s\n" % line)

                    result_to_file = []

                    if len(no_access) != 0:
                        with open(file_no_access, 'a') as f_obj:
                            for line in no_access:
                                f_obj.write("%s\n" % line)

                        no_access = []







                except NoSuchElementException:
                    print("No access to this course")
                    result_to_file.append("Can't access this course")
                    no_access.append(str(courseURL[i]))
                    pass

        else:
            otherfiles.append(file)



    except Exception as e:
        raise e
        print("No files found here!")
        result_to_file.append("No files found here")




# close file
setDate.driver.close()

print("Total files found: ", counter)