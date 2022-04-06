from selenium import webdriver
import time
import pyautogui as pg

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

	def set_ticker(self, ticker):

		if type(ticker) != str:
			ticker = str(ticker)

		self.driver.find_element_by_id("trading-order-input-symbol").click()

		# writes as if you are pressing the keyboard itself, feel free to adjust the interval timer (time between key presses)
		# if you feel the execution isn't fast enough
		pg.typewrite(ticker +"\n", interval=0.005) 



	# price is equivalent to 'low' if order type is Range and the limit price for LMTs
	# ^input for the left price bar on the web free platform

	# sprice is equivalent to 'stop price' for Stop-MKT/LMT and 'high' for Range
	# ^input for the right price bar 

	def set_type_and_price(self, order_type, price = 0, sprice = 0):

		price = round(price, 2)
		sprice = round(sprice, 2)

		types = ["MKT","LMT","Stop-MKT", "Stop-LMT", "MKT-Close", "LMT-Close", "Range"]

		self.driver.find_element_by_xpath(f"/html/body/div[3]/section[1]/div[1]/div[2]/div/div[5]/span[2]/select/option[{str(types.index(order_type)+1)}]").click()


		self.driver.find_element_by_id("trading-order-input-price").send_keys(str(price))

		# self.driver.find_element_by_id("trading-order-input-price").click()
		# pg.typewrite(str(price), interval=0.005)

		self.driver.find_element_by_id("trading-order-input-sprice").send_keys(str(sprice))
		# pg.typewrite(str(sprice), interval=0.005)
	



	def set_quantity(self, quantity):

		self.driver.find_element_by_id("trading-order-input-quantity").send_keys(str(quantity))
		# pg.typewrite(str(quantity), interval = 0.005)




	def set_action(self, action):

		if action == "Buy" or action == 0:
			self.driver.find_element_by_id("trading-order-button-buy").click()

		if action == "Sell" or action == 1:
			self.driver.find_element_by_id("trading-order-button-sell").click()




	def submit_order(self,ticker, quantity, order_type, price=0, sprice=0, action=None):

		self.set_ticker(ticker)
		self.set_quantity(quantity)
		self.set_type_and_price(order_type, price, sprice)
		time.sleep(0.01)
		self.set_action(action)

	def reset(self):
		self.driver.find_element_by_id("trading-order-input-quantity").clear()

		self.driver.find_element_by_id("trading-order-input-price").clear()
		
		self.driver.find_element_by_id("trading-order-input-sprice").clear()
	



