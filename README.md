# Space Trucker Trading Tracker

![Space Trucker Trading Tracker](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/responsive-website-mockup.png)

## Introduction

The Space Trucker Trading Tracker (STTT) is a cargo inventory management tool made for the citizens of Star Citizen.

Star Citizen (SC) is a deep space, science fiction game / simulation set 930 years in the future. The STTT's main purpose allows SC Traders to keep track of their ship's current cargo inventory and estimated value.

The way trading works in SC is you go to one of many locations and you purchase a particular commodity with "alpha United Earth Credits" (aUEC) which is the in-game currency. You then transport that commodity to another location that's in need of it, and sell them for a profit.

The STTT is at heart a stock and inventory management tracking system that keeps you up to date with your current inventory, your current financial risk and how much you've made or are due to make on your current trading run. 

The commodity pricing in SC is also determined by demand and supply so the pricing is always changing. An organisation called UEX Corp have agents that regularly check the prices at different locations and provide an API that lists the average commodity prices. The STTT uses this data to populate the price inputs and provide users with their estimated profit. 

I've taken a mobile first design approach with accessibility and ease of use at the top of STTT's priorities. This makes it simple and easy for all space truckers across the galaxy to input the prices and trades from their small screened device without having to switch views on their main monitor and be at risk of piracy. But it's also responsive to work on all devices.

A deployed version may be found here: [Space Trucker Trading Tracker](https://space-trucker.herokuapp.com/)

# Instructions for Use and Existing Features

This app uses session id cookies to associate trades and inventory with the individual user. If your browser blocks cookies then you'll need to log in with your google account.

![Google Log In](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/google-log-in.png)

If you don't want to or don't have a google account, you can register or log in to the STTT using the link at the bottom of the page.

![Registration and Log In Links](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/register-log-in-links.png)

To register, simply fill out the form. No email address is required.

![Registration Page](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/register-page.png)

Once you're registered you'll be able to log in.

![Log In Page](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/log-in-page.png)

Once you're ready to start tracking your trading, first select the commodity from the drop down list.

![Drop Down Commodity List](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/drop-down-commodity-list.png)

The most recent average buy/sell prices for this commodity will then be inserted into the trade boxes automatically.

![Buy Trade Box](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/buy-trade-box.png)

Adjust the buy value to the unit price you're actually paying, then adjust the unit amount to how many you're actually buying.

![Buy Button](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/buy-button.png)

Now tap or click the "BUY" button to input your trade. You'll notice your total balance will now show a negative value. This is the total amount you're now risking and what you'd lose in the case of a catastrophe.

![Negative Balance](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/negative-balance.png)

You'll notice below now that the commodity you bought will appear in a list of your cargo. If you buy a different commodity it will also be added. And if you fly to a different location to buy the same commodity it will be added to your existing cargo inventory of the same commodity.

![List Of Cargo](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/list-of-trades.png)

Once you've arrived at the selling location, you can simply tap or click the row of the commodity you wish to sell and it will automatically select the right commodity and populate the details into the buy/sell value boxes.

![Trade List Row](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/trade-list-row.png)

Now edit the values to make sure the price and number of units are correct, then hit the "SELL" button.

![Sell Box](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/sell-box.png)

Your total balance at the top will then be updated and that amount of cargo will be deducted from your inventory. If you sell all units of that commodity, the commodity will be deleted from your cargo commodity list.

In your list you'll see some columns with information about the commodites you've bought. The "Cost" is the amount that you have invested in that commodity, and how much you're risking.

![Commodity Cost Column](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/commodity-cost-column.png)

The "Units" column is the amount of units you have of that commodity.

![Commodity Units Column](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/commodity-units-column.png)

The "Value" column is the estimated sale price for the whole amount of that commodity. The value is calculated based on it's average sell price.

![Commodity Value Column](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/commodity-value-column.png)

The "Due" column is the profit that you stand to make from selling all of that commodity at the estimated price.

![Commodity Due Column](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/commodity-due-column.png)

On the bottom row of your cargo list you'll see the totals. The total "Due" may not seem like it's calculated correctly, but this is taking into account all of your trades - including the ones you've already sold since your last reset. This helps to show how much profit you expect to make for the entire trade run.

![Commodity Due Total](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/commodity-due-total.png)

At the end of each trade run you can tap or click the "Reset Profit" button. This does exactly what you think and resets the profit recorded to zero.

![Reset Profit Button](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/reset-profit-button.png)

If you'd like to find out what the most profitable commodities are, you can view all of the prices on the Latest Prices page by clicking the link at the bottom.

![Latest Prices Link](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/latest-prices-link.png)

From there you can view the latest reported buy / sell prices.

![Latest Prices Page](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/latest-prices-page.png)

If you'd like to see the last date the prices were updated, you'll need to view it on a wider screen.

![Latest Prices Wide Page](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/latest-prices-wide-page.png)

If you're granted admin privilidges you'll also be able to manually edit the commodity prices. Just press the button to take you to the Price Editor.

![Price Editor Button](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/price-editor-button.png)

In the price editor, just edit the buy / sell values for the commodity you'd like to update and hit the "Edit" button.

![Price Editor Page](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/price-editor-page.png)

You'll also be able to view the dates last modified in a wider screen view. The commodities are listed in order of date. The oldest prices most urgently in need of update are listed at the top.

![Price Editor Wide Page](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/price-editor-wide-page.png)

From all pages you're able log out by pressing the button at the bottom of the page.

![Log Out Button](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/log-out-button.png)

And you'll also find a button to return to the main page at the top of each page (unless you're already on that page!)

![Home Button](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/home-button.png)

# Planning 

I planned to make a Star Citizen trading app that would work on any web browser and to be a reliable and easy to use tool for the user to want to make it an invaluable resource when they're trading multiple commodities at once.

I came up with the name of "Space Trucker Trading Tracker" as it's a bit of a tongue twister but has a nice ring to it. I think most people would refer to it as just STTT.

Before writing any code I first drew a wireframe outline on the back of an envelope.

Although basic, this helped me to realise what features I needed to code on the back-end, just as much as the front-end.

<img src="https://github.com/MadStu/space-trucker/raw/main/static/readme-images/wireframe.jpg" width="250">

## Features Left to Implement

- Code API retrieval to get in-game ships and the cargo bay size info.
    - User option to choose unit amount by ship size.
    - Save the user's ship to the databases so it remembers.
    - Default the unit amount to the remaining cargo bay space.
- Code API retrieval to get the buy/sell locations for each commodity.
    - Provide an option for the user to see where to buy or sell.

# Data Model

The Trade model holds all of the users' trade details, the commodity, the amount of units, the price, the profit to expect and the time the trade was made.

The CommodityPrice model holds all of the commodity details received from the UEX API.

The ErrorList model holds a list of errors that may have been encountered.

The UserProfit model holds the users' total profit.

## Logic Flow

Index view

- When the main index page loads, the first thing that happens are some variables are defined such as the epoch_time and getting the session key.

- Next the view checks to see if a record exists for the "Time Updated" object.
    - If it exists, it will retrieve the time of the last update from the UEX API.
    - If it doesn't exist, it creates one.

- It will then check how much time has elapsed since last API update
    - If more than 6 hours has elapsed, the API is called and the time is recorded.
        - delete_old_trades() is also called to remove trades in the database that are over 14 days old.
        - A check is carried out to see if the API is working. 
            - If a status of "OK" is received, handle_api_data() is called to insert the data into the database.
            - This function then loops through the commodity data received. 
                - If a commodity doesn't exist, it's created.
                - If a commodity already exists, the date_modified dates are then compared to see if the prices already in the database is newer.
                    - If the data received is newer, then it will update the existing record.

- When the index view receives form data by POST method, it checks to see if it was the user pressing the "Reset Profit" button.
    - If it was the reset button pressed it then checks to see if the user (defined by the session key received) has trades already exsting in the database.
        - If it exists, it then resets the user's profit value to 0.

    - If it wasn't the reset button, then it was a trade entry into the database and it checks the boolean value for whether it was a buy or sell.
        - If True, it was a buy trade and the variables are assigned accordingly.
        - If False, it was a sell trade and the variables are assigned accordingly.
    - The variables that have been assigned are then insterted in to the database using the handle_form_data() function.
        - handle_form_data() then checks if the user already has a trade with the same commodity.
            - If it exists, it then it gets that object and checks if it's a buy or sell trade.
                - If a buy trade, the existing commodity amount is updated with the added number of units bought and the cost and profit expected is calculated to reflect that.
                - If a sell trade, a check is made to see if too much cargo has sold than exists in the inventory.
                    - If too much then an error message is added to the database using the add_error_message() function.
                        - add_error_message() simply stores an error message into the ErrorList model.
                    - If it passes this check, the existing commodity amount is reduced to reflect how many units the user has remaining in their cargo. The cost and profit are also updated.
                - Another check is made against the ErrorList model and if there isn't one, it checks the inventory amount.
                    - If there is no remaining cargo, then this whole trade object is deleted.
                    - If there is cargo still remaining, the object is updated with the newly calculated values.
                - user_profit_calc() is called to update the total profit amount.
                    - First a check is made, if an object of the profit for that user does not exist, a new one is created.
                    - The function then updates the user's profit by subtraction if it's a buy trade, or addition if they've sold.
            - If the commodity doesn't yet exist in the user's trades, then the cost and potential profit are calculated and a new record is inserted with the details. With user_profit_calc() being called again to update total profit.
        - update_commodity_prices() is then called which checks if there's any recorded errors and that the user is a superuser.
            - If the user is a superuser, the commodity price is updated with the values received in the trade form.
        - After all the form data is handled, the page is redirected back to the home page.

- Next the index view gets some information from the database to populate the template form in anticipation of what the user will be using.
    - If trade objects exist for this user, it gets the most recently traded item and retrieves the details and creates the variable.
    - If a trade object doesn't exist, we provide it with some default values to populate.

- Next it calculates the totals by looping through all the user's trades and puts them in variables for the template.

- The total profit is next retrieved with a check to see if it exists.
    If it doesn't exist, a default of 0 is assigned to the template variable.

- Within the context dictionary, variables from the view are assigned for the templates. commodity_data() is also assigned which is a list of all the commodity objects in the CommodityPrice model.
    - commodity_data() also filters out commodities which are not relevant to star citizen traders.

Editor view

- The editor view receives and handles the POST data when a superuser is editing prices of a commodity from the editor page.
    - The CommodityPrice object is updated with the new prices, as well as the time being saved to show when it was last updated.

- The context dictionary just sends the commodity_data() list.

Prices view

- The prices view is just for information and only sends the commodity_data() list to the template.

## Technologies Used

- Python

- Django

- JavaScript

- HTML

- CSS

- PostgreSQL

- Heroku

- Bootstrap

# Testing

I've tested the code continuously as I've developed it, making sure all functionality works as it should and fix any typos or coding errors as and when they happen in all scenarios.

I've also asked friends and players of Star Citizen to test the STTT with no errors being reported.

## Validator Testing 

- Python
    - No errors or warnings were returned when passing through [PEP8online](http://pep8online.com/).

- HTML
    - No errors or warnings to show when passing through the official [W3C Validator](https://validator.w3.org/nu/?doc=https%3A%2F%2Fspace-trucker.herokuapp.com%2F).
- CSS
    - No errors were found when passing through the official [(Jigsaw) validator](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fspace-trucker.herokuapp.com%2Fstatic%2Fcss%2Fstyle.css).

- JavaScript
    - No errors are shown when passing through the [Beautful Tools Javascript Validator](https://beautifytools.com/javascript-validator.php).

- Accessibility
    - No errors or contrast errors [Wave](https://wave.webaim.org/report#/https://space-trucker.herokuapp.com/).

## Bugs

- ~~Entering other values into int form field produces error.~~
  - Solved by changing input type to correct values for form validation.
- ~~API limitations meant the request limit had exceeded.~~
    - Solved by saving API details to a database so it doesn't require updating so often.
- ~~Sessions won't work on all browsers due to session id's not staying the same.~~
    - Solved by adding the option for users to register instead of relying on browser cookies.
- ~~Profit tracker will only add and minus the same cost amount.~~
    - Solved by correcting an incorrect variable used to send to the profit tracker function.
- ~~Resetting profit when entry didn't exist would cause error.~~
    - Solved by adding a check to see if the record existed.
- ~~Total profit is only being worked out by the commodity database sell price.~~
    - Solved by correcting an incorrect variable.
- ~~Due Profit wasn't calculating correctly.~~
    - Solved. It was calculating the wrong price. I compared code with a previous commit to find where I'd made the mistake.
- ~~Static files not loading on Heroku.~~
    - Solved by installing whitenoise to allow the app to serve its own static files.
- ~~Received the Error: local variable referenced before assignment.~~
    - Solved. It was working with sell trades, but I'd forgot to create the variable in the right place for the buy trades.

# Deployment

I've deployed it on heroku.com and used the following method.

- The Space Trucker Trading Tracker can be deployed to heroku.com. The steps to deploy are as follows:
- Sign up or log in to GitHub.com.
- Navigate to this repository page at https://github.com/MadStu/space-trucker.
- Press the "Fork" button which will make a copy of this space-trucker repository in your own account.
- Sign up or log in to heroku.com.
- Click "New" then "Create new app".
- Enter an app name, choose your region and then click "Create app".
- On the next page, go to the Settings Tab.
- Click on "Add buildpack", add the python build pack, then save changes.
- Click on "Reveal Config Vars" and enter the following vars without quotes:
    - Key: "SECRET_KEY" Value: "Enter your own randomly generated key, you could use a 504-bit WPA Key from [randomkeygen.com](https://randomkeygen.com/)"
    - Key: "UEX_API_KEY" Value: "Enter your API Key from [UEX Corp](https://uexcorp.space/api.html)"
- Go to the Resources Tab, then search for and add the Heroku Postgres add-on.
- Click on the Deploy tab at the top, select GitHub and connect to your GitHub account.
- Search for the repository name (space-trucker) and click the "Connect" button.
- Scroll down to the Manual deploy section and choose the main branch to deploy from.
- Click the "Deploy Branch" button which syncs the heroku.com files with the repository.

# Credits 

- I used the amazing API created by the [UEX Corp](https://uexcorp.space/) team.
- I intially found the colours and what colours went best with them from [w3schools](https://www.w3schools.com/colors/color_tryit.asp?color=DarkSlateGray).
- I used the Michroma font from [Google Fonts](https://fonts.google.com/specimen/Michroma#standard-styles).
- The nice little icons in the buttons are from [Font Awesome](https://fontawesome.com/).
- I often used [W3Schools](https://www.w3schools.com/python/), [Django docs](https://docs.djangoproject.com/en/4.0/) and [Bootstrap Docs](https://getbootstrap.com/docs/5.2/getting-started/introduction/) as a guide for finding the best solutions and using the code in the correct format.
- I'd also search google a lot which more often than not would show similar solutions written on [Stack Overflow](https://stackoverflow.com/).
- I used a wallpaper image of a large cargo ship called a Drake Caterpillar with credits to Cloud Imperium Gaming for creating the [Star Citizen](https://tinyurl.com/2yet2hz9) game.
- https://www.w3schools.com/howto/howto_css_modals.asp

## Final Notes

I really do enjoy coding with Python and learning to use Django has been a real eye opener. I can see the potential Django has for creating ultra powerful web apps with it's batteries included features.

The links between the MVT was a struggle at first but now I'm nearing the end of the project I'm literally dreaming of how everything ties in together. At the beginning I felt like I'd been thrown in at the deep Django end of the pool, but now I know my future projects will be a lot easier to begin with.
