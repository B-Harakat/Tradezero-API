# Tradezero-API
 A simple script to interact with the Tradezero web platform through python using selenium. 

## Requirement
 **Python 3.6+**
 
 **Stable internet**
 
 **FireFox** *Google should work too but i recommend firefox since it's the browser I used for the developement*
 
 **Have Selenium-python set up on your computer**
 
 **A tradezero account** *We are going to use ZeroFree, the free basic web platform, no hotkeys needed (disable them if you've set it up previously)*

## Set Up Selenium
 *Note: I am running this on ubuntu 20.04, if you are using another OS, following instructions may not apply to you*

 First pip install selenium module
 
 ```pip3 install selenium```

 Next we need to download the web driver, here we choose Firefox but Chrome is an option as well

 ```sudo apt -y install firefoxdriver```

 If you don't have geckodriver already installed, set it up by downloading the latest tar from [here](https://github.com/mozilla/geckodriver/releases). 
 Change to the directory where the tar is located and type the following in the terminal
 ```
    tar -xvzf geckodriver*
    chmod +x geckodriver
    sudo mv geckodriver /usr/local/bin
 ```

 Now it should be working, insert your tradezero login info to `main.py` and run the file, a new window of ZeroFree should be opened,you will be automatically logged in and some exemplary trades will be executed.
 
 ## Code Explained
 
 Example Code :
```python
 from Tradezero_API import Tradezero_API
 zero = Tradezero_API()

 zero.login(usr_name="XXXXXX",pass_word="xxxxxxxxxx")
 zero.submit_order(ticker = "TSLA", quantity = 1, order_type = "LMT",price = 100, sprice = 100, time_in_force = "DAY", action = "Buy")
```

There is really only two methods you need to acquaint yourself with for this API, the first one : `zero.login(usr_name="XXX",pass_word="xxx")` takes in your tradezero account name and pass word. It will open up a new window and automatically logs in to ZeroFree with your account info.

If you are uncomfortable with typing in account info as plain text you could try something like what [this redditor shared](https://www.reddit.com/r/Python/comments/3sx851/comment/cx1m0j3/?utm_source=share&utm_medium=web2x&context=3)

The second method is fairly straight forward, you input the value you normally would do in the web platform, and it will submit the order placement 
```python
zero.submit_order(ticker, quantity , order_type, price = 0, sprice = 0, time_in_force = "DAY", action = None, auto_locate=False)
```
Compare it to the usual docker in the web platform
![alt text](https://github.com/Harakat-Bjorn/Tradezero-API/blob/main/Screenshot%20from%202022-04-07%2021-27-36.png "Tradezero web platform docker")

*Note    : if value were assigned to **price** and **sprice** when they are not relevant e.g. market buy/sell, they will be ignored.*

*Note.2  : order type includes all 7 default types i.e. MKT, LMT, Stop-MKT, Stop-LMT, MKT-Close,LMT-Close,Range. However, I do not recommend using order types of Stop-MKT/Stop-LMT with this API as they sometimes block other orders from being placed if executed poorly.* 

The python script will interact with the window via reading from and wrting to the html/css elements of the website using selenium, it all happens in the back ground so you can do other stuff on the computer as long as the window is not closed. *Update: not relevant if started in headless mode, since there'll be no window to close.

## Short Locate
This api has the capability of automatically locating shorts of hard-to-borrow stocks, however, use this with caution as the locate will be executed no matter how much it will cost. *Update: No longer the case, see below*

To enable auto locate, simply set the `auto_locate` flag to `True`.

```python
zero.submit_order(ticker, quantity , order_type, price, sprice, time_in_force, action, auto_locate=True)
```

To manually locate shorts,
```python
zero.locate_short(ticker = "TSLA",quantity = 100)
```

***One Last Note***

Looking through `Tradezero_API.py` you will find alot of time.sleep() calls, this is to account for the time it takes for the web page to load stuff inbetween our scripts, feel free to adjust these if you have faith in your internet speed and find the code execution slow. 

Finally, I need to emphasize that this API is not meant for HFT or scalping or anything requiring rapid order firing, use at your own risk.




## Update 5/5/2022

Headless start is now an option.
```python
zero = Tradezero_API(headless=True)
```
This way no visual browser tab will appear.

The full list of positional arguments of `submit_order()` has been updated to
```python
zero.submit_order(ticker, quantity , order_type, price = 0, sprice = 0,offset=0, time_in_force = "DAY", action = None, auto_locate=False, fee_limit=1E+6)
```
### Fee Limit
The `fee_limit` argument lets you set a threshold for the short locate fee, if the locate fee is above this limit then the order execution is halted and nothing happens.

If you want to check the locate fee of a specific stock without placing an order, use `fee = zero.get_locate_fee(ticker,quantity)`

### Near-Market Limit Order
Added a custom order type: `order_type = NM-LMT`. When set, it will place a limit order at the bid/ask price (*depending on if you are going long or short*) + the `offset` value. 

### Additional Features
```python
df = zero.get_positions(ticker=None)
```
Returns a pandas dataframe of all the stocks you hold along with its information, equivalent to the information tab in the web platform. Setting a specific ticker will instead return a list with the info of that ticker.


```python
zero.cancel_all_orders()
```
Cancels all active orders. Does so sequentially so might take a while if there are many orders.

```python
my_money = zero.get_funds()
```
Returns available funds (Equity - Exposure), does not account for available leverage.









