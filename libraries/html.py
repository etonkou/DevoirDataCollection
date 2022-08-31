from .utils import Utils
import json
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = '../../COURSE/DATABASES/data-zIybdmYZoV4QSwgZkFtaB.html'


# BASE_URL = 'COURSE/DATABASES/data-zIybdmYZoV4QSwgZkFtaB.html'


class HtmlFactory(object):
    @classmethod
    def openFile(cls):
        with open(BASE_URL) as file:
            data = file.read()
            data = BeautifulSoup(data,'html.parser')
            file.close()
        return data

    @classmethod
    def getRows(cls):
        data = cls.openFile()
        rows = data.find_all('tr')
        return rows[1:]

    @classmethod
    def getRecord(cls):
        lines =[]
        data = cls.getRows()
        for line in data:
            datas = line.find_all('td')
            myRecord = {
                'Name':datas[0].getText(),
                'Phone':datas[1].getText(),
                'Email':datas[2].getText(),
                'LatLon':datas[3].getText(),
                'Salary':datas[4].getText(),
                'Age':datas[5].getText()
            }
            lines.append(myRecord)
        return lines

    @classmethod
    def triList(cls, data):
        i = 0
        listNom = []
        listPhone = []
        listEmail = []
        # listAdress = []
        listLatlng = []
        listSalary = []
        listAge = []

        for _ in data:
            listNom.append(data[i]['Name'])
            listPhone.append(data[i]['Phone'])
            # listPhone.append(data[i]['Phone'])
            listEmail.append(data[i]['Email'])
            listLatlng.append(data[i]['LatLon'])
            listSalary.append(float(data[i]['Salary']))
            listAge.append(int(data[i]['Age']))
            i = i + 1
        return listNom, listPhone, listEmail, listLatlng, listSalary, listAge


    # Affiche les donnees
    @classmethod
    def afficheDataFrame(cls,data):
        # Create multiple lists
        nom = data[0]
        phone = data[1]
        email = data[2]
        latlng = data[3]
        salary = data[4]
        age = data[5]

        columns = ['Nom', 'Phone', 'Email', 'Latlng', 'Salary', 'Age']
        # Create DataFrame from multiple lists
        df = pd.DataFrame(list(zip(nom, phone, email, latlng, salary, age)), columns=columns)

        df.to_csv("./outputHtmlFactory.csv")
        return df


    @classmethod
    def main(cls):
        data = cls.openFile()
        data = cls.getRows()
        data = cls.getRecord()
        data = cls.triList(data)
        data = cls.afficheDataFrame(data)
        return data

