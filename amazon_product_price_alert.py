import requests
import re
import smtplib
from bs4 import BeautifulSoup as bs
import time
from notify_run import Notify
from datetime import datetime
import html5lib
headers = { "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36" }
def send_email():
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("***********","*********")
    subject = "Price Drop Alert !!!"
    body = "Hey **********!! \n The price of ******** decreased below your described price..."
    msg = f"Subject: {subject} \n\n {body}"
    server.sendmail("***************","****************",msg)
    print("Mail has been sent...")
    server.quit()
def push_notification():
    notify = Notify()
    notify.send("Hey ****** price just got decreased...")
    print("Notification sent...")
def get_url(org_url):
    dp = re.findall(r'/dp/\S+\?',org_url)
    dp = dp[0]
    if dp[::-1] != '/':
        dp = dp[:dp.rfind("/")+1]
    cust_url = "https://www.amazon.in"+dp[:len(dp)-1]
    return cust_url
def get_curr_price(url):
    try:
        r = requests.get(url,headers = headers)
        soup = bs(r.content,'html5lib')
        title = soup.find(id="productTitle").get_text().strip()
        curr_price = soup.find(id="priceblock_ourprice")
        if curr_price is None:
            curr_price = soup.find(id="priceblock_dealprice")
        curr_price = curr_price.get_text().strip()[2:].replace(",","")
        curr_price = float(curr_price)
        return curr_price
    except:
        return -1
def check_price(URL,des_price):
    URL = get_url(URL)
    curr_price = get_curr_price(URL)
    if curr_price == -1:
        print("Product dosen't exist or is currently unavailable...")
    else:
        if curr_price <= des_price:
            print("You can now buy the product for ",curr_price,". Hurry up!! ")
            send_email()
            push_notification()
        else:
            print("Current price is",curr_price-des_price,"higher than desired price")

count = 0
if __name__ == "__main__":
    URL = input("Enter the product url: ")
    des_price = float(input("Enter the desired price: "))
    while True:
        count += 1
        print("Count : ",str(count),", Checking at : ",datetime.now())
        check_price(URL,des_price)
        print("Rechecking...")
        time.sleep(3600)

    




