class m_detail():
    detail={}
    timeoup=""
    def __init__(self):
        return None
    def detail_verify(self,details,timeoup):
        self.detail=details
        self.timeoup=timeoup
        lst=[]
        lst.append(details['ID'])
        if 'Oferta od' in self.detail.keys():
            lst.append(self.detail['Oferta od'])
        else:
            lst.append("empty")
        if 'Kategoria' in self.detail.keys():
            lst.append(self.detail['Kategoria'])
        else:
            lst.append("empty")
        if 'Marka pojazdu' in self.detail.keys():
            lst.append(self.detail['Marka pojazdu'])
        else:
            lst.append("empty")
        if 'Model pojazdu' in self.detail.keys():
            lst.append(self.detail['Model pojazdu'])
        else:
            lst.append("empty")
        if 'Wersja' in self.detail.keys():
            lst.append(self.detail['Wersja'])
        else:
            lst.append("empty")
        if 'Generacja' in self.detail.keys():
            lst.append(self.detail['Generacja'])
        else:
            lst.append("empty")
        if 'Rok produkcji' in self.detail.keys():
            lst.append(details['Rok produkcji'])
        else:
            lst.append("empty")
        if 'Przebieg' in self.detail.keys():
            lst.append(self.detail['Przebieg'])
        else:
            lst.append("empty")
        if 'Pojemność skokowa' in self.detail.keys():
            lst.append(self.detail['Pojemność skokowa'])
        else:
            lst.append("empty")
        if 'Rodzaj paliwa' in self.detail.keys():
            lst.append(self.detail['Rodzaj paliwa'])
        else:
            lst.append("empty")
        if 'Moc' in self.detail.keys():
            lst.append(self.detail['Moc'])
        else:
            lst.append("empty")
        if 'Skrzynia biegów' in self.detail.keys():
            lst.append(self.detail['Skrzynia biegów'])
        else:
            lst.append("empty")
        if 'Napęd' in self.detail.keys():
            lst.append(self.detail['Napęd'])
        else:
            lst.append("empty")
        if 'Uszkodzony' in self.detail.keys():
            lst.append(self.detail['Uszkodzony'])
        else:
            lst.append("empty")
        if 'Typ' in self.detail.keys():
            lst.append(self.detail['Typ'])
        else:
            lst.append("empty")
        if 'Liczba drzwi' in self.detail.keys():
            lst.append(self.detail['Liczba drzwi'])
        else:
            lst.append("empty")
        if 'Liczba miejsc' in self.detail.keys():
            lst.append(self.detail['Liczba miejsc'])
        else:
            lst.append("empty")
        if 'Kolor' in self.detail.keys():
            lst.append(self.detail['Kolor'])
        else:
            lst.append("empty")
        if 'Metalik' in self.detail.keys():
            lst.append(self.detail['Metalik'])
        else:
            lst.append("empty")
        if 'Możliwość finansowania' in self.detail.keys():
            lst.append(self.detail['Możliwość finansowania'])
        else:
            lst.append("empty")
        if 'Kraj pochodzenia' in self.detail.keys():
            lst.append(self.detail['Kraj pochodzenia'])
        else:
            lst.append("empty")
        if 'Pierwsza rejestracja' in self.detail.keys():
            lst.append(self.detail['Pierwsza rejestracja'])
        else:
            lst.append("empty")
        if 'Zarejestrowany w Polsce' in self.detail.keys():
            lst.append(self.detail['Zarejestrowany w Polsce'])
        else:
            lst.append("empty")
        if 'Numer rejestracyjny pojazdu' in self.detail.keys():
            lst.append(self.detail['Numer rejestracyjny pojazdu'])
        else:
            lst.append("empty")
        if 'Pierwszy właściciel' in self.detail.keys():
            lst.append(self.detail['Pierwszy właściciel'])
        else:
            lst.append("empty")
        if 'Serwisowany w ASO' in self.detail.keys():
            lst.append(self.detail['Serwisowany w ASO'])
        else:
            lst.append("empty")
        if 'Stan' in self.detail.keys():
            lst.append(self.detail['Stan'])
        else:
            lst.append("empty")
        lst.append(self.timeoup)

        return lst
#det={'ID':2123123,}

#print(m_detail().detail_verify(det))