# SlackFood
Simple python3 script for parse restaurant daily menu from Zomato and post it to the slack via webhook.

# Config
Fill the config.sample.json with your credentials and rename it to the sample.json

Fill the Zomato ids and names of your restaurants to restaurants.json

# Requirements
only requests library, you can install it by this code:

> pip3 install -r requirements.txt

# Examples
If you want to debug, you can run:
> python3 main.py

and output will be printed to console.


If you want post it via webhook you can run:
> python3 main.py -s

and output will be posted via webhook.

If you want display food only when price is defined you can run:

> python3 main.py -wp
