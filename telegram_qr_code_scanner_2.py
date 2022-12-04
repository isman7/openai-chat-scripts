"""
## Telegram QR Code scanner

This script was generated playing with https://chat.openai.com/chat, and it might not be functional, but it seems to me it is. 

> 15 minutes

### Prompts: 

- Hi! i would like to use the Google ML kit to locate barcodes in Python
- My bad, there is an API-based approach, such as the Vision API which I can use to that purpose?
- Aw! that is really nice! I would like to use this inside a Python app that uses "telebot" to load the image instead from the filesystem, to load it from a Telegram user. Could it be possible?
- Nice, I would like to filter only QR Codes and also send one message per each QR Code, not a stacked message. 

"""

# Import the necessary libraries
from google.cloud import vision
import telebot

# Authenticate your Google Cloud account
client = vision.ImageAnnotatorClient()

# Create a new Telegram bot and listen for incoming messages
bot = telebot.TeleBot("YOUR_BOT_TOKEN")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Get the file ID of the photo that was sent
    file_id = message.photo[-1].file_id

    # Use the Telegram API to download the photo
    file = bot.get_file(file_id)
    response = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(bot.token, file.file_path))

    # Use the Vision API's barcodeDetection method to detect barcodes in the photo
    image = vision.types.Image(content=response.content)
    response = client.barcode_detection(image=image)
    barcodes = response.barcodes

    # Process each detected barcode
    for barcode in barcodes:
        # If the barcode is a QR code, send a message with its value
        if barcode.symbology == "QR_CODE":
            bot.send_message(message.chat.id, "I found a QR code with the value: " + barcode.display_value)

bot.polling()
