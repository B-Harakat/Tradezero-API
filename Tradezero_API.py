from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import math

from datetime import datetime

from pytz import timezone



class Tradezero_API():


	def __init__(self):
		pass

	def login(self, usr_name, pass_word, url = "https://standard.tradezeroweb.co/"):

		self.usr_name = usr_name
		self.pw = pass_word
		self.url = url

		# This will open up a new firefox window and direct to the url specified i.e. the web platform.
		# Can be changed to Chrome, refer to the selenium module tutorial for how. 
		self.driver = webdriver.Firefox()
		self.driver.get(self.url)


		self.driver.find_element_by_id("login").send_keys(self.usr_name)
		self.driver.find_element_by_name("password").send_keys(self.pw)

		self.driver.find_element_by_xpath("/html/body/form/input[1]").click()

		try:
			element = WebDriverWait(self.driver, 45).until(EC.element_to_be_clickable((By.ID, "short-list-input-symbol")))
		except:
			self.driver.quit()
			print("Connection Timed Out")
		time.sleep(5)

	def get_time(self):

		# Allocating, shorting and covering available 6am to 8pm EST (<--- not ET)

		# eastern = timezone('US/Eastern')
		eastern = timezone('EST')

		loc_dt = datetime.now(eastern)

		split_date_time = str(loc_dt).split(" ")
		split_time = split_date_time[1].split(":")
		split_time.insert(0,datetime.today().weekday())


		time_now = split_time[:3]

		# Returns a list of ['weekday', 'hr', 'minute']
		return time_now


	def set_ticker(self, ticker):

		if type(ticker) != str:
			ticker = str(ticker)

		self.driver.find_element_by_id("trading-order-input-symbol").send_keys(str(ticker), Keys.ENTER)

		# writes as if you are pressing the keyboard itself, feel free to adjust the interval timer (time between key presses)
		# if you feel the execution isn't fast enough
		


	# price is equivalent to 'low' if order type is Range and the limit price for LMTs
	# ^input for the left price bar on the web free platform

	# sprice is equivalent to 'stop price' for Stop-MKT/LMT and 'high' for Range
	# ^input for the right price bar 

	def set_type_and_price(self, order_type, price = 0, sprice = 0):


		price = round(price, 2)
		sprice = round(sprice, 2)

		# I do not recommend using Stop-MKT or Stop-LMT cause they may block other trades from executing on tradezero
		# Besides we can program our own stop-mkt/lmt trade using live data from somewhere else.
		types = ["MKT","LMT","Stop-MKT", "Stop-LMT", "MKT-Close", "LMT-Close", "Range"]

		if order_type in types:

			self.driver.find_element_by_xpath(f"/html/body/div[3]/section[1]/div[1]/div[2]/div/div[5]/span[2]/select/option[{str(types.index(order_type)+1)}]").click()


			if order_type in ["LMT","Stop-LMT","LMT-Close","Range"]:
				if price > 0:
					self.driver.find_element_by_id("trading-order-input-price").send_keys(str(price))
				else:
					print(f"positive value for price (low) required for order type {order_type}")


			if order_type in ["Stop-MKT", "Stop-LMT","Range"]:
				if sprice > 0:
					self.driver.find_element_by_id("trading-order-input-sprice").send_keys(str(sprice))
				else:
					print(f"positive value for stop price (high) required for order type {order_type}")

		else:
			print(f"Wrong input for order_type, accepted inputs are {types}")




	def set_quantity(self, quantity):

		self.driver.find_element_by_id("trading-order-input-quantity").send_keys(str(quantity))




	def set_action(self, action):

		actions = ["buy", "sell", "short", "cover"]

		try:
			if action.lower() in actions:

				self.driver.find_element_by_id(f"trading-order-button-{action.lower()}").click()

			else:
				print(f"action type incorrect, allowed actions are {actions} \n")

		except:
			print(f"something went wrong, short shares weren't allocated")

	def set_tif(self, time_in_force):

		types = ["DAY", "GTC", "GTX"]
		
		self.driver.find_element_by_xpath(f"/html/body/div[3]/section[1]/div[1]/div[2]/div/div[8]/span[2]/select/option[{str(types.index(time_in_force.upper())+1)}]").click()



###### SHORT & COVER #######


	def get_short_status(self, ticker):
		
		status = self.driver.find_element_by_id("trading-order-locate-status").text
		
		return status
		


	# Main function for locating shorts
	def locate_short(self, ticker, quantity = 100):
			
		try:
			time.sleep(0.5)

			self.driver.find_element_by_id("short-list-input-symbol").send_keys(ticker,Keys.ENTER)
			time.sleep(0.5)

			if quantity % 100 == 0:

				self.driver.find_element_by_id("short-list-input-shares").send_keys(str(quantity),Keys.ENTER)
			else:
				print("quantity needs to be in steps of 100")

			time.sleep(0.5)
			
			try:
				WebDriverWait(self.driver, 1.5).until(EC.element_to_be_clickable((By.CLASS_NAME, "button-box.button-box-small.button-blue-filled")))
				
			except:
				pass

			print("waiting")
			time.sleep(1.5)
			
			self.driver.find_element_by_id("short-list-button-locate").click()
			time.sleep(0.1)

			try:
				WebDriverWait(self.driver, 4).until(EC.presence_of_element_located((By.CLASS_NAME, "icon-box.icon-box-accept")))
				time.sleep(0.1)
			except:
				print("cant find green")

			self.driver.find_element_by_class_name("icon-box.icon-box-accept").click()
		except:
			print(f"Couldn't locate short of {ticker}")



	def cancel_locate(self):
		try:
			WebDriverWait(self.driver, 2.5).until(EC.element_to_be_clickable((By.ID, "short-locate-button-cancel")))
			time.sleep(0.5)
			self.driver.find_element_by_id("short-locate-button-cancel").click()
			print("Cancelled locate")
		except:
			pass


	def reset_short_locate_info(self):
		try:
			self.driver.find_element_by_id("short-list-input-symbol").clear()
		except:
			pass

		try:
			self.driver.find_element_by_id("short-list-input-shares").clear()
		except:
			pass



######### GENERAL METHODS  ##########


	def submit_order(self,ticker, quantity, order_type, price=0, sprice=0, time_in_force="DAY", action=None , auto_locate = False):
		
		# Check if it is the weekends
		if self.get_time()[0] == 5 or self.get_time()[0] == 6:
			pass

		else:
			self.set_ticker(ticker)
			time.sleep(2)
			self.set_quantity(quantity)
			time.sleep(0.25)
			self.set_type_and_price(order_type, price, sprice)
			time.sleep(0.25)
			self.set_tif(time_in_force)
			time.sleep(0.25)

			if auto_locate == True:

				if action.lower() == "short" and int(self.get_time()[1])>=6 and int(self.get_time()[1])<=20:

					# Incase the ticker is hard-to-borrow and we need to locate shorts
					if "S" not in self.get_short_status(ticker):

						# round quantity to the nearest hundreds
						short_quantity = int(math.ceil(float(quantity/100))) * 100
						
						# locate it and reset the input field
						self.locate_short(ticker, short_quantity)
						time.sleep(0.25)
						self.reset_short_locate_info()
						time.sleep(0.25)

						self.set_action(action)
						time.sleep(0.25)

					# Incase the ticker is hard-to-borrow and we already located some shorts
					elif "/" in self.get_short_status(ticker):

						# Check if quantity is more than available short locates, if not, locate more
						available_shorts = self.get_short_status(ticker).strip("S( )")
						available_shorts = available_shorts.split("/")
						available_shorts = int(available_shorts[0])

						if available_shorts >= quantity:
							self.set_action(action)
							time.sleep(0.25)

						elif available_shorts < quantity:
							
							short_quantity = int(math.ceil(float((quantity-available_shorts)/100))) * 100
							self.locate_short(ticker, short_quantity)
							time.sleep(0.25)
							self.reset_short_locate_info()
							time.sleep(0.25)

							self.set_action(action)
							time.sleep(0.25)
							

					# Incase the ticker is easy-to-borrow
					elif "S" in self.get_short_status(ticker):
						self.set_action(action)
						time.sleep(0.25)


				elif action.lower() in ["short", "cover"]:
					print(f"Shorting and Covering only allowed between 6am and 8pm EST, current time = {self.get_time()[1:]}\n")

				else:
					self.set_action(action)
					time.sleep(0.25)


			else:
				self.set_action(action)
				time.sleep(0.25)

				# To close the pop-up window that appears when you try to short without enough allocates
				# Will do nothing if there is no pop-up window i.e. we have enough shorts allocated
				if action.lower() == "short":

					self.cancel_locate()
					time.sleep(0.25)


			



	def reset(self):
		self.driver.find_element_by_id("trading-order-input-quantity").clear()

		# Incase the price fields on tradezero is unavailable, e.g. when the order type is MKT
		try:
			self.driver.find_element_by_id("trading-order-input-price").clear()
		except:
			pass

		try:
			self.driver.find_element_by_id("trading-order-input-sprice").clear()
		except:
			pass

		self.driver.find_element_by_xpath(f"/html/body/div[3]/section[1]/div[1]/div[2]/div/div[8]/span[2]/select/option[1]").click()

	

	


