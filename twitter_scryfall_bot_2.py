"""
## Telegram Scryfall Bot

This script was generated playing with https://chat.openai.com/chat, and it might not be functional, but it seems to me it is. The functionality was not achieved up to a 100%, because now it broke when asking for a polling mechanism. 


> 15 minutes

### Prompts: 
- Hi! Do you know Scryfall API?
- I want to build an app written in Python, based on the Scryfall API. Using the "twitter" client library in Python, to send the image of a given card from a cited tweet responding to the user with the given image. Could you propose me an example?
- I think the python library is called scrython, so the import should be that one.
- Nice, instead of using the general tweet search, I want to use the mention thread!
- Yes! Could you please also modify the example to look for cards using this rule: if the card name is surrounded by double brackets, such as [[Lightning bolt]], it should parsed and used as the name of the card. Also, the search of the card, should use the parameter fuzzy.
- Please, do not join the card names matches, but instead iterate over them and only take the first one
- Could the example use the four first images, upload them to twitter as media, and then use the attribute "media_ids" in the PostUpdate function to create a tweet with the four first card images?
- Could you break the example into functions? For example: a function called "process_tweet" which takes the tweet as the input and performs all the pipeline, which depends on a function called "scryfall_to_twitter" which downloads an image given a card object and uploads it to Twitter. 


"""

import twitter
import scrython
import re

# Replace these values with your API keys and access tokens
api_key = "your_api_key"
api_secret_key = "your_api_secret_key"
access_token = "your_access_token"
access_token_secret = "your_access_token_secret"

# Authenticate your app
api = twitter.Api(consumer_key=api_key,
                  consumer_secret=api_secret_key,
                  access_token_key=access_token,
                  access_token_secret=access_token_secret)

def process_tweet(tweet):
    """Process a tweet and respond with the card images.

    Args:
        tweet: The tweet to process.

    Returns:
        None
    """
    # Use a regular expression to find card names surrounded by double brackets
    card_names = re.findall(r"\[\[(.*?)\]\]", tweet.text)

    # If the tweet contains one or more card names, search for the cards
    if len(card_names) > 0:
        # Use the Scryfall API to search for the first card by name
        # Enable fuzzy search to match similar card names
        cards = scrython.cards.search(q=card_names[0], fuzzy=True)

        # If the cards were found, upload their images to Twitter
        if len(cards) > 0:
            # Upload the first four card images to Twitter
            media_ids = [scryfall_to_twitter(card) for card in cards[:4]]

            # Tweet the card images as a reply to the original tweet
            reply_text = "@" + tweet.user.screen_name + " Here are the cards you requested:\n"
            api.PostUpdate(status=reply_text, media_ids=media_ids)

def scryfall_to_twitter(card):
    """Download an image from Scryfall and upload it to Twitter.

    Args:
        card: The Scryfall card object.

    Returns:
        The media ID of the uploaded image on Twitter.
    """
    # Download the card image from Scryfall
    image_url = card.image_uris["large"]
    image_data = requests.get(image_url).content

    # Upload the image to Twitter and return the media ID
    return api.UploadMediaSimple(media=image_data)


# Get the most recent tweets that mention your app's Twitter account
results = api.GetMentions(count=100)

# Process each tweet and respond with the card images
for tweet in results:
    process_tweet(tweet)

