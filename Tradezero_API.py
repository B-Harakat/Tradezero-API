from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

import time
import math

from datetime import datetime
from pytz import timezone
import pandas as pd



class Tradezero_API():


	def __init__(self,headless=False):
		if headless == True:
			options = Options()
			options.headless = True
			self.driver = webdriver.Firefox(options=options)

		else:
			self.driver = webdriver.Firefox()


		
	def login(self, usr_name=None, pass_word=None, url = "https://standard.tradezeroweb.co/"):

		self.usr_name = usr_name
		self.pw = pass_word
		self.url = url
		self.driver.get(self.url)

		self.driver.find_element_by_id("login").send_keys(self.usr_name)
		self.driver.find_element_by_name("password").send_keys(self.pw)

		self.driver.find_element_by_xpath("/html/body/form/input[1]").click()

		try:
			element = WebDriverWait(self.driver, 45).until(EC.element_to_be_clickable((By.ID, "short-list-input-symbol")))
		except:
			self.driver.quit()
			print("Error. Connection Timed Out.")
		time.sleep(5)

	def get_time(self):

		# Allocating, shorting and covering available 6am to 8pm EST (<--- not ET)

		tz = timezone('US/Eastern')
		now = datetime.now(tz)
		weekday = now.weekday()
		hour    = int(now.strftime("%H"))
		minute  = int(now.strftime("%M"))

		time_now = [weekday, hour, minute]
		return time_now

	def get_bid(self,ticker=None):
		if ticker != None:
			self.set_ticker(ticker)

		for i in range(1000):
			try:
				bid  = self.driver.find_element_by_id("trading-order-bid").text
				bid = float(bid)
				break
			except:
				time.sleep(0.1)
		return(float(bid))

	def get_ask(self,ticker=None):
		if ticker != None:
			self.set_ticker(ticker)

		for i in range(100):
			try:
				ask = self.driver.find_element_by_id("trading-order-ask").text
				ask = float(ask)
				break
			except:
				time.sleep(0.1)
		return(float(ask))

	def get_notification(self):
		notice  = self.driver.find_element_by_id("notifications-list-1").text
		return notice

	def get_funds(self):
		money    = self.driver.find_element_by_id("h-equity-value").text
		exposure = self.driver.find_element_by_id("h-exposure-value").text

		money = money.replace(",","")
		money = money.replace("$","")
		money = float(money)

		exposure = exposure.replace(",","")
		exposure = exposure.replace("$","")
		exposure = float(exposure)

		available_funds = money-exposure

		return available_funds




### Auxillary ###

	def set_ticker(self, ticker):

		if type(ticker) != str:
			ticker = str(ticker)
		self.driver.find_element_by_id("trading-order-input-symbol").send_keys(str(ticker), Keys.ENTER)
		time.sleep(0.75)
			


	def set_type_and_price(self, order_type, price = 0, sprice = 0, action=None, offset=0):


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
					print(f"Error. Negative price input.")


			if order_type in ["Stop-MKT", "Stop-LMT","Range"]:
				if sprice > 0:
					self.driver.find_element_by_id("trading-order-input-sprice").send_keys(str(sprice))
				else:
					print(f"Error. Negative price input.")


		elif order_type == "NM-LMT":
			self.driver.find_element_by_xpath(f"/html/body/div[3]/section[1]/div[1]/div[2]/div/div[5]/span[2]/select/option[2]").click()

			if action.lower() in ["sell", "short"]: 
				price = self.get_bid()+offset
				if price > 0:
					self.driver.find_element_by_id("trading-order-input-price").send_keys(str(price))
				else:
					print(f"Error. Negative price input.")

			elif action.lower() in ["buy", "cover"]: 
				price = self.get_ask()+offset
				if price > 0:
					self.driver.find_element_by_id("trading-order-input-price").send_keys(str(price))
				else:
					print(f"Error. Negative price input.")



		else:
			print(f"Error. Wrong input for order_type, accepted inputs are {types}")




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
			print(f"Error. Short shares weren't allocated")

	def set_tif(self, time_in_force):

		types = ["DAY", "GTC", "GTX"]
		
		self.driver.find_element_by_xpath(f"/html/body/div[3]/section[1]/div[1]/div[2]/div/div[8]/span[2]/select/option[{str(types.index(time_in_force.upper())+1)}]").click()



###### SHORT & COVER #######


	def get_short_status(self, ticker):
		
		status = self.driver.find_element_by_id("trading-order-locate-status").text	

		if "S" not in status:
			return("HTB")

		elif "/" in status:

			# Check if quantity is more than available short locates, if not, locate more
			available_shorts = status.strip("S( )")
			available_shorts = available_shorts.split("/")
			available_shorts = int(available_shorts[0])

			return(available_shorts)

		elif "S" in status:
			return("ETB")

		else:
			print(f"Error. Unknown short status: {status}")


	def get_locate_fee(self,ticker,quantity):
		try:
			time.sleep(0.5)
			self.driver.find_element_by_id("short-list-input-symbol").send_keys(ticker,Keys.ENTER)
			time.sleep(0.5)

			if quantity % 100 == 0:
				self.driver.find_element_by_id("short-list-input-shares").send_keys(str(quantity),Keys.ENTER)
			else:
				print("quantity needs to be in steps of 100")
			time.sleep(0.5)
			
			WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "button-box.button-box-small.button-blue-filled")))
			time.sleep(1.5)

			self.driver.find_element_by_id("short-list-button-locate").click()
			time.sleep(0.1)

			WebDriverWait(self.driver, 6).until(EC.presence_of_element_located((By.CLASS_NAME, "icon-box.icon-box-accept")))
			time.sleep(0.1)

			fee = self.driver.find_element_by_id(f"oitem-l-{ticker}-cell-6").text
			self.driver.find_element_by_class_name("icon-box.icon-box-cancel").click()

			return float(fee)
		
		except:
			print(f"Error. Couldn't locate short of {ticker}")
			return None	





	# Main function for locating shorts
	def locate_short(self, ticker, quantity=100, fee_limit=1E+6):
		
		self.locate_success = False

		try:
			time.sleep(0.1)

			self.driver.find_element_by_id("short-list-input-symbol").send_keys(ticker,Keys.ENTER)
			time.sleep(0.1)

			if quantity % 100 == 0:

				self.driver.find_element_by_id("short-list-input-shares").send_keys(str(quantity),Keys.ENTER)
			else:
				print("Error. qty needs to be in steps of 100.")

			time.sleep(0.1)
			
			WebDriverWait(self.driver, 1.5).until(EC.element_to_be_clickable((By.CLASS_NAME, "button-box.button-box-small.button-blue-filled")))
			time.sleep(0.1)
			
			self.driver.find_element_by_id("short-list-button-locate").click()
			time.sleep(0.1)

			
			WebDriverWait(self.driver, 4).until(EC.presence_of_element_located((By.CLASS_NAME, "icon-box.icon-box-accept")))
			time.sleep(0.1)

			fee = float(self.driver.find_element_by_id(f"oitem-l-{ticker}-cell-6").text)

			if fee < fee_limit:
				self.driver.find_element_by_class_name("icon-box.icon-box-accept").click()
				self.locate_success = True

			else:
				self.driver.find_element_by_class_name("icon-box.icon-box-cancel").click()
				self.locate_success = False

		except:
			print(f"Error. Couldn't locate short of {ticker}.")
			self.locate_success = False


	def cancel_locate(self):
		try:
			WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.ID, "short-locate-button-cancel")))
			time.sleep(0.1)
			self.driver.find_element_by_id("short-locate-button-cancel").click()
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

	# Cleans the input fields
	def reset(self):

		self.driver.find_element_by_id("trading-order-input-quantity").clear()
		time.sleep(0.1)
		try:
			self.driver.find_element_by_id("trading-order-input-price").clear()
			time.sleep(0.1)
		except:
			pass

		try:
			self.driver.find_element_by_id("trading-order-input-sprice").clear()
			time.sleep(0.1)
		except:
			pass

		self.driver.find_element_by_xpath(f"/html/body/div[3]/section[1]/div[1]/div[2]/div/div[8]/span[2]/select/option[1]").click()


	def cancel_all_orders(self):
		self.driver.find_element_by_id("portfolio-tab-ao-1").click()
		time.sleep(2)
		try:
			for i in range(200):
				try:
					WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,\
						"/html/body/div[3]/section[1]/div[3]/div[2]/div[5]/div[2]/div[2]/div[3]/div/div[1]/div/table/tbody/tr/td")))

					self.driver.find_element_by_xpath(\
						"/html/body/div[3]/section[1]/div[3]/div[2]/div[5]/div[2]/div[2]/div[3]/div/div[1]/div/table/tbody/tr/td"\
							).click()

					if EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/section[1]/div[3]/div[2]/div[5]/div[2]/div[2]/div[3]/div/div[1]/div/table/tbody/tr/td")):
						text = self.driver.find_element_by_xpath("/html/body/div[3]/section[1]/div[3]/div[2]/div[5]/div[2]/div[2]/div[3]/div/div[1]/div/table/tbody/tr/td").text
						print(text)
						if "no" in text:
							break
					time.sleep(1)
				
				except:
					pass		
		except:
			print("All order cancelled")




	def get_positions(self,ticker=None):

		self.driver.find_element_by_id("portfolio-tab-op-1").click()

		df = pd.DataFrame(columns=\
			["Symbol","type","qty","P-close","entry","Price","Change","%Change", "Day PNL", "PNL", "O/N"])

		positions = self.driver.find_element_by_xpath(\
			"/html/body/div[3]/section[1]/div[3]/div[2]/div[5]/div[2]/div[2]/div[1]/div/div[1]/div/table/tbody"\
				).text
		try:
			positions = positions.split("\n")
			for i in positions:
				i = i.split(" ")
				di = pd.DataFrame([i], columns=\
					["Symbol","type","qty","P-close","entry","Price","Change","%Change", "Day PNL", "PNL", "O/N"])
				df = pd.concat([df,di],ignore_index=True)

			if ticker in df["Symbol"].values:
				return df.loc[df["Symbol"]==ticker].values.tolist()[0]

			elif ticker not in df["Symbol"] and ticker != None:
				print(f"---Can't find your position on {ticker}---")

			else:
				return df

		except:
			print("Error. Couldn't get positions.")

	def _input_and_submit_order(self,quantity,order_type,price,sprice,offset,time_in_force,action):
		time.sleep(0.15)
		self.set_quantity(quantity)
		time.sleep(0.15)
		self.set_type_and_price(order_type, price, sprice, action, offset)
		time.sleep(0.1)
		self.set_tif(time_in_force)
		time.sleep(0.1)
		self.set_action(action)
		time.sleep(0.1)

	def submit_order(self,ticker, quantity, order_type, price=0, sprice=0,offset=0, time_in_force="DAY", action=None , auto_locate = False, fee_limit=1E+6):
		weekday = self.get_time()[0]
		hr = self.get_time()[1]
		#Check if it is the weekends
		if weekday == 5 or weekday == 6:
			print("Its the WeekEnds!!")

		elif hr >= 4 and hr <20 :
			self.set_ticker(ticker)
			time.sleep(0.2)

			hr = self.get_time()[1]
			short_status  =self.get_short_status(ticker)

			if auto_locate == True:
				if action.lower() == "short" and hr>=6 and hr<20:
					if short_status == "HTB":

						short_quantity = int(math.ceil(float(quantity/100))) * 100
					
						self.locate_short(ticker, short_quantity)
						time.sleep(0.05)
						self.reset_short_locate_info()
						time.sleep(0.05)

						if self.locate_success == True:
							self._input_and_submit_order(quantity,order_type,price,sprice,offset,time_in_force,action)
							time.sleep(0.05)

						elif self.locate_success == False:
							print(f"Error. Did not locate {ticker}.")
					
					# Incase the ticker is hard-to-borrow and we already located some shorts
					elif type(short_status) == int:
						available_shorts = short_status
						if available_shorts >= quantity:
							self._input_and_submit_order(quantity,order_type,price,sprice,offset,time_in_force,action)
							time.sleep(0.05)

						elif available_shorts < quantity:
							
							short_quantity = int(math.ceil(float((quantity-available_shorts)/100))) * 100
							self.locate_short(ticker, short_quantity, fee_limit)
							time.sleep(0.25)
							self.reset_short_locate_info()
							time.sleep(0.25)

							if self.locate_success == True:
								self._input_and_submit_order(quantity,order_type,price,sprice,offset,time_in_force,action)
								time.sleep(0.05)

							elif self.locate_success == False:
								print(f"Did not locate {ticker}")
						
					elif short_status == "ETB":
						self._input_and_submit_order(quantity,order_type,price,sprice,offset,time_in_force,action)
						time.sleep(0.25)


				elif action.lower() in ["short", "cover"] and hr<=6 and hr>20 and time_in_force == "DAY":
					print(f"Short/Cover only allowed between 6am and 8pm EST, use GTC order instead. Current time = {self.get_time()[1:]}\n")

				else:
					self._input_and_submit_order(quantity,order_type,price,sprice,offset,time_in_force,action)
					time.sleep(0.25)


			else:
				self._input_and_submit_order(quantity,order_type,price,sprice,offset,time_in_force,action)
				time.sleep(0.25)

				# To close the pop-up window that appears when you try to short without enough allocates
				# Will do nothing if there is no pop-up window i.e. we have enough shorts allocated
				if action.lower() == "short":

					self.cancel_locate()
					print(f"Error. Not enough shares allocated to execute the short, auto locate turned off, cancelled locate of {ticker}")
					time.sleep(1)

		else:
			print(f"Time is {hr}:{self.get_time[2]}, market not open.")

		time.sleep(0.25)
		self.reset()
		time.sleep(0.5)
		











			
class PaperTraderAPI(Tradezero_API):
	def __init__(self):
		super().__init__()


	def locate_paper_short(self,ticker,quantity):
		try:
			time.sleep(0.5)
			self.driver.find_element_by_id("short-list-input-symbol").send_keys(ticker,Keys.ENTER)
			time.sleep(0.5)

			if quantity % 100 == 0:
				self.driver.find_element_by_id("short-list-input-shares").send_keys(str(quantity),Keys.ENTER)
			else:
				print("quantity needs to be in steps of 100")
			time.sleep(0.5)
			
			WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "button-box.button-box-small.button-blue-filled")))
			time.sleep(1.5)

			self.driver.find_element_by_id("short-list-button-locate").click()
			time.sleep(0.1)

			WebDriverWait(self.driver, 6).until(EC.presence_of_element_located((By.CLASS_NAME, "icon-box.icon-box-accept")))
			time.sleep(0.1)

			# locate_info = self.driver.find_element_by_id("mCSB_7").text
			fee = self.driver.find_element_by_id(f"oitem-l-{ticker}-cell-6").text

			return float(fee)
		
		except:
			print(f"Couldn't locate short of {ticker}")
			return None		
#"Ticker","Date","Time", "Action","Price", "Shares", "Fee", "Profit"

	def submit_paper_order(self,ticker, quantity, order_type, price=0, sprice=0, time_in_force="DAY", action=None , auto_locate = False):
		tz  = timezone('US/Eastern')
		now = datetime.now(tz)
		date= now.strftime("%Y/%m/%d")
		times= now.strftime("%H:%M")

		if action == "short":
			self.locate_success = False
			self.set_ticker(ticker)
			time.sleep(0.25)
			
			if self.get_short_status(ticker) == "HTB":
							# round quantity to the nearest hundreds
							short_quantity = int(math.ceil(float(quantity/100))) * 100
							
							# locate it and reset the input field
							fee = self.locate_paper_short(ticker, short_quantity)
							time.sleep(0.25)
							self.reset_short_locate_info()
							time.sleep(0.25)

							if fee != None:
								print("Successive paper short")
								self.reset()
								return([ticker,date,times,"short",price,quantity,fee,quantity*price-fee])
							else:
								self.reset()
								return([])
			else:
				return([])

		if action == "cover":
			self.set_ticker(ticker)
			self.reset()
			return([ticker,date,times,"cover",price,quantity,0,-price*quantity])





	

	


