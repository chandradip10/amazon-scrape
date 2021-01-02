import pip._vendor.requests
from pip._vendor import requests
from bs4 import BeautifulSoup
import smtplib
import csv
import datetime
import os
import time

URL ='https://www.amazon.in/Logitech-Hero-Gaming-Mouse-Black/dp/B07GBZ4Q68/ref=sr_1_20_sspa?dchild=1&keywords=gaming+mouse&qid=1609568727&sr=8-20-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFYNkYzQ0I2S1hXOVAmZW5jcnlwdGVkSWQ9QTAxOTE2NTgxSDQxR1VTN1ZPRkNHJmVuY3J5cHRlZEFkSWQ9QTAxNjgzMTIxSUw3QlMwTkgxMlZSJndpZGdldE5hbWU9c3BfYnRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=='

headers ={"User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

def check_price():
    page = requests.get(URL,headers=headers)

    soup = BeautifulSoup(page.content,'html.parser')

    title = soup.find(id="productTitle").get_text()
    price = soup.find(id="priceblock_ourprice").get_text()
    converted_price = float(price[2:10].replace(',',''))

    file_exists = True

    if not os.path.exists("./price.csv"):
        file_exists = False

    with open("price.csv","a") as file:
        writer = csv.writer(file,lineterminator ="\n")
        fields = ["Timestamp","price"]
        
        if not file_exists:
            writer.writerow(fields)

        timestamp = f"{datetime.datetime.date(datetime.datetime.now())},{datetime.datetime.time(datetime.datetime.now())}"
        writer.writerow([timestamp, converted_price])
        print("wrote csv data")

        print(title.strip())
        print(converted_price)

    return converted_price


def send_mail():
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('dippanja100@gmail.com','nplyybhqnufzfsfg')

    subject = 'Price fell down .'
    body = 'Check the link https://www.amazon.in/Logitech-Hero-Gaming-Mouse-Black/dp/B07GBZ4Q68/ref=sr_1_2_sspa?dchild=1&keywords=gaming+mouse&qid=1609227964&smid=A14CZOWI0VEHLG&sr=8-2-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzUk84STY5QVZPWkhHJmVuY3J5cHRlZElkPUEwNzk3NDQwMUlQR0U4SVVLNTVVMiZlbmNyeXB0ZWRBZElkPUEwNzQxNzQ3MTdFUlVWSkJWRkpEMSZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU='
    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'dippanja100@gmail.com',
        'chandradippanja10@gmail.com',
        msg
    )

    print('Hey email has been sent !!!!')

    server.quit()


while True:
    price = check_price()
    if(price <= 4000):
        send_mail()
        break
    time.sleep(43200)


