# import re
# import pandas as pd
# import os

# mail = "stawy-mowic-0e@icloud.com"

# mail = mail[:-11]

# def nameSurname():
#     parts = re.split('[-._]', mail)
    
#     sorted_words = sorted(parts, key=len, reverse=True)
    
#     name = sorted_words[0]
#     lastname = sorted_words[1]
#     toCSV(name.capitalize(), lastname.capitalize(), mail)



# def toCSV(name, lastname, mail):
#     file = "accounts.csv"
#     if not os.path.isfile(file):
#     # Utworzenie nowego DataFrame z nagłówkami
#         df = pd.DataFrame(columns=['NAME', 'LASTNAME', 'EMAIL'])
        
#         # Zapisanie DataFrame do pliku CSV
#         df.to_csv(file, index=False)
    
#     df = pd.DataFrame
    
    
#     df = pd.DataFrame({'NAME': [name],
#         'SURNAME': [lastname],
#         'EMAIL': [mail+"@icloud.com"]})
    
#     df.to_csv('accounts.csv', index=False,header=False, mode='a')

# nameSurname()

# import time

# from time import gmtime, strftime

# import datetime
# from datetime import datetime

# c = datetime.now()    
# # current_time = c.strftime('%H:%M:%S')
from playwright.sync_api import sync_playwright, Playwright
import time
import random
import json
import pandas as pd
import string
from time import gmtime, strftime
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime
import re
import os
        
# print(c)
with open("./settings.json", 'r', encoding='utf-8') as plik:
    settings = json.load(plik)

def webhook_execute(email):
    webhook = DiscordWebhook(url=settings["Webhook"])
    
    embed = DiscordEmbed(title="ICloud Browser Based", color="0a401c")
    embed.set_thumbnail(url="https://help.apple.com/assets/622BDFD810622B2B9C0BD80A/622BDFDA10622B2B9C0BD82D/de_DE/dc4bdf1973030717f16d02d3e44e3793.png")

    embed.add_embed_field(name="Email", value=f"||{email}"+ "@gmail.com"+"||")
    embed.add_embed_field(name="Generated", value=":white_check_mark:")

    embed.set_footer(text="Meow Gen")
    embed.set_timestamp()

    webhook.add_embed(embed)

    response = webhook.execute(remove_embeds=True)


webhook_execute("mikolaj.stanco")