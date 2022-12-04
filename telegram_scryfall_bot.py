"""
## Telegram Scryfall Bot

This script was generated playing with https://chat.openai.com/chat, and it might not be functional, but it seems to me it is. 

> 10 minutes

### Prompts: 

- Hi! Do you know Scryfall API?
- Nice, I want to build an application using the Scryfall app to download the image of a given card, and I want to do so in Python. Could you provide an example?
- Nice, that is lovely, I also want to use this inside a Python Telegram bot, instead as a plain script. 
- Could you rewrite this example to use Telebot library and configure it to perform a polling? 
- Really nice, I would like that the Telegram bot captured the card from the input from the user through Telegram instead of having a variable. 
- We're almost done, I want the Telegram bot to listen to group messages, instead of messages from users; moreover, I want the bot to parse all the card names from the text using a regular expression which parses card names inside double brackets, such as [[Lightning bolt]]. It should return each match, not only the first one.
- A small detail, I want the bot to return both the image and the name of the card together to the group.
"""

import re
import requests
import telebot

# Create a telebot bot with your API token
bot = telebot.TeleBot("your_api_token")

# Define a function to handle incoming messages
@bot.message_handler(func=lambda message: message.chat.type == "group")
def handle_group_message(message):
    # Use a regular expression to find card names in double brackets
    card_names = re.findall(r"\[\[([^\]]+)\]\]", message.text)

    # Loop through each card name
    for card_name in card_names:
        # Use the Scryfall API to search for the card
        r = requests.get("https://api.scryfall.com/cards/named", params={"fuzzy": card_name})

        # Check the response status code to make sure the request was successful
        if r.status_code == 200:
            # Parse the JSON response
            card_data = r.json()

            # Get the image URL for the card
            image_url = card_data["image_uris"]["normal"]

            # Use the requests module to download the image
            image_data = requests.get(image_url)

            # Send the card name and downloaded image as a photo
            bot.send_photo(message.chat.id, photo=image_data.content, caption=card_name)
        else:
            bot.send_message(message.chat.id, "Could not find card with name: " + card_name)

# Start polling for messages
bot.polling()
