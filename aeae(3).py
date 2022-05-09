import pandas as pd
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium.webdriver.common.by import By



headers = {
    'authority': 'scrapeme.live',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}  # this is use to tell zomato website from which source or which user is accessing their website because zomato use secure network

driver = webdriver.Chrome(
    executable_path=r"E:\codec and ineuron\ineuron classes\web scrapping\zomato\chromedriver.exe")  # this is selenium driver which is use to automate the website
driver.get(
    "https://www.zomato.com/hyderabad")  # zomato URL for getting data
time.sleep(2)  # time dealy for wait to open website
scroll_pause_time = 3  # scroll time  by which zomato website auto scroll after each 3 second
screen_height = driver.execute_script("return window.screen.height;")  # this is use to define screen height
i = 1

while True:  # run a loop until website reach end of the page

    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height,
                                                                            i=i))  # its execute scroll positions
    i += 1
    time.sleep(scroll_pause_time)

    scroll_height = driver.execute_script("return document.body.scrollHeight;")

    if (screen_height) * i > scroll_height:
        break  # when website reach end of the page then while loop break

soup = BeautifulSoup(driver.page_source, "html.parser")  # this is use to get the data from the page open above
divs1 = soup.findAll('div',
                    class_='sc-1mo3ldo-0')  # this is a class in zomato website. by this class we get div html tag. under this tag all required data is listed

divs=divs1[4:]
print(len(divs1))
print(len(divs1[4:]))
# create arr to store data for further use
urls = []
rest_name = []
ratings = []
addresses = []
price = []
crusine = []
data=pd.DataFrame()
# run a loop until we found child div tag. in these child div tag we get data from each restaurant

for parent in divs:
    try:
        isCom=True
        # print(parent)
        try:
            if "Inspiration for your first order" in parent.find("h3").text:
                print("no need first")
                isCom = False
        except Exception as e:
            print("")
            # pass
        try:
            if "Best Food in" in parent.find("h1").text:
                print("no need best")
                isCom = False
        except Exception as e:
            print("")
            # pass
        try:
            if "Top brands for" in parent.find("h3").text:
                print("no need top")
                isCom = False
        except Exception as e:
            print("")
            # pass
        try:
            if "End of search results" in parent.find("h3").text:
                print("no need end")
                isCom = False
                break
        except Exception as e:
            print("")
            # break
        if isCom:

            # name_tag = parent.find("h4")  # this h4 is a html tag. we use this to get name of restaurant
            # #
            # rest_name.append(name_tag.text)  # add name in array

            divas = parent.findAll('div',class_='jumbo-tracker')
            print(len(divas))
            i =0
            for par in divas:

                print(i)
                i=i+1
                link_tag = par.find("a")  # here we get link of that restaurant of zomato page

                base = "https://www.zomato.com"

                if 'href' in link_tag.attrs:
                    link = link_tag.get('href')

                url = urljoin(base, link)  # not we join base zomato link & restaurant link and add in url array
                urls.append(url)
                print(url)

                rating_tag = par.div.a.next_sibling.div.div.div.div.div.div.div.text
                price_tag = par.div.a.next_sibling.p.next_sibling.text
                crusine_tag = par.div.a.next_sibling.p.text
                # print(name_tag.text)
                # print(rating_tag)
                # print(price_tag)
                # print(crusine_tag)
                ratings.append(rating_tag)
                # addresses.append(address[2].te
                price.append(price_tag)
                crusine.append(crusine_tag)

                driver.get(url)
                time.sleep(3)
                soup = BeautifulSoup(driver.page_source, "html.parser")  # this is use to get the data from the page open above
                # divsas = soup.findAll('div', class_='sc-1mo3ldo-0')
                # sectionMenu=soup.findAll('section')
                # print(sectionMenu)

                cuisine_name = []
                priceL = []
                description = []
                rest_namea = []
                rest_namea.append(soup.select('h1.sc-7kepeu-0')[-1].text)
                rest_name.append(soup.select('h1.sc-7kepeu-0')[-1].text)
                for h in soup.find_all('h4', class_="sc-1s0saks-15 iSmBPS"):
                    cuisine_name.append(h.text)

                rest_namea = rest_namea * len(cuisine_name)

                for h1 in soup.find_all('span', class_="sc-17hyc2s-1 cCiQWA"):
                    priceL.append(h1.text)

                for h2 in soup.find_all('p', class_="sc-1s0saks-12 hcROsL"):
                    description.append(h2.text)

                if data.empty:
                    data = pd.DataFrame(zip(rest_namea, cuisine_name, priceL, description))
                else:
                    data1 = pd.DataFrame(zip(rest_namea, cuisine_name, priceL, description))
                    data = data.append(data1, ignore_index=True)

                data.to_csv('Zomata_menu2.csv', index=False)

                # for aa in divsas:
                    # rest_name.append(aa.section.next_sibling.next_sibling.h1.text)
                    # print(aa.section.next_sibling.next_sibling.div.div.div.section.div.div.div.div.div.text)

                addresses.append(soup.findAll('a', class_='sc-cmTdod')[0].text)


    except Exception as e:
        print(e)
        pass

        # print(soup.findAll('section', class_='sc-iTlrqL'))
        # print(aa.section.next_sibling.next_sibling.next_sibling)


#
# for div in divs:
#     rating_tag = div.div.a.next_sibling.div.div.div.div.div.div.div.text
#     price_tag = div.div.a.next_sibling.p.next_sibling.text
#     crusine_tag = div.div.a.next_sibling.p.text
#     # address = div.div.a.next_sibling.findAll('p', class_='sc-1hez2tp-0')
#     # print(address[2].text)
#     ratings.append(rating_tag)
#     # addresses.append(address[2].text)
#     price.append(price_tag)
#     crusine.append(crusine_tag)

print(len(urls))
print(len(rest_name))
print(len(addresses))
print(len(ratings))
print(len(price))
print(len(crusine))
#
out_df2 = pd.DataFrame(
    {'links': urls, 'names': rest_name, 'address': addresses, 'ratings': ratings, 'price for two': price,
     'crusine': crusine})  # we create csv data

out_df2.to_csv("restaurants_Main.csv")  # save csv data in  file
driver.close()
#
# zomato = pd.read_csv('restaurants_Main.csv')
# zomato.to_json (r'restaurants.json')
