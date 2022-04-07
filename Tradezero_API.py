from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import math

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



	def get_short_status(self, ticker):
		
		status = self.driver.find_element_by_id("trading-order-locate-status").text
		print(f"short status of {ticker} is : {status} \n")
		return status
		



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
				WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "icon-box.icon-box-accept")))
				time.sleep(0.1)
			except:
				print("cant find green")

			self.driver.find_element_by_class_name("icon-box.icon-box-cancel").click()
		except:
			print(f"Couldn't locate short of {ticker}")

	def reset_short_locate_info(self):
		self.driver.find_element_by_id("short-list-input-symbol").clear()
		self.driver.find_element_by_id("short-list-input-shares").clear()





	def submit_order(self,ticker, quantity, order_type, price=0, sprice=0, time_in_force="DAY", action=None):

		self.set_ticker(ticker)
		time.sleep(2)
		self.set_quantity(quantity)
		time.sleep(0.25)
		self.set_type_and_price(order_type, price, sprice)
		time.sleep(0.01)
		self.set_tif(time_in_force)
		time.sleep(0.01)

		if action.lower() == "short":
			if self.get_short_status(ticker) != "S":
				short_quantity = int(math.ceil(float(quantity/100))) * 100

				self.locate_short(ticker, short_quantity)
				time.sleep(0.2)
				self.reset_short_locate_info()

		time.sleep(0.25)
		self.set_action(action)
		time.sleep(0.5)



	def reset(self):
		self.driver.find_element_by_id("trading-order-input-quantity").clear()

		try:
			self.driver.find_element_by_id("trading-order-input-price").clear()
		except:
			pass

		try:
			self.driver.find_element_by_id("trading-order-input-sprice").clear()
		except:
			pass

		self.driver.find_element_by_xpath(f"/html/body/div[3]/section[1]/div[1]/div[2]/div/div[8]/span[2]/select/option[1]").click()

	

	


