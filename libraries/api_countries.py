import random

from .utils import Utils
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

URL = 'https://history.state.gov/countries/all'
BASE_URL = 'https://history.state.gov'

class CountriesFactory(object):

    @classmethod
    def fetch(cls, url: str):
        with requests.Session() as session:
            data = session.get(url)
        return data.text

    @classmethod
    def setBs4Instance(cls, url: str):
        data = BeautifulSoup(cls.fetch(url),features="html.parser")
        return data

    @classmethod
    def cleanByReplace(cls, string: str):
        string = str(string)
        regex = re.compile('/countries/\w+')
        string = re.findall(regex, string)
        return string[0]

    @classmethod
    def formUrlLink(cls, string: str):
        return f'{BASE_URL}{string}'

    @classmethod
    def getLinkList(cls, SoupList: list):
        return [
            cls.formUrlLink(
                cls.cleanByReplace(link))
            for link in SoupList
        ]

    @classmethod
    def getImgLink(cls, instanceBs4):
        try:
            flag = instanceBs4.find(class_='tei-graphic')['src']
        except TypeError:
            return "Flag non disponible"
        else:
            return flag


    @classmethod
    def scrapChildLinkList(cls, SoupUrlList: list):
        newList = []
        for link in SoupUrlList:
            data = cls.setBs4Instance(link)
            data = data.find(class_='tei-graphic')
            if data:
                newList.append(data['src'])
            continue
        return newList

    # Retourne la liste des pays dans une liste constituee de lien et une autre liste constituee de noms des pays
    @classmethod
    def listPays(cls):
        data = cls.setBs4Instance(URL)

        regex = re.compile('/countries/\w+')
        lista = data.find_all(href=regex) # recupere les liens de tous les pays
        lista = lista[2:-1] # les elts d'index 0 a 1 puis le dernier elt de la liste sont exclus
        pays = []  # la liste des nom des pays
        i = 0
        for x in lista:
            pays.append(lista[i].text.replace("*","")) # remplace le caractere '*' constate dans les noms de certains pays
            i= i+1
        return lista, pays

    # retourne les pays selectionnes au hasard avec les liens des flag correspondant
    @classmethod
    def paysFlag(cls):
        data = cls.listPays()
        pays = data[1]  # liste des pays
        lien = data[0]  # liste des liens des pays
        paysSelectedListDict = []
        paysSelected = []
        paysSelectedIndex = []
        flagSelected = []

        inputImg = []
        # on choisi 05 pays au hasard
        for _ in range(5):
            selected = random.choice(pays)
            paysSelectedDict = {}
            paysSelectedDict['pays'] = selected
            paysSelectedListDict.append(paysSelectedDict)
            indexSelected = pays.index(selected)

            paysSelected.append(selected) # List pays Selectionnes
            paysSelectedIndex.append(indexSelected)

            lienPaysSelected = [lien[indexSelected]]
            lienPaysSelected = cls.getLinkList(lienPaysSelected)
            paysSelectedDict['lien'] = lienPaysSelected


            var1 = cls.setBs4Instance(lienPaysSelected[0])
            inputImg.append(var1)

        i=0
        for x in inputImg:
            imgLogo = cls.getImgLink(x)
            #print('imgLogo', imgLogo)
            paysSelectedListDict[i]['flag'] = imgLogo
            #print(paysSelectedListDict[i])
            i=i+1

        return paysSelectedListDict

    @classmethod
    def affichage(cls, data):
        pays = []
        lien = []
        flag = []
        i = 0
        for _ in data:
            pays.append(data[i]['pays'])
            lien.append(data[i]['lien'][0])
            flag.append(data[i]['flag'])
            i = i+1

        columns = ['Pays', 'Lien', 'Flag']
        # Create DataFrame from multiple lists
        df = pd.DataFrame(list(zip(pays, lien, flag)), columns=columns)
        df.to_csv("./countries_api.csv")
        return df



    @classmethod
    def main(cls):
        data = cls.paysFlag()
        data = cls.affichage(data)

        return data