# coding:utf-8
# author: Ke Mao
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time, datetime
import sqlite3

# for server without a display
# from pyvirtualdisplay import Display
# display = Display(visible=0, size=(800, 600))
# display.start()

##### account here #####
fb_email = ''
fb_pass = ''
########################

# sqlite db
con = sqlite3.connect("data.db")
# auto commit
con.isolation_level = None
cur = con.cursor()
cur.execute( "CREATE TABLE IF NOT EXISTS event (url text primary key, date text, title text, location text, source text)" )

source = 'facebook'

if __name__ == "__main__":

	browser = webdriver.Firefox() # Get local session of firefox
	try:

		browser.get("https://www.facebook.com/login.php")

		username = browser.find_element_by_id("email") # Find input box
		username.send_keys(fb_email)

		password = browser.find_element_by_id("pass") # Find input box
		password.send_keys(fb_pass)
		password.send_keys(Keys.RETURN)

		# calendar
		time.sleep(2)
		browser.get("https://www.facebook.com/groups/258997184124380/events/")

		# prepare dates
		# weekday_date = dict()
		# weekday_date['Today'] = datetime.datetime.today().isoformat()[:10]
		# weekday_date['Tomorrow'] = ( datetime.datetime.today() + datetime.timedelta(days=1) ).isoformat()[:10]
		# weekday_ith = datetime.datetime.today().weekday()
		# weekday_strs = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
		# # Monday - 0, Sunday - 6
		# for i in xrange( weekday_ith + 1, 7 ):
		# 	delta = i - weekday_ith
		# 	date = ( datetime.datetime.today() + datetime.timedelta(days=delta) ).isoformat()[:10]
		# 	weekday_date[ weekday_strs[ ( datetime.datetime.today() + datetime.timedelta(days=delta) ).weekday() ] ] = date
		# print weekday_date
		year_int = int( datetime.datetime.today().isoformat()[:4] )
		today = datetime.datetime.today()

		for item in browser.find_elements_by_class_name("fbCalendarList"):
			month = item.get_attribute("id")[-4:-2]
			day = item.get_attribute("id")[-2:]
			this_date = datetime.datetime.strptime( str(year_int) + month + day , "%Y%m%d")
			if this_date.date() < ( datetime.datetime.today() - datetime.timedelta(days=7) ).date():
				this_date = datetime.datetime.strptime( str(year_int + 1) + month + day , "%Y%m%d")

			date_str = this_date.isoformat()[:10]
			
			for elem in item.find_elements_by_class_name("fbCalendarItem"):

				try:
					url = elem.find_elements_by_xpath("table/tbody/tr/td[1]/a")[0].get_attribute("href")
					clock = elem.find_elements_by_xpath("table/tbody/tr/td[1]/a/div")[0].text
					title = elem.find_elements_by_xpath("table/tbody/tr/td[2]/div/div/div/div[2]/div/div[2]/div[1]/a")[0].text

					location = ''
					location_elem = elem.find_elements_by_xpath("table/tbody/tr/td[2]/div/div/div/div[2]/div/div[2]/span/span")
					if len( location_elem ) > 0:
						location = location_elem[0].text
					# print clock, title.encode("utf-8"), url, location
					cur.execute( "INSERT OR REPLACE INTO event VALUES (?, ?, ?, ?, ?) ", (url, date_str, clock + ': ' + title, location, source) )
				except Exception as e:
					print e, "skipped item: ", date_str

	except Exception as e:
		print e
		
	browser.quit()

	con.close()

	# server only
	# display.stop()	