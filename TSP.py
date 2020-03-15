import random
import math


from ACO import Graf, ACO




def _losowanie(rozmiar: int):
    wierzcholki = []
    macierzDrog = []
    #id = 1
    ok = False
    for i in range(rozmiar):
        wierzcholki.append(dict(index=i + 1, x=random.randint(0, 300), y=random.randint(0, 150)))
        while not ok and i > 0:
            for j in range(i):
                if wierzcholki[j]['x'] == wierzcholki[i]['x'] and wierzcholki[j]['y'] == wierzcholki[i]['y']:
                    print("Powtorzenie")



def _odleglosc(wierzcholek1: dict, wierzcholek2: dict):
    return math.sqrt((wierzcholek1['x'] - wierzcholek2['x']) ** 2 + (wierzcholek2['y'] - wierzcholek1['y']) ** 2)



def _zachlanny(graf: Graf):
    nieodwiedzone = [True for i in range(graf.Rozmiar)]
    jeszcze_nie = True
    rozwiazanie = []
    aktualny = random.randint(0, graf.Rozmiar)
    droga = 0.0
    while jeszcze_nie:
        id = -1
        min = float('inf')
        for i in range(graf.Rozmiar):
            if nieodwiedzone[i] and graf.DlugosciDrog[aktualny][i] < min:
                min = graf.DlugosciDrog[aktualny][i]
                id = i
        droga += min
        nieodwiedzone[id] = False
        rozwiazanie.append(id+1)
        aktualny = id
        if len(rozwiazanie) == graf.Rozmiar:
            jeszcze_nie = False
    droga += graf.DlugosciDrog[aktualny][0]
    print('Droga: {}\nKoszt: {}'.format(rozwiazanie, droga))





def main():
    wierzcholki = []
    macierzDrog = []

    # # #           Otwarcie pliku

    # f = open('D:/Uczelnia/Python Projects/TSP/Graf.txt')
    try:
        with open('D:/Uczelnia/Python Projects/TSP/Graf.txt') as f:
            for linia in f:
                pom = linia.split()
                wierzcholki.append(dict(index=int(pom[0]), x=float(pom[1]), y=float(pom[2])))
    finally:
        f.close()

    for i in range(len(wierzcholki)):
        print(wierzcholki[i])
    print('\n')

    # # #           Obliczanie drog

    rozmiarGrafu = len(wierzcholki)
    for i in range(rozmiarGrafu):
        zMiasta_i = []
        for j in range(rozmiarGrafu):
            zMiasta_i.append(_odleglosc(wierzcholki[i], wierzcholki[j]))
        macierzDrog.append(zMiasta_i)
        #print(zMiasta_i)


    # # #          Tworzenie obiektu ACO i wykonywanie programu

    aco = ACO(800, 5, 2.0, 5.8, 0.8, 1.0, 1)
    graf = Graf(macierzDrog, rozmiarGrafu, wierzcholki)
    #start = datetime.datetime.now()
    for ile in range(0, 3):
        aco._dzialaj(graf)
    #for ile in range(3):
     #   _zachlanny(graf)






if __name__ == '__main__':
    main()