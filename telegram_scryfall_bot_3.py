"""
## Telegram Scryfall Bot

This script was generated playing with https://chat.openai.com/chat, and it might not be functional, but it seems to me it is. 

> 2 minutes

### Prompts: 

- Hi there, could you explain me this code? (paste the contents in https://github.com/isman7/openai-chat-scripts/blob/master/telegram_scryfall_bot.py)
- Nice, could you rewrite this bot to use the `python-telegram-bot` library instead of `telebot`, please?
- Could you replace the `request` library by the `scrython` library? 

"""

import re
from scrython import ScryfallClient
from telegram.ext import Updater

# Create a bot and initialize it with your API token
updater = Updater("your_api_token")

# Define a function to handle incoming messages
def handle_group_message(update, context):
    # Use a regular expression to find card names in double brackets
    card_names = re.findall(r"\[\[([^\]]+)\]\]", update.message.text)

    # Loop through each card name
    for card_name in card_names:
        # Use the Scryfall API to search for the card
        scryfall = ScryfallClient().cards.named(fuzzy=card_name)

        # Check the response status code to make sure the request was successful
        if scryfall.status_code == 200:
            # Parse the JSON response
            card_data = scryfall.data()

            # Get the image URL for the card
            image_url = card_data["image_uris"]["normal"]

            # Use the requests module to download the image
            image_data = requests.get(image_url)

            # Send the card name and downloaded image as a photo
            update.message.chat.send_photo(photo=image_data.content, caption=card_name)
        else:
            update.message.chat.send_message("Could not find card with name: " + card_name)

# Start the bot
updater.start_polling()
