import random
import datetime


class Graf(object):
    def __init__(self, macierzDrog: list, rozmiarGrafu: int, wierzcholki: dict):
        """

        :param macierzDrog:
        :param rank:
        """
        self.DlugosciDrog = macierzDrog
        self.Rozmiar = rozmiarGrafu
        self.Feromon = [[1.0 / (rozmiarGrafu * rozmiarGrafu) for j in range(rozmiarGrafu)] for i in range(rozmiarGrafu)]

        self.Wierzcholki = wierzcholki




class ACO(object):
    def __init__(self, liczbaMrowek: int, generacje: int, alfa: float, beta: float, ro: float, nasycenie: int, strategia: int):
        """

        :param liczbaMrowek:
        :param generacje:
        :param alfa: wpływ feromonu na wybor drogi
        :param beta: wplyw informacji widocznych(krotsza droga)
        :param ro: poziom zanikania feromonow
        :param nasycenie:
        :param strategia:
        """

        self.Nasycenie = nasycenie
        self.LiczbaMrowek = liczbaMrowek
        self.Pokolenia = generacje
        self.Alfa = alfa
        self.Beta = beta
        self.Ro = ro
        self.Schemat = strategia        # # #       Moze jednak nie trzeba


    def _aktualizacja_feromonow(self, graf: Graf, mrowki: list):
        for i, rzad in enumerate(graf.Feromon):
            for j, kolumna in enumerate(rzad):
                graf.Feromon[i][j] *= self.Ro
                for mrowka in mrowki:
                    graf.Feromon[i][j] += mrowka.FeromonyDelta[i][j]



    # noinspection PyProtectedMember
    def _dzialaj(self, graf: Graf):

        start = datetime.datetime.now()
        drogaKoszt = float('inf')
        rozwiazanie = []
        for pok in range(self.Pokolenia):
            mrowki = [Mrowka(self, graf, i) for i in range(self.LiczbaMrowek)]
            for mrowka in mrowki:               # WYPUSZCZAMY MROWKE
                #print('Mrowka: ', mrowka.ID)
                for i in range(graf.Rozmiar-1):       # MROWKA TRWORZY LISTE ODWIEDZONYCH WIERZCHOLKOW
                    mrowka._nastepny()
                mrowka.KosztCalkowity += graf.DlugosciDrog[mrowka.Odwiedzone[-1]][mrowka.Odwiedzone[0]]
                if mrowka.KosztCalkowity < drogaKoszt:
                    drogaKoszt = mrowka.KosztCalkowity
                    rozwiazanie = [] + mrowka.Odwiedzone
                    print("najlepszy koszt: {} \nnajlepsza sciezka: {} \nczas: {}".format(drogaKoszt, rozwiazanie, (datetime.datetime.now() - start).seconds))
                mrowka._aktualizacja_feromonu_d()
            self._aktualizacja_feromonow(graf, mrowki)

        # # # Sprawdzenie drogi
        droga = 0.0
        for i in range(1, graf.Rozmiar):
            droga += graf.DlugosciDrog[rozwiazanie[i - 1]][rozwiazanie[i]]
        droga += graf.DlugosciDrog[rozwiazanie[-1]][rozwiazanie[0]]
        print(droga, len(rozwiazanie), '\n')

        # # # Wypisanie drogi
        for i in range(graf.Rozmiar):   rozwiazanie[i] = graf.Wierzcholki[rozwiazanie[i]]['index']
#        rozwiazanie.remove(rozwiazanie.index(0))
        print('koszt: {}, sciezka: {}'.format(drogaKoszt, rozwiazanie))
        print((datetime.datetime.now() - start).seconds, 'sekund \n\n\n')





class Mrowka(object):
    def __init__(self, aco: ACO, graf: Graf, id: int):
        self.ID = id
        self.Kolonia = aco
        self.Graf = graf
        self.KosztCalkowity = 0.0
        self.Odwiedzone = []
        self.Nieodwiedzone = [True for i in range(graf.Rozmiar)]
        self.FeromonyDelta = []
        poczatek = random.randint(0, graf.Rozmiar - 1)
        self.Odwiedzone.append(poczatek)
        self.ObecnyWierzcholek = poczatek
        self.Nieodwiedzone[poczatek] = False

    def _nastepny(self):
        calkowite_prawdobodobienstwo = 0.0
        wybrany = 0
        prawdopodobienstwa = [0.0 for i in range(self.Graf.Rozmiar)]
        for i in range(self.Graf.Rozmiar):
            if self.Nieodwiedzone[i]:
                try:
                    prawdopodobienstwa[i] = pow(self.Graf.Feromon[self.ObecnyWierzcholek][i], self.Kolonia.Alfa) * \
                                                pow(1.0 / self.Graf.DlugosciDrog[self.ObecnyWierzcholek][i], self.Kolonia.Beta) #       TUTAJ ZMIENIALEM
                    calkowite_prawdobodobienstwo += prawdopodobienstwa[i]
                except ZeroDivisionError:
                    pass

        if calkowite_prawdobodobienstwo > 0.0:
            los = random.uniform(0.0, calkowite_prawdobodobienstwo)
            for i in range(self.Graf.Rozmiar):
                if self.Nieodwiedzone[i]:
                    los -= prawdopodobienstwa[i]
                    if los < 0.0:
                        wybrany = i
                        break




        self.Nieodwiedzone[wybrany] = False
        self.Odwiedzone.append(wybrany)
        self.KosztCalkowity += self.Graf.DlugosciDrog[self.ObecnyWierzcholek][wybrany]
        self.ObecnyWierzcholek = wybrany
        #print(wybrany)


    def _aktualizacja_feromonu_d(self):
        self.FeromonyDelta = [[0 for j in range(self.Graf.Rozmiar)] for i in range(self.Graf.Rozmiar)]
        for c in range(1, len(self.Odwiedzone)):
            i = self.Odwiedzone[c - 1]
            j = self.Odwiedzone[c]
            if self.Kolonia.Schemat == 1:       # system jakosciowy
                self.FeromonyDelta[i][j] = self.Kolonia.Nasycenie
            elif self.Kolonia.Schemat == 2 and self.Graf.DlugosciDrog[i][j]:     # system ilosciowy
                self.FeromonyDelta[i][j] = self.Kolonia.Nasycenie / self.Graf.DlugosciDrog[i][j]
            else:                               # system cyklowy
                self.FeromonyDelta[i][j] = self.Kolonia.Nasycenie / self.KosztCalkowity
