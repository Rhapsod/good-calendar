# coding: utf-8
# author: Ke Mao
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

# for server without a display
from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 600))
display.start()

# for server: replace the file location
data_output_file = 'data.js'
# account here
gc_email = ''
gc_pass = ''

def process_one_month(browser):

	output = open( data_output_file, 'a' )

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
		date = month + '-' + day + '-' + year

		events = []
		for event_div in events_div:
			href = event_div.find_element_by_xpath("a").get_attribute("href")
			title = event_div.find_element_by_xpath("a").text
			events.append( (href, title) )

		# print date, events

		# append data.js
		output.write("'" + date + "': [")

		# write events
		for event in events:
			(href, title) = event
			output.write( ("'<a href=\"" + href + '" target="_blank">' + title + "</a>',\n").encode("utf-8")  )

		output.write("],\n\n");

	output.close()


if __name__ == "__main__":

	# empty data file
	output = open( data_output_file, 'w' )
	output.write("var codropsEvents = {\n")
	output.close()

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
		time.sleep(2)
		browser.get("http://square.goodenough.ac.uk/eventcalendar.aspx")
		process_one_month( browser )

		# calendar-next month
		time.sleep(2)
		next_button = browser.find_element_by_id("monthRight")
		next_button.click()
		process_one_month( browser )

		# logout
		time.sleep(2)
		browser.get("http://square.goodenough.ac.uk/logout.aspx")

		# quit
		time.sleep(2)
		browser.quit()	

	except:
		browser.quit()

	# append end of the file
	output = open( data_output_file, 'a' )
	output.write("};")
	output.close()

	# server only
	display.stop()