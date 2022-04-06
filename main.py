import pyautogui
import time
from Tradezero_API import Tradezero_API

zero = Tradezero_API()

zero.login("XXXXX","xxxxxxx")

# Give time to load page
time.sleep(25)
print("Ready for order")

zero.submit_order(ticker = "DNN", quantity = 1, order_type = "Stop-LMT",price = 8.4, sprice = 7, action = "Sell")
print("submitted")
time.sleep(10)
zero.submit_order(ticker = "DNN", quantity = 1, order_type = "Stop-LMT",price = 8.4, sprice = 7.3, action = "Sell")
print("DIDIT")



