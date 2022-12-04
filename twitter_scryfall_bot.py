"""
## Telegram Scryfall Bot

This script was generated playing with https://chat.openai.com/chat, and it might not be functional, but it seems to me it is. The functionality was not achieved up to a 100%, that is because the bot returns the four images stacked into one image, and when asked to correct this, the output was broken.

> 20 minutes

### Prompts: 
- Hi there! Do you know what is Scryfall? 
- Nice, I want to build an application using the Scryfall app to download the image of a given card, and I want to do so in Python. Could you provide an example?
- That is nice! I was thinking of use this code inside a Twitter bot that responded to users with that card image!
- Aw, that is nice! Could we read the card name from the previous tweet from the user, by parsing the tweet looking for card names inside double brackets, such as [[lightning bolt]], and I want the bot to response with the first four matches.
- I would only suggest 2 changes to the script: first, the four images should be sent in only one update; and, I would like to run the script indefinitely by some kind of polling mechanism, looking actively for tweets. 
- Could you rewrite this example using the "twitter" python library instead of twython?

"""

import io
import re
import time
from PIL import Image
import requests
import twitter

# Set the Twitter API keys
api_key = "YOUR_API_KEY"
api_secret_key = "YOUR_API_SECRET_KEY"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

# Set the polling interval in seconds
poll_interval = 30

# Create a Twitter API client
client = twitter.Api(consumer_key=api_key,
                     consumer_secret=api_secret_key,
                     access_token_key=access_token,
                     access_token_secret=access_token_secret)

while True:
    # Get the latest tweets mentioning the bot
    tweets = client.GetMentions()

    # Check if there are any tweets
    if len(tweets) > 0:
        # Get the latest tweet mentioning the bot
        latest_tweet = tweets[0]

        # Extract the card names from the tweet text
        card_names = re.findall(r"\[\[(.*?)\]\]", latest_tweet.text)

        # Check if any card names were found
        if len(card_names) > 0:
            # Set the API endpoint
            endpoint = "https://api.scryfall.com/cards/named"

            # Create an empty list to store the image data
            image_data = []

            # Iterate over the first four card names
            for card_name in card_names[:4]:
                # Make a GET request to the endpoint, passing the card name as a query parameter
                response = requests.get(endpoint, params={"fuzzy": card_name})

                # Check if the request was successful
                if response.status_code == 200:
                    # Parse the JSON response
                    data = response.json()

                    # Extract the card image URL from the response
                    image_url = data["image_uris"]["normal"]

                    # Download the image
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        # Save the image to memory
                        image_data.append(response.content)

            # Check if any images were downloaded
            if len(image_data) > 0:
                # Create an image object from the first image
                image = Image.open(io.BytesIO(image_data[0]))

                # Iterate over the remaining images
                for img in image_data[1:]:
                    # Open the image
                    img = Image.open(io.BytesIO(img))

                    # Paste the image onto the existing image
                    image.paste(img, (0, 0), img)

                # Save the combined image to memory
                image_bytes = io.BytesIO()
                image.save(image_bytes, "JPEG")
                image_bytes.seek(0)

                # Post the image to Twitter
                client.PostUpdate("Here are the cards you requested!", media=image_bytes)

    # Sleep for the specified interval
    time.sleep(poll_interval)


