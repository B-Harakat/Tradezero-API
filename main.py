import pyautogui
import time
from Tradezero_API import Tradezero_API

zero = Tradezero_API()

# Opens a new window and logs in to the tradezero web free platform
zero.login(usr_name="XXXXX",pass_word="xxxxxx")

# Give time to load page
# Adjust according to your internet speed 
time.sleep(20)
print("Ready for order")

# submit-method
zero.submit_order(ticker = "TSLA", quantity = 1, order_type = "Stop-LMT",price = 3000, sprice = 2500, action = "Sell")

# cleans the input field, required between submissions
zero.reset()

zero.submit_order(ticker = "TSLA", quantity = 1, order_type = "Stop-LMT",price = 6900, sprice = 4200, action = "Sell")

print("Done!")



