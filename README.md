# The Space Trucker Trading Tracker

## A Trading Tool for Star Citizen

https://space-trucker.herokuapp.com/

[Star Citizen](https://tinyurl.com/2yet2hz9) is a futuristic, deep space, science fiction game / simulation. This tool allows Star Citizen Traders to keep track of their ship's current cargo inventory and estimated value.

I will take a design thinking and agile approach to creating the app.

### Bugs
- Entering other values into int form field produces error
    - Solved. Changed input type to correct input for form validation
- API limitations meant the request limit had exceeded
    - Solved. Saved API details to a databsse so doesn't require updating so often
- Sessions won't work on all browsers due to session id's not staying the same
    - Solved. Added option for users to register instead of relying on their session cookies
- Profit tracker will only add and minus the same cost amount
    - Solved. corrected an incorrect variable used to send to the profit tracker function
- Resetting profit when entry didn't exist would cause error
    - Solved. Added a check to see if the record existed
- Total profit is only being worked out by the commodity database sell price
    - Solved. Was sending the wrong variable
- Due Profit wasn't calculating correctly
    - Solved. Was calculating the wrong price

### Todo
- Main Styling
- Admin Area
- Readme
- Single login social accounts
- Refactor Code again
- Error messages

### Credits
- [UEX](https://uexcorp.space/) for providing an amazing API.
- Cloud Imperium for creating [Star Citizen](https://tinyurl.com/2yet2hz9)