import pyautogui
import time
from Tradezero_API import Tradezero_API

zero = Tradezero_API()

zero.login(usr_name="XXXXX",pass_word="xxxxxxx")

# Give time to load page
# Adjust according to your internet speed 
time.sleep(25)
print("Ready for order")


zero.submit_order(ticker = "DNN", quantity = 1, order_type = "Stop-LMT",price = 8.4, sprice = 7, action = "Sell")

# Above execution takes some time, hence this buffer before next order
time.sleep(1)

zero.submit_order(ticker = "DNN", quantity = 1, order_type = "Stop-LMT",price = 8.4, sprice = 7.3, action = "Sell")

print("Done!")



