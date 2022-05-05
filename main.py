from Tradezero_API import Tradezero_API


print("Initiate!!")

zero = Tradezero_API()

# For headless operation
#zero = Tradezero_API(headless=True) 

# Opens a new window and logs in to the tradezero ZeroFree platform
zero.login(usr_name="XXXXXX",pass_word="xxxxxxxxxx")


# Submit-method
zero.submit_order(ticker = "TSLA", quantity = 1, order_type = "LMT",price = 100, time_in_force = "DAY", action = "buy")

# Auto locating shares to short enabled, the amount is the quantity input rounded up to the nearest hundreds, this one will locate 200 shares.
zero.submit_order(ticker = "GME", quantity = 177, order_type = "LMT",price = 6900, time_in_force = "DAY", action = "short", auto_locate=True)

# This case of NearMarket-Limit order will set a limit buy order of AMC at the current bid price - 15
zero.submit_order(ticker = "AMC", quantity = 1, order_type = "NM-LMT",offset = -15, time_in_force = "DAY", action = "buy")

# This case of NearMarket-Limit order will set a limit sell order of DNN at the current ask price - 1.5,
# essentially market selling unless the bid/ask spread is larger than $1.5.
zero.submit_order(ticker = "DNN", quantity = 1, order_type = "NM-LMT",offset = -1.5, time_in_force = "DAY", action = "sell")

# Auto locate shorts for GME and place a short order at current ask-0.01. However, does nothing if the locate fee for 200 shares is above $8. 
# zero.submit_order(ticker = "GME", quantity = 177, order_type = "NM-LMT",offset = -0.01,\
#                   time_in_force = "DAY", action = "short", auto_locate=True, fee_limit = 8)

# For when you want to locate shorts manually, quantity needs to be in steps of 100
# zero.locate_short("DNN", quantity=100)

# Check for locate fee
# print(zero.get_locate_fee("DNN",quantity=100))











