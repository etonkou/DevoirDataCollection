import random

from .utils import Utils
import requests
from bs4 import BeautifulSoup


PATH_URL = 'cours/cours-des-devises-contre-Franc-CFA-appliquer-aux-transferts'
URL = f'https://www.bceao.int/fr/{PATH_URL}'

class DeviseFactory(object):
    @classmethod
    def httpFetcher(cls, URL):
        with requests.Session() as session:
            result = session.get(URL)
            result = result.text
            return result

    @classmethod
    def scrapLink(cls, URL):
        return cls.httpFetcher(URL)

    @classmethod
    def souper(cls, URL):
        result = cls.scrapLink(URL)
        return BeautifulSoup(
            result,
            'html.parser')

    @classmethod
    def getBoxCourse(cls, URL=URL):
        soupering = cls.souper(URL)
        soupering = soupering \
            .find_all(attrs={
                'id': 'box_cours'})
        if soupering:
            table = soupering[0].table
            return table
        return None

    @classmethod
    def makeCurrencyList(cls, URL=URL):
        soupering = cls.getBoxCourse(URL)
        if soupering:
            tr = soupering.find_all('tr')
            factory = [
                item.find_all('td')
                for item in tr
            ][1:]
            factory = [
                {
                    'Devise': x.string.strip(),
                    'Achat': float(y.string.strip().replace(',', '.')),
                    'Vente': float(z.string.strip().replace(',', '.')),
                }
                for (x, y, z) in factory
            ]
            return factory
        return None

    @classmethod
    def save(cls, URL=URL, format=None):
        soupering = cls.makeCurrencyList(URL)
        if soupering:
            return soupering
        return None

    # Retourne la valeur en XAF/XOF de la devise choisi au hasard
    @classmethod
    def deviseValue(cls,data, deviseAuChoix):
        i = 0
        for _ in data:
            if data[i]['Devise'] == deviseAuChoix:
                valeur = data[i]['Vente']
                break
            i = i + 1
        return valeur

    # Attribue de maniere aleatoire les devices (Euro, Dollar, Yen)
    # j'affiche la devise attribue et sa conversion en XOF a la fin de la liste
    @classmethod
    def randomChoice(cls,data):
        devise = ['Euro','Dollar us','Yen japonais']
        randomDevise = random.choice(devise)

        deviseDict = {}
        deviseDict['randomDevise'] = randomDevise
        deviseDict['XOF'] = cls.deviseValue(data,randomDevise)
        data.append(deviseDict)
        return data


    @classmethod
    def main(cls):
        data = cls.makeCurrencyList()
        data = cls.randomChoice(data) # affiche la donnee avec la nouvelle devise choisi au hasard
        return data