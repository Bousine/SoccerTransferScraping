import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

playerlist = []
valuelist = []
yearlist = []
prevTeamList = []
nextTeamList = []

startyear = 1980
endyear = 2020

for year in range(startyear,endyear):
    print(year)
    prevPlayer0 = ""
    pageNum = 1
    notEnd = 1
    while True:
        #page = "https://www.transfermarkt.co.uk/transfers/transferrekorde/statistik/top/ajax/yw2/saison_id/" + str(year) + "/plus/0/galerie/0/page/" + str(pageNum)
        page = "https://www.transfermarkt.co.uk/transfers/transferrekorde/statistik?ajax=yw2&altersklasse=&ausrichtung=&land_id=0&leihe=&plus=1&saison_id="+str(year)+"&spielerposition_id=&w_s=&page="+str(pageNum)
        pageTree = requests.get(page, headers=headers)
        pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
        Players = pageSoup.find_all("a", {"class" : "spielprofil_tooltip"})
        comp1 = (str(prevPlayer0))
        comp2 = (str(Players[0].text))
        if comp1 == comp2:
            break
        prevPlayer0 = comp2

        Values = pageSoup.find_all("td", {"class": "rechts hauptlink"})
        TableCells = pageSoup.find_all("td", {"class": "hauptlink"})

        TeamNames = []
        for cell in TableCells:
            team = cell.find("a",{"class": "vereinprofil_tooltip"})
            if team is None:
                team = cell.find("a",{"title":"Unknown"})
                if team is None:
                    team = cell.find("a",{"title":"Career break"})
                    if team is None:
                        continue

            TeamNames.append(team.text)
        #print(len(TeamNames))
        #print(pageNum)
        #Teams = pageSoup.find_all("a", {"class": "vereinprofil_tooltip"})
        #Teams = [team for team in Teams if len(team.text)>0]
        PrevTeams = [team for (i,team) in enumerate(TeamNames) if i%2 == 0]
        NextTeams = [team for (i,team) in enumerate(TeamNames) if i%2 == 1]

        pagelen = len(Players)

        for i in range(pagelen):
            #print("left:",PrevTeams[i], "joined:",NextTeams[i])
            valueText = Values[i].text
            if 'loan'in valueText or 'Loan' in valueText:
                continue

            value = (valueText.strip(' £m'))
            if 'k' in value:
                value = float(value.strip('k'))
                value /= 1000

            playerlist.append(Players[i].text)
            valuelist.append(float(value))
            yearlist.append(year)
            prevTeamList.append(PrevTeams[i])
            nextTeamList.append(NextTeams[i])

        pageNum += 1

df = pd.DataFrame({"Year":yearlist,"Players":playerlist, "Left":prevTeamList, "Joined":nextTeamList, "Values":valuelist})
df.to_csv(r'TransferData.csv', index = False)
