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
import sys
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

def nameSurname(mail, file):
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
    
    toCSV(name.capitalize(), lastname.capitalize(), mail, file)

    if file == "accounts.csv":
        webhook_execute(mail)

def actualtime():
    c = datetime.now()    
    current_time = c.strftime('%H:%M:%S')
    return current_time

def toCSV(name, lastname, mail, file):
    # if mode == "generating":
    #     file = "accounts.csv"
    # elif mode == "allgeneratedmails":
    #     file = "iCloudAllGeneratedMails.csv"
    
    if not os.path.isfile(file):
        df = pd.DataFrame(columns=['NAME', 'LASTNAME', 'EMAIL'])
        df.to_csv(file, index=False)
    
    df = pd.DataFrame
    
    df = pd.DataFrame({'NAME': [name],
        'SURNAME': [lastname],
        'EMAIL': [mail+"@icloud.com"]})
    
    df.to_csv(file, index=False,header=False, mode='a')
    
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
     
def collectAllGeneratedMails():   
    print("[" + actualtime() +  "]" , "[ICloud] Collecting Generated Mails Started")    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state="session.json")
        page = context.new_page() 
        page.goto("https://www.icloud.com/icloudplus/")
        time.sleep(3)
        page.locator("xpath=//*[@id='root']/ui-main-pane/div/div[2]/div/div/main/div/div[3]/div/div[1]/article/div/button").click()
        time.sleep(3)
        
        frame = page.frame_locator("iframe[data-name='hidemyemail']")
        divs = frame.locator('xpath=//span[@class="Typography searchable-card-subtitle Typography-body2"]').element_handles()
        
        for div in divs:
            nameSurname(div.text_content(), "iCloudAllGeneratedMails.csv")
    
        browser.close()    
   
def generating():
    counter = 0
    print("[" + actualtime() +  "]" , "[ICloud] Generation started")
    while (counter <750):
        print(counter)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                context = browser.new_context(storage_state="session.json", locale="us-US")
                page = context.new_page() 
            except:
                print("[" + actualtime() +  "]" , "[ICloud] Session Error - Generation Aborted - [ENTER] to continue")
                input()
                sys.exit(1)

            page.goto("https://www.icloud.com/icloudplus/")
            time.sleep(3)
            
            #otwiera Hide My Mail frame
            page.locator("xpath=//*[@id='root']/ui-main-pane/div/div[2]/div/div/main/div/div[3]/div/div[1]/article/div/button").click()
            time.sleep(3)
            
            #lokalizuje Hide My Mail frame
            frame = page.frame_locator("iframe[data-name='hidemyemail']")
            #counter ilości zrobionych maili - jeżeli nie znajduje oznacza że żadne mail nie został jeszcze wykonany 
            counter = frame.locator("xpath=//*[@id='router-nav-container']/div/div[2]/section[1]/div/div/div[1]/h2")
            if counter.count() > 0:
                #znalazł ilość zrobionych maili - łuskanie wymaganej wartości - przerabanie na int
                counter = int(counter.text_content().split()[0])
                #lokalizuje i klika plus/dodaj noweg maila
                frame.get_by_role("button", name="Add").click()
                time.sleep(1)
                
            else:   
                #żaden mail nie został jeszcze wykonany więc wartość counter to 0,
                counter = 0
                
                #lokalizuje i klika dodaj noweg maila
                frame.locator("xpath=//*[@id='router-nav-container']/div/div[2]/section/div/div/div/div[1]/div/div[1]/h3").click()
                time.sleep(1)
            
            #lokalizuje i zapisuje do zmiennej *mail wygenerowany adres email
            mail = frame.locator("xpath=//*[@id='router-nav-container']/div/div[2]/div[1]").text_content()
            

            #TODO - Zmiana na US odpowiednik
            if "WczytywanieGeneruję" in mail:
                time.sleep(10)
                mail = frame.locator("xpath=//*[@id='router-nav-container']/div/div[2]/div[1]").text_content()
            
            
            #oznaczenie wykonania zdarzenia - generated Email
            print("[" + actualtime() +  "]" , "[ICloud]" ,f"[{counter + 1}]", f"[{mail}]", "Generated Email")
            time.sleep(1.5)
            
            #lokalizuje i wypełnia "oznacznie" maila - pole wymagane
            text_inputs = frame.locator('//input[@type="text"]').element_handles()
            text_inputs[0].fill("Meowek")
            
            #oznaczenie wykonania zdarzenia - data filled
            print("[" + actualtime() +  "]" , "[ICloud]",f"[{counter + 1}]", f"[{mail}]", "Data Filled")
            time.sleep(1.5)
            
            #lokalizuje i klika przycisk "Utwórz adres email"
            frame.locator("xpath=//*[@id='app-modal']/div/div[2]/fieldset/div/div[2]/button").click()

            time.sleep(3)
        
            #error grabber
            locator = frame.locator('xpath=//div[@class="form-message-wrapper"]')

            if locator.count() > 0:
                errno = len(locator.text_content()) > 1
            else:
                errno = False
            
            while errno == True:
                print("[" + actualtime() +  "]" , "[ICloud]",f"[{counter + 1}]", f"[{mail}]", "Max accounts Generation reached, waiting additional time")
                time.sleep(720) 
                frame.locator("xpath=//*[@id='app-modal']/div/div[2]/fieldset/div/div[2]/button").click() 
                time.sleep(4)
                locator = frame.locator('xpath=//div[@class="form-message-wrapper"]')

                if locator.count() > 0:
                    errno = len(locator.text_content()) > 1
                else:
                    errno = False

            time.sleep(2) 
            nameSurname(mail, "accounts.csv")
            print("[" + actualtime() +  "]" , "[ICloud]",f"[{counter + 1}]", f"[{mail}]", "Task Finished")
            print("[" + actualtime() +  "]" , "[ICloud]",f"[{counter + 1}]", f"[{mail}]", "Sleeping for 12 minutes")
            browser.close()
        time.sleep(720)

def main():
    
    #TODO deleteAllMails()
    #TODO openAccount()
    #TODO login()
    # collectAllGeneratedMails()
    generating()
    # login()

        
main()