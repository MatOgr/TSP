// Generator_losowych.cpp : Ten plik zawiera funkcję „main”. W nim rozpoczyna się i kończy wykonywanie programu.
//

#include "pch.h"
#include <iostream>
#include <vector>
#include <fstream>

using namespace std;

void generator()
{
	ofstream plik("D:/Uczelnia/Python Projects/TSP/Graf.txt", ios::trunc);
	int i = 0, j, tab[500][3];
	bool ok = false;
	for (i; i < 500; i++)
	{
		cout << "\ngeberowanie";
		tab[i][0] = i + 1;
		tab[i][1] = rand() % 1000;
		tab[i][2] = rand() % 1000;
		while (!ok && i > 0)
		{
			for (j = 0; j < i; j++)
			{
				cout << "\nPowtorzenia";
				if (tab[j][1] == tab[i][1] && tab[j][2] == tab[i][2])
				{
					tab[i][1] = rand() % 1000;
					ok = false;
					break;
				}
				ok = true;
			}
		}

		cout << tab[i][0] <<
			'\t' << tab[i][1] << '\t'
			<< tab[i][2] << endl;

		plik << tab[i][0] <<
			' ' << tab[i][1] << ' '
			<< tab[i][2] << endl;
	}
	
	plik.close();
}

int main()
{
	generator();

	return 0;
}

// Uruchomienie programu: Ctrl + F5 lub menu Debugowanie > Uruchom bez debugowania
// Debugowanie programu: F5 lub menu Debugowanie > Rozpocznij debugowanie

// Porady dotyczące rozpoczynania pracy:
//   1. Użyj okna Eksploratora rozwiązań, aby dodać pliki i zarządzać nimi
//   2. Użyj okna programu Team Explorer, aby nawiązać połączenie z kontrolą źródła
//   3. Użyj okna Dane wyjściowe, aby sprawdzić dane wyjściowe kompilacji i inne komunikaty
//   4. Użyj okna Lista błędów, aby zobaczyć błędy
//   5. Wybierz pozycję Projekt > Dodaj tab element, aby utworzyć nowe pliki kodu, lub wybierz pozycję Projekt > Dodaj istniejący element, aby dodać istniejące pliku kodu do projektu
//   6. Aby w przyszłości ponownie otworzyć ten projekt, przejdź do pozycji Plik > Otwórz > Projekt i wybierz plik sln
