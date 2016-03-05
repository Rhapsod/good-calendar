# coding: utf-8
# author: Ke Mao
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import sqlite3

# for server without a display
# from pyvirtualdisplay import Display
# display = Display(visible=0, size=(800, 600))
# display.start()

##### account here #####
gc_email = ''
gc_pass = ''
########################

# sqlite db
con = sqlite3.connect("data.db")
# auto commit
con.isolation_level = None
cur = con.cursor()
cur.execute( "CREATE TABLE IF NOT EXISTS event (url text primary key, date text, title text, location text, source text)" )

source = 'square'


def process_one_month(browser):

	# get items
	time.sleep(5)
	for item in browser.find_elements_by_class_name("calendar-day-item"):
		divs = item.find_elements_by_xpath("div")
		div_content_type = divs[1].get_attribute("class")
		# pass grey(empty) grids
		if 'calendar-day-item-content content-gray-background' == div_content_type:
			continue

		# pass white grids with zero events
		events_div = divs[1].find_elements_by_xpath("div")
		if len( events_div ) == 0:
			continue

		# process events_div
		date_raw = divs[0].get_attribute("id")
		year = date_raw.split("x")[0].replace("day", "")
		month = date_raw.split("x")[1]
		if len(month) == 1:
			month = '0' + month
		day = date_raw.split("x")[2]
		if len(day) == 1:
			day = '0' + day
		# order for db
		date = year + '-' + month + '-' + day

		events = []
		for event_div in events_div:
			href = event_div.find_element_by_xpath("a").get_attribute("href")
			title = event_div.find_element_by_xpath("a").text
			events.append( (href, title) )

		# print date, events

		# write events
		for event in events:
			(href, title) = event
			cur.execute( "INSERT OR REPLACE INTO event VALUES (?, ?, ?, ?, ?) ", (href, date, title, '', source) )


if __name__ == "__main__":

	browser = webdriver.Firefox() # Get local session of firefox
	try:

		# Login page
		browser.get("http://square.goodenough.ac.uk/default.aspx")
		# browser.get("http://localhost/") # Load page

		# Find input box
		username = browser.find_element_by_id("loginPanel_username") 
		username.send_keys(gc_email)

		# Find input box
		password = browser.find_element_by_id("loginPanel_password") 
		password.send_keys(gc_pass)
		password.send_keys(Keys.RETURN)

		# calendar
		time.sleep(5)
		browser.get("http://square.goodenough.ac.uk/eventcalendar.aspx")
		process_one_month( browser )

		# calendar-next month
		time.sleep(5)
		next_button = browser.find_element_by_id("monthRight")
		next_button.click()
		process_one_month( browser )

		# logout
		time.sleep(5)
		browser.get("http://square.goodenough.ac.uk/logout.aspx")

		# quit
		time.sleep(5)
	except:
		print 'Except.'

	browser.quit()

	# close
	con.close()

	# server only
	# display.stop()