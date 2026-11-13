import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

url = "https://darksouls3.wiki.fextralife.com"
headers = {"User-Agent" : "mozilla/5.0"}
response = requests.get(url+"/bosses", headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

table = soup.find("table")
baseGameBosses = table.find_all("tr")
dlc1table = table.find_next_sibling("table")
dlc2table = dlc1table.find_next_sibling("table")
dlc1bosses = dlc1table.find_all("tr")
dlc2bosses = dlc2table.find_all("tr")

data = {"Boss": [],
        "NG": [],
        "NG+": [],
        "NG++": [],
        "NG+3": [],
        "NG+4": [],
        "NG+5": [],
        "NG+6": [],
        "NG+7": [],

}


def addBosses(table):
    global url
    for i in table[1:]:
        if i.find_all("td") == []:
            link = "/Demon_Prince"
        else:
            row = i.find_all("td")
            link = row[0].find("a")["href"]
        urlJoined = urljoin(url, link)
        urlResponse = requests.get(urlJoined,headers = headers)
        pageSoup = BeautifulSoup(urlResponse.content,"html.parser")
        row = pageSoup.find_all("table", class_="wikitable")
        for i in range(0,len(row)):
            if link == "/Deacons_of_the_Deep" or link == "/Dragonslayer_Armour":
                if i ==3:
                    makeRow(row[i].findAll("tr")[1],pageSoup)
            elif link == "/Demon_in_Pain_and_Demon_From_Below":
                if i == 1:
                    makeRow(row[i].findAll("tr")[1],pageSoup)
            elif i == 2:
                if len(row[i].findAll("tr")) > 2 and row[i].findAll("tr")[2].find("b").text != "Defense":
                    for j in range(1,len(row[i].findAll("tr"))):
                        makeRow(row[i].findAll("tr")[j],pageSoup,boss=True)
                else:
                    makeRow(row[i].findAll("tr")[1],pageSoup)
            elif link == "/Lothric,_Younger_Prince":
                if i == 4:
                    makeRow(row[i].findAll("tr")[1],pageSoup)
        # makeRow(row[0],pageSoup)
        # print(data)
        time.sleep(1)

def makeRow(row,page,boss = False):
        percent = row.find_all("td")
        
        i = 0
        for key in data:
            if key == "Boss":
                if boss == False:
                    data[key].append(page.find("h2").text.strip("\n"))
                else:
                    if percent[i].parent.parent.parent.parent.findPrevious("h3").text.strip("\n").split("Stats")[0] == "Nameless King & King of the Storm":
                        data[key].append(percent[i].find("b").text.strip("Health"))
                    else:
                        data[key].append(percent[i].parent.parent.parent.parent.findPrevious("h3").text.strip("\n").split("Stats")[0]+ percent[i].find("b").text.strip("Health"))
            else: 
                data[key].append(percent[i].text.strip("\n"))
            i +=1


# urlJoined = urljoin(url, "/Iudex_Gundyr")
# urlResponse = requests.get(urlJoined,headers = headers)
# pageSoup = BeautifulSoup(urlResponse.content,"html.parser")
# row = pageSoup.find_all("table", class_="wikitable")
# for i in range(0,len(row)):
#     if i ==2:
#         print(f"Hi{row[i]}\n")
# row = [row]
# makeRow(row[0],pageSoup)
dlc2bosses.insert(2,dlc2table.find("a", href = "/Demon_Prince"))
addBosses(baseGameBosses)
addBosses(dlc1bosses)
addBosses(dlc2bosses)

for i in range(0,len(data["Boss"])-1):
    if data["Boss"][i] == "Sister Friede Total ":
        j = i
        for key in data:
            del data[key][j]

df = pd.DataFrame(data)
df.index += 1
df.index.name = "#"
filename = "DarkSouls3BossInfo.csv"
with open(filename,"a+") as f:
    f.seek(0,2)
    f.write("\nHP Values\n")
    df.to_csv(f, header = True)

