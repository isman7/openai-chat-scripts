"""
## Telegram Scryfall Bot 2

This script was generated playing with https://chat.openai.com/chat, and it might not be functional, but it seems to me it is. 

> 5 minutes

### Prompts: 
- Hi! Could you rewrite the following script, instead of using the "requests" library, using the "scrython" library. Also, refactor it into small functions? Please. (attached the contents of https://github.com/isman7/openai-chat-scripts/blob/master/telegram_scryfall_bot.py)
- Thanks for changing the library! I would also want the part of the code which handles the download of the image and the upload to be refactored info a function called "scryfall_to_telegram", thanks!
- I think the import from scrython is wrong, you should use directly "import scrython" and use the library as it is.

"""

import re
import scrython
import telebot

# Create a telebot bot with your API token
bot = telebot.TeleBot("your_api_token")

# Define a function to handle downloading and uploading an image from Scryfall to Telegram
def scryfall_to_telegram(card_name, message):
    # Use the Scryfall API to search for the card
    card = scrython.cards.Named(fuzzy=card_name)

    # Check the response status code to make sure the request was successful
    if card.object == 'card':
        # Get the image URL for the card
        image_url = card.image_uris['normal']

        # Use the Scrython library to download the image
        image_data = scrython.download(image_url)

        # Send the card name and downloaded image as a photo
        bot.send_photo(message.chat.id, photo=image_data, caption=card_name)
    else:
        bot.send_message(message.chat.id, "Could not find card with name: " + card_name)

# Define a function to handle incoming messages
def handle_group_message(message):
    # Use a regular expression to find card names in double brackets
    card_names = re.findall(r"\[\[([^\]]+)\]\]", message.text)

    # Loop through each card name
    for card_name in card_names:
        # Download and upload the image from Scryfall to Telegram
        scryfall_to_telegram(card_name, message)

# Start polling for messages
bot.polling()

