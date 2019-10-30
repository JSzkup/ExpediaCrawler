# Browser automation through webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Structure the data
import pandas as pd

# Lets me use .sleep() so my script doesnt work faster than the page can update
import time
import datetime

# Emailing the results
import smtplib
from email.mime.multipart import MIMEMultipart

# Executeable path to Chrome WEBDRIVER, not chrome executable
browser = webdriver.Chrome(
    executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')

# ticket types paths
return_ticket = "//label[@id='flight-type-roundtrip-label-hp-flight']"
one_way_ticket = "//label[@id='flight-type-one-way-label-hp-flight']"
multi_ticket = "//label[@id='flight-type-multi-dest-label-hp-flight']"

# Panda dataframe to hold data
df = pd.DataFrame()


def ticket_chooser(ticket):  # Looks for the defined ticket types
    try:
        ticket_type = browser.find_element_by_xpath(ticket)
        ticket_type.click()
    except Exception as i:
        pass


# Chooses the country we are DEPARTING from
def dep_country_chooser(dep_country):
    # Origin Box on website
    fly_from = browser.find_element_by_xpath(
        "//input[@id='flight-origin-hp-flight']")
    time.sleep(1)
    # Clearing the Origin input box
    fly_from.clear()
    time.sleep(1.5)
    fly_from.send_keys('  ' + dep_country)
    time.sleep(1.5)
    # Chooses first option in  Origin Box
    first_item = browser.find_element_by_xpath("//a[@id='aria-option-0']")
    time.sleep(1.5)
    first_item.click()


# Chooses the country we are ARRIVING at
def arrival_country_chooser(arrival_country):
    # Destination Box on website
    fly_to = browser.find_element_by_xpath(
        "//input[@id='flight-destination-hp-flight']")
    time.sleep(1)
    # Clearing input
    fly_to.clear()
    time.sleep(1.5)
    fly_to.send_keys('  ' + arrival_country)
    time.sleep(1.5)
    first_item = browser.find_element_by_xpath("//a[@id='aria-option-0']")
    time.sleep(1.5)
    first_item.click()


def dep_date_chooser(month, day, year):  # Choose DEPARTURE date
    dep_date_button = browser.find_element_by_xpath(
        "//input[@id='flight-departing-hp-flight']")
    dep_date_button.clear()
    dep_date_button.send_keys(month + '/' + day + '/' + year)


def return_date_chooser(month, day, year):  # Choose ARRIVAL date
    return_date_button = browser.find_element_by_xpath(
        "//input[@id='flight-returning-hp-flight']")
    # Browser autofills date of max 11 characters, and .clear() wont work
    for i in range(11):
        return_date_button.send_keys(Keys.BACKSPACE)
    return_date_button.send_keys(month + '/' + day + '/' + year)


def search():  # Clicks the search button
    search = browser.find_element_by_xpath(
        "//button[@class='btn-primary btn-action gcw-submit']")
    search.click()
    # Long delay, search loads slowly
    time.sleep(15)
    # tells user when things are searched properly
    print('Results ready!')


def compile_data():
    # variables to store search results
    global df
    global dep_times_list
    global arr_times_list
    global airlines_list
    global price_list
    global durations_list
    global stops_list
    global layovers_list

    # departure times
    dep_times = browser.find_elements_by_xpath(
        "//span[@data-test-id='departure-time']")
    dep_times_list = [value.text for value in dep_times]

    # arrival times
    arr_times = browser.find_elements_by_xpath(
        "//span[@data-test-id='arrival-time']")
    arr_times_list = [value.text for value in arr_times]

    # airline name
    airlines = browser.find_elements_by_xpath(
        "//span[@data-test-id='airline-name']")
    airlines_list = [value.text for value in airlines]

    # prices
    prices = browser.find_elements_by_xpath(
        "//span[@data-test-id='listing-price-dollars']")
    # TODO check here for errors
    price_list = [value.text.split('')[1] for value in prices]

    # durations
    durations = browser.find_elements_by_xpath(
        "//span[@data-test-id='duration']")
    durations_list = [value.text for value in durations]

    # stops
    stops = browser.find_elements_by_xpath("//span[@class='number-stops']")
    stops_list = [value.text for value in stops]

    # layovers
    layovers = browser.find_elements_by_xpath(
        "//span[@data-test-id='layover-airport-stops']")
    layovers_list = [value.text for value in layovers]
    # renaming price for every iteration
    now = datetime.datetime.now()
    current_date = (str(now.year) + '-' + str(now.month) + '-' + str(now.day))
    current_time = (str(now.hour) + ':' + str(now.minute))
    current_price = 'price' + '(' + current_date + '---' + current_time + ')'

    # Creates a list of data for each variable
    for i in range(len(dep_times_list)):
        try:
            df.loc[i, 'departure_time'] = dep_times_list[i]
        except Exception as i:
            pass
        try:
            df.loc[i, 'arrival_time'] = arr_times_list[i]
        except Exception as i:
            pass
        try:
            df.loc[i, 'airline'] = airlines_list[i]
        except Exception as i:
            pass
        try:
            df.loc[i, 'duration'] = durations_list[i]
        except Exception as i:
            pass
        try:
            df.loc[i, 'stops'] = stops_list[i]
        except Exception as i:
            pass
        try:
            df.loc[i, 'layovers'] = layovers_list[i]
        except Exception as i:
            pass
        try:
            df.loc[i, str(current_price)] = price_list[i]
        except Exception as i:
            pass
    print('Excel Sheet Created!')
