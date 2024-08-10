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

with open("./settings.json", 'r', encoding='utf-8') as plik:
    settings = json.load(plik)

def webhook_execute(email):
    webhook = DiscordWebhook(url=settings["Webhook"])
    
    embed = DiscordEmbed(title="ICloud Browser Based", color="0a401c")
    embed.set_thumbnail(url="https://help.apple.com/assets/622BDFD810622B2B9C0BD80A/622BDFDA10622B2B9C0BD82D/de_DE/dc4bdf1973030717f16d02d3e44e3793.png")

    embed.add_embed_field(name="Email", value=f"||{email}"+ "@icloud.com"+"||")
    embed.add_embed_field(name="Generated", value=":white_check_mark:")

    embed.set_footer(text="Meow Gen")
    embed.set_timestamp()

    webhook.add_embed(embed)

    response = webhook.execute(remove_embeds=True)


def remove_digits(text):
    return re.sub(r'\d+', '', text)

def nameSurname(mail):
    mail = mail[:-11]
    parts = re.split('[-._]', mail)
    
    sorted_words = sorted(parts, key=len, reverse=True)
    try:
        name = sorted_words[0]
        lastname = sorted_words[1]
    except:
        name = sorted_words[0]
        lastname = "None"
        

    
    name = remove_digits(name)
    lastname = remove_digits(lastname)
    
    toCSV(name.capitalize(), lastname.capitalize(), mail)
    webhook_execute(mail)

def actualtime():
    c = datetime.now()    
    current_time = c.strftime('%H:%M:%S')
    return current_time

def toCSV(name, lastname, mail):
    file = "accounts.csv"
    if not os.path.isfile(file):
        df = pd.DataFrame(columns=['NAME', 'LASTNAME', 'EMAIL'])
        df.to_csv(file, index=False)
    
    df = pd.DataFrame
    
    
    df = pd.DataFrame({'NAME': [name],
        'SURNAME': [lastname],
        'EMAIL': [mail+"@icloud.com"]})
    
    df.to_csv('accounts.csv', index=False,header=False, mode='a')
    

def login():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        page.goto("https://www.icloud.com/")
        
        
        
        print("[" + actualtime() +  "]" , " [ICloud]", "Press Enter after completed login")

        a = input("")
        context.storage_state(path="session.json")
        print("[" + actualtime() +  "]" , "[ICloud]", "Session Created")
        browser.close()
        
        
def errorHandling(page):
    page
    result = page.evaluate("""document.querySelector("#form-textbox-1722015576438-0_error")""")
    print(result)
    if result is None:
        return False
    else:
        return True
  
    
def openloggedin():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="session.json")
        page = context.new_page() 
        # page.goto("https://www.icloud.com/")
        # time.sleep(2)
        page.goto("https://www.icloud.com/icloudplus/")
        time.sleep(3)
        page.locator("xpath=//*[@id='root']/ui-main-pane/div/div[2]/div/div/main/div/div[3]/div/div[1]/article/div/button").click()
        time.sleep(3)
        
        frame = page.frame_locator("iframe[data-name='hidemyemail']")
        frame.get_by_role("button", name="Dodaj").click()
        time.sleep(3)
        mail = frame.locator("xpath=//*[@id='router-nav-container']/div/div[2]/div[1]/div").text_content()
        print("[" + actualtime() +  "]" , "[ICloud]", f"[{mail}]", "Generated E-Email")
        
        text_inputs = frame.locator('//input[@type="text"]').element_handles()
        text_inputs[0].fill("Meowek")
        print("[" + actualtime() +  "]" , "[ICloud]", f"[{mail}]", "Data Filled")
        frame.locator("xpath=//*[@id='app-modal']/div/div[2]/fieldset/div/div[2]/button").click()
        time.sleep(4)
        #error
        try:
            error = frame.locator('xpath=//div[@class="form-message-wrapper"]').text_content()
            if len(error) > 1:
                errno = True
            else:
                errno = False
        except:
            errno = False   
        
        while errno == True:
            print("[" + actualtime() +  "]" , "[ICloud]", f"[{mail}]", "Max accounts Generation reached, waiting additional time")
            time.sleep(720) 
            frame.locator("xpath=//*[@id='app-modal']/div/div[2]/fieldset/div/div[2]/button").click() 
            time.sleep(4)
            try:
                error = frame.locator('xpath=//div[@class="form-message-wrapper"]').text_content()
                if len(error) > 1:
                    errno = True
                else:
                    errno = False
            except:
                errno = False 
        time.sleep(2) 
        nameSurname(mail)
        print("[" + actualtime() +  "]" , "[ICloud]", f"[{mail}]", "Task Finished")
        print("[" + actualtime() +  "]" , "[ICloud]", f"[{mail}]", "Sleeping for 12 minutes")
        browser.close()
        
        
        
def main():

    # login()
    # time.sleep(5)
    while True:
        openloggedin()
        time.sleep(720)
        
main()



#all divs:
# divs = page.query_selector_all("div.Typography.searchable-card-subtitle.Typography-body2")