"""
## Flask Scryfall Bot

This script was generated playing with https://chat.openai.com/chat, and it might not be functional, but it seems to me it is. This was a difficult one to pull out, as I debugged it a little bit. 

The worker in fact broke, and had to restart it. 

> 35 minutes

### Prompts: 
- Hi there, could we modify this code snippet instead to be a Telegram Bot, to be a webview written in Flask that whenever the user inputs in a prompt a text, we parse the matches of cards and return an adaptative grid of images (i.e. using Bootstrap 4), of those images? (paste code in https://github.com/isman7/openai-chat-scripts/blob/master/telegram_scryfall_bot.py)
- Continue
- Could you please join all the steps into a unique Python file, where the HTML part is embedded as a multiline string variable (triple string quotes) and give it to me, thanks. 
- continue
- Resend me please, from the "cards_html" definition as a code block, the previous answer is broken
- Hi, there is something wrong with the scryfall library: Traceback (most recent call last):
  ...
ImportError: cannot import name 'ScryfallClient' from 'scrython' (/home/ibenito/.pyenv/versions/miniconda3-latest/envs/gpt3-playground/lib/python3.10/site-packages/scrython/__init__.py)
- Error: While importing 'flask_scryfall_bot', an ImportError was raised:

Traceback (most recent call last):
  ...
ModuleNotFoundError: No module named 'scrython.Client'
- Error: While importing 'flask_scryfall_bot', an ImportError was raised:

Traceback (most recent call last):
  File "/home/ibenito/.pyenv/versions/miniconda3-latest/envs/gpt3-playground/lib/python3.10/site-packages/flask/cli.py", line 218, in locate_app
    __import__(module_name)
  File "/home/ibenito/git/openai-chat-scripts/flask_scryfall_bot.py", line 4, in <module>
    from scrython import Client
ImportError: cannot import name 'Client' from 'scrython' (/home/ibenito/.pyenv/versions/miniconda3-latest/envs/gpt3-playground/lib/python3.10/site-packages/scrython/__init__.py)
- neither of those approaches seem to work, It should be using directly the library as     >>>import scrython
    >>>card = scrython.cards.Named(fuzzy="Black Lotus")
- everything was fine in the home webview, but when searching the cards something odd happended: [2022-12-09 10:37:51,305] ERROR in app: Exception on / [POST]
Traceback (most recent call last):
  ...
    raise RuntimeError('There is no current event loop in thread %r.'
RuntimeError: There is no current event loop in thread 'Thread-2 (process_request_thread)'.
- continue, in a new code block
- [2022-12-09 10:41:08,261] ERROR in app: Exception on / [POST]
Traceback (most recent call last):
  ...
AttributeError: 'Named' object has no attribute 'status_code'
- continue
- Everything worked without any exception, but the search is empty! Could you check if the line "if scryfall.object == 'card':" makes sense, if not, remove it and use a try except based approach to add the data to the cards dictionary. 
- continue
- It seems scrython is not finding the cards: flask --app flask_scryfall_bot.py run
 * Serving Flask app 'flask_scryfall_bot.py'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
Could not find card with name: Krenko, mob boss
Could not find card with name: Krenko, street
- I modified the script, I think it will work now, could you spot the differences? (paste a cleaned script by myself)

> Dead thread, starting a new one:_
> Crashes ones again when passing the exact code there is in this file. Strange the message is: An error occurred. If this issue persists please contact us through our help center at help.openai.com. 

"""


import asyncio
import re
from flask import Flask, render_template_string, request
import scrython

app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def home():
    # Render the HTML template for the home page
    return render_template_string(home_html)

# Define a route for the / URL that handles POST requests
@app.route('/', methods=['POST'])
def search_card():
    card_name = request.form['card_name']

    # Use a regular expression to find card names in double brackets
    card_names = re.findall(r"\[\[([^\]]+)\]\]", card_name)

    # Create a dictionary to map card names to image data
    cards = {}

    # Loop through each card name
    for card_name in card_names:
        # Create and set the event loop
        asyncio.set_event_loop(asyncio.new_event_loop())

        # Use the Scryfall API to search for the card
        try:
            card = scrython.cards.Named(fuzzy=card_name)


            # Get the image URL for the card
            image_url = card.image_uris()["normal"]


            # Add the card name and image url to the dictionary
            cards[card_name] = image_url
        except Exception as e:
            # If an error occurs, add an error message to the dictionary
            print(e)
            print("Could not find card with name: " + card_name)

    # Render the HTML template for the cards page, passing the cards dictionary as a parameter
    return render_template_string(cards_html, cards=cards)


# Define the HTML templates as multiline string variables
home_html = """
<!doctype html>
<html>
    <head>
        <title>Card Search</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous">
    </head>
    <body>
        <h1>Card Search</h1>
        <form action="/" method="post">
            <input type="text" name="card_name" placeholder="Enter a card name">
            <button type="submit">Search</button>
        </form>
    </body>
</html>
"""

cards_html = """
<!doctype html>
<html>
    <head>
        <title>Card Search</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous">
    </head>
    <body>
        <h1>Card Search</h1>
        <div class="card-deck">
            {% for card_name, image_data in cards.items() %}
                <div class="card">
                    <img src="{{ image_data }}" class="card-img-top" alt="{{ card_name }}">
                    <div class="card-body">
                        <h5 class="card-title">{{ card_name }}</h5>
                    </div>
                </div>
            {% endfor %}
        </div>
    </body>
</html>
"""

# Run the Flask app

if __name__ == '__main__':
	app.run()

	
