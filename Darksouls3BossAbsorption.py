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

del dlc2bosses[3]
data = {"Boss": [],
        "Standard" : [],
        "Strike" : [],
        "Slash" : [],
        "Thrust" : [],
        "Magic" : [],
        "Fire" : [],
        "Lightning" : [],
        "Dark" : [],
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
        row = pageSoup.find("h3", class_="titlearea").previousSibling.previousSibling.find_all("tr")
        abs = pageSoup.find_all("a", title="Absorption")
        row = []
        for i in abs:
            if i.text == "absorption":
                del i
            elif link == "/Dancer_of_the_Boreal_Valley" or len(data["Boss"]) == 27:
                row.append(i.parent.parent)
            else:
                row.append(i.parent.parent.parent)
        if len(row)>1:
            for i in range(0,len(row)):
                makeRow(row[i],pageSoup,boss=True)
        else:
            makeRow(row[0],pageSoup)
        time.sleep(1)

def makeRow(row,page,boss = False):
        percent = row.find_all("td")
        i = 0
        for key in data:
            if key == "Boss":
                if boss == False:
                    data[key].append(page.find("h2").text.strip("\n"))
                else:
                    if  percent[i].text.strip("\n").strip("Absorptions") != "":
                        data[key].append(percent[i].text.strip("\n").strip("Absorptions"))
                    else:
                        data[key].append(percent[i].parent.parent.parent.parent.findPrevious("h3").text.strip("\n").split("Stats")[0])
            else: 
                data[key].append(percent[i].text.strip("\n"))
            i +=1

def darkeaterMidir():
    urlResponse = requests.get(url+"/Darkeater_Midir",headers = headers)
    midirSoup = BeautifulSoup(urlResponse.content, "html.parser")
    midirRows = midirSoup.find("h3", class_="titlearea").find_previous("table").find_all("tr")
    data["Boss"].append("Midirs Body")
    data["Boss"].append("Midirs Head")
    for i in range(1,len(midirRows)):
        midirnumber = midirRows[i].find_all("td")
        key = midirnumber[0].text.strip("\n")
        
        if key == "Physical":
            key = "Standard"
        for j in range(2,len(midirnumber)):

            data[key].append(midirnumber[j].text.strip("\n"))

dlc2bosses.insert(2,dlc2table.find("a", href = "/Demon_Prince"))

addBosses(baseGameBosses)
addBosses(dlc1bosses)
addBosses(dlc2bosses)
darkeaterMidir()

# for key in data:
#     if key == "Boss":
#         data[key].append("Average")
#     else:
#         average = 0
#         for i in data[key]:
#             j = int(i.strip("%"))
#             average += j
#         data[key].append(str(round(average/len(data[key]),2))+"%")

df = pd.DataFrame(data)
df.index += 1
df.index.name = "#"
filename = "DarkSouls3BossInfo.csv"
with open(filename,"a+") as f:
    f.seek(0,2)
    f.write("\nAbsorption Values\n")
    df.to_csv(f, header = True)





 
x = np.linspace(0,len(data["Boss"]),len(data["Boss"]))
for key in data:
    y = []
    if key != "Boss":
        for i in data[key]:
            y.append((int(i.strip("%"))))
        y = np.array(y)
        slope, intercept = np.polyfit(x,y,1)
        plt.scatter(x,y)
        plt.plot(x,x*slope+intercept,label = key,)
plt.legend()
plt.grid()
plt.show()

# for i in list.find_all("li"):
#     link = i.find("a")
#     print(link)
#     url = urljoin(url, link["href"])
#     urlResponse = requests.get(url, headers={"User-Agent" : "mozilla/5.0"})
#     pageSoup = BeautifulSoup(urlResponse.content, "html.parser")
#     pageHeader = pageSoup.find("h1")
#     print(pageHeader.text)
#     time.sleep(1) 