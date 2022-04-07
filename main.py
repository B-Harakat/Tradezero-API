from Tradezero_API import Tradezero_API


print("Initiate!!")

zero = Tradezero_API()

# Opens a new window and logs in to the tradezero web zero platform
zero.login(usr_name="XXXXXXX",pass_word="xxxxxxx")


# submit-method
zero.submit_order(ticker = "TSLA", quantity = 1, order_type = "LMT",price = 100, sprice = 100, time_in_force = "DAY", action = "Buy")

# cleans the input field, required between submissions
zero.reset()

# For when you want to locate shorts manually
# zero.locate_short("DNN", quantity=100)

zero.submit_order(ticker = "DNN", quantity = 351, order_type = "LMT",price = 6900, sprice = 4200, time_in_force = "DAY", action = "Short", auto_locate=False)







