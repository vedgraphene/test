import bs4
import requests
import mysql.connector
from bs4 import BeautifulSoup
from time import sleep

#Connect to MySQL server
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="py",
  auth_plugin='mysql_native_password'
)

#Scrapes price from website
def parsePrice(strTick):
    r = requests.get("https://finance.yahoo.com/quote/"+strTick)
    soup = bs4.BeautifulSoup(r.text, "lxml")
    #Specific position/place where the price is on the website
    price = soup.find_all('div', {'class':'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
    return float(price.replace(',', '')) 


my = mydb.cursor()
#Query
my.execute("SELECT ticker, name, lowerbound, upperbound FROM stock")
ticker =  my.fetchall()
print("@ scraping.py")

for tick in ticker:
    print(tick[0])
    price = parsePrice(tick[0])
    mycursor = mydb.cursor()

    #Replaces values in databse with new values
    sql = "REPLACE INTO stock (ticker, name, price, lowerbound, upperbound) VALUES (%s, %s, %s, %s, %s)"
    val = (tick[0], tick[1], str(price), tick[2], tick[3])
    mycursor.execute(sql, val)


    mydb.commit()
