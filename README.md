# Tradezero-API
 A simple script to interact with the Tradezero web platform through python using selenium. 

## Requirement
 **Python 3.6+**
 **Stable internet**
 **FireFox** *Google should work too but i recommend firefox since it's the browser I used for the developemtn*
 **Have Selenium python set up on your computer**
 **A tradezero account**
 We are using the Tradezero web portal, the free basic one, no hotkeys needed (disable them if you've set it up previously)

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

 Now it should be working, insert your tradezero login info to `main.py` and run the file, a new window with the trading platform should be opened,you will be automatically logged in and some exemplary trades will be executed.
 
 ## Code Explained
 
 Example Code :
```python
 from Tradezero_API import Tradezero_API
 zero = Tradezero_API()

 zero.login(usr_name="XXXXXX",pass_word="xxxxxxxxxx")
 zero.submit_order(ticker = "TSLA", quantity = 1, order_type = "LMT",price = 100, sprice = 100, time_in_force = "DAY", action = "Buy")
```

There is really only 2 methods you need to acquiant yourself with for this API, the first one : `zero.login(usr_name="XXX",pass_word="xxx")` takes in your tradezero account name and pass word. It will open up a new window and automatically logs in to the web platform with your account info.

The second method is fairly straight forward, you input the value you normally would do in the web platform, and it will submit the order placement 
```
zero.submit_order(ticker, quantity , order_type, price = 0, sprice = 0, time_in_force = "DAY", action = None, auto_locate=False)
```
Compare it to the usual docker in the web platform


 zero.submit_order(ticker = "DNN", quantity = 351, order_type = "LMT",price = 6900, sprice = 4200, time_in_force = "DAY", action = "Short", auto_locate=False)


