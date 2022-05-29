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

Once you've arrive at the selling location, you can simply tap or click the row of the commodity you wish to sell and it will automatically select the right commodity and populate the details into the buy/sell value boxes.

![Trade List Row](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/trade-list-row.png)

Now edit the values to make sure the price and number of units are correct, then hit the "SELL" button.

![Sell Box](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/sell-box.png)

Your total balance at the top will then be updated and that amount of cargo will be removed from your inventory. If you sell all units of that commodity, the commodity will be removed from your cargo list.

In the cargo list you'll see some columns with information about the commodites you've bought. The "Cost" is the amount that is what you have invested for that commodity, what it has cost you to buy, and how much you're risking.

![Commodity Cost Column](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/commodity-cost-column.png)

The "Units" column is the amount of units you have of that stock.

![Commodity Units Column](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/commodity-units-column.png)

The "Value" column is the estimated sale price for the whole amount of that commodity. The value is calculated based on the average price of the current stock.

![Commodity Value Column](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/commodity-value-column.png)

The "Due" column is the profit that you stand to make from selling all of that commodity at the estimated price.

![Commodity Due Column](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/commodity-due-column.png)

At the bottom of your cargo list you'll see the totals. The total "Due" may not seem like it's calculated correctly, but this is taking into account all of your trades - including the ones you've already sold since your last reset. This helps to show how much profit you expect to made for the entire trade run.

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

You'll also be able to view the dates last modified ina wider screen view. The commodities are listed in order of date. The oldest prices most urgently in need of update are listed at the top.

![Price Editor Wide Page](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/price-editor-wide-page.png)

From all pages you're able log out by pressing the button at the bottom of the page.

![Log Out Button](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/log-out-button.png)

And you'll also find a button to return to the main page at the top of each page that isn't the main page.

![Home Button](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/home-button.png)

# Planning 

I planned to make a Star Citizen trading app that would work on any web browser and be reliable and easy to use enough for the user to want to make it an essential tool when they're trading multiple commodities.

I came up with the name of "Space Trucker Trading Tracker" as it's a bit of a tongue twister but has a nice ring to it. I hope most people would refer to it as STTT for short.

Before writing any code I first drew a wireframe outline on the back of an envelope.

This helped me to realise what features I needed to code on the back-end, just as much as the front-end.

![Wireframe Drawing](https://github.com/MadStu/space-trucker/raw/main/static/readme-images/wireframe.png)

## Features Left to Implement

- Code API retrieval to get in-game ships and the cargo bay size info.
- User option to choose unit amount by ship size.
- Save the user's ship to the databases so it remembers.
- Default the unit amount to the remaining cargo bay space

# Data Model

## Logic Flow

## Libraries Used

# Testing

## Validator Testing 

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

# Credits 

- I used the amazing API created by the [UEX Corp](https://uexcorp.space/) team.
- I intially got the colours and what went best with tehm from [w3schools](https://www.w3schools.com/colors/color_tryit.asp?color=DarkSlateGray).
- I used the Michroma font from [Google Fonts](https://fonts.google.com/specimen/Michroma#standard-styles).
- The nice little icons in the buttons are from [Font Awesome](https://fontawesome.com/).
- I often used [W3Schools](https://www.w3schools.com/python/), [Django docs](https://docs.djangoproject.com/en/4.0/) and [Bootstrap Docs](https://getbootstrap.com/docs/5.2/getting-started/introduction/) as a guide for finding the best solutions and using the code in the correct format.
- I'd also search google which more often than not would show solutions written on [Stack Overflow](https://stackoverflow.com/).
- I used a wallpaper image of a large cargo ship called a Drake Caterpillar with credits to Cloud Imperium Gaming for creating the [Star Citizen](https://tinyurl.com/2yet2hz9) game.

## Final Notes
