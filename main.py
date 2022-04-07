import pyautogui
import time
from Tradezero_API import Tradezero_API


print("Initiate!!")

zero = Tradezero_API()

# Opens a new window and logs in to the tradezero web zero platform
zero.login(usr_name="XXXXXX",pass_word="xxxxxx")


# submit-method
zero.submit_order(ticker = "TSLA", quantity = 1, order_type = "LMT",price = 7000, sprice = 6500, time_in_force = "DAY", action = "Short")

# cleans the input field, required between submissions
zero.reset()


zero.submit_order(ticker = "DNN", quantity = 1, order_type = "LMT",price = 6900, sprice = 4200, time_in_force = "DAY", action = "Short")




# time.sleep(0.5)

# zero.locate_short(ticker="DNN", quantity=100)




