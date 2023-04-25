import requests
import time
import os.path
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as BS
num_listings=[]
price_list=[]
plt.ion()
path = 'C:/Users/wilme/Desktop'
listings_file = "listings.txt"
price_file = "price.txt"
compl_name_list =os.path.join(path, listings_file)  #Set file path and name
compl_name_price =os.path.join(path, price_file)
figure, ax1 = plt.subplots(figsize=(8,6))
ax1.set_facecolor('xkcd:cement')
ax2 = ax1.twinx()
URL = "https://steamcommunity.com/market/search?appid=730&q=Fracture+Case"
f = open(compl_name_list,"r")
h = open(compl_name_price, "r")

data_listings = f.read() #Reads data form file
temp_listings = data_listings.split(" ") #Cleanup
temp_listings.remove("")

data_price = h.read() 
temp_price = data_price.split(" ")
temp_price.remove("")

for x in temp_listings: #loads in saved data into working list
    x = float(x)  
    num_listings.append(x)

for x in temp_price:
    x = float(x)
    price_list.append(x)

while True:
    measurements=[]
    page = requests.get(URL)
    soup = BS(page.content, "html.parser")
    #Listingsdata scrape
    num_listing = (soup.find("div",class_="market_listing_right_cell market_listing_num_listings").find("span", class_="market_listing_num_listings_qty"))
    num_listing = [d.text for d in num_listing]
    num_listing = float(num_listing[0].replace(",", "."))
    num_listings.append(num_listing)

    #Pricedata scrape
    price = (soup.find("div",class_="market_listing_right_cell market_listing_their_price").find("span", class_="normal_price"))
    price = [d.text for d in price]
    price = price[3]
    price = price.replace("$","") #Cleanup
    price = price.replace(" ","")
    price = price.replace("USD","")
    price = float(price)
    price_list.append(price)

    f = open("listings.txt","wt")
    for item in num_listings:
        f.write(' ' + str(item))  #Write contents of list separated by space
    f.close()

    f = open("price.txt","wt")
    for item in price_list:
        f.write(' ' + str(item))
    f.close()

    for g in range(0,len(num_listings)): #Create list for use in x-axis in chart
        measurements.append(g)
    line1, = ax1.plot(measurements, num_listings, 'b')  #Create two lines
    line2, = ax2.plot(measurements, price_list,'r')

    figure.canvas.draw()
    figure.canvas.flush_events()
    time.sleep(60)

    plt.plot(measurements, price_list)
    plt.show()