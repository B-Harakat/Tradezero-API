from Tradezero_API import Tradezero_API


print("Initiate!!")

zero = Tradezero_API()

# Opens a new window and logs in to the tradezero ZeroFree platform
zero.login(usr_name="XXXXXX",pass_word="xxxxxxxxxx")


# submit-method
zero.submit_order(ticker = "TSLA", quantity = 1, order_type = "LMT",price = 100, sprice = 100, time_in_force = "DAY", action = "Buy")

# auto locating shares to short enabled, the amount is the quantity input rounded up to the nearest hundreds, this one will locate 200 shares.
zero.submit_order(ticker = "DNN", quantity = 177, order_type = "LMT",price = 6900, sprice = 4200, time_in_force = "DAY", action = "Short", auto_locate=True)

# For when you want to locate shorts manually, quantity needs to be in steps of 100
# zero.locate_short("DNN", quantity=100)







