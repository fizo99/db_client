12. Klient bazy danych     
Opis zadania    
-  Program udający klienta bazy danych, pozwalający na utworzenie/usunięcie tabeli, dodawanie/usuwanie wpisów w niej, oraz wyszukanie danych. 
-  Możliwe utworzenie tabeli o dowolnej liczbie kolumn, każda kolumna zawierająca dane typu liczba calkowitaalbo liczba rzeczywista albo tekst. 
-  Typ liczba calkowitapozwala na przechowywanie liczb całkowitych (pythonowy int). 
-  Typ liczba rzeczywista pozwala na przechowywanie liczb rzeczywistych (pythonowy float). 
-  Typ tekst pozwala na przechowywanie dowolnego tekstu (domyślny typ tekstowy pythona). 
-  Nazwy tabel i kolumn nie mogą być puste (muszą zawierać przynajmniej jeden znak drukowalny). 
-  Główne okno powinno powinno posiadać listę tabel znajdujących się w bazie danych, listę wpisów w zaznaczonej tabeli (lista lub dowolny czytelnysposób prezentacji danych), oraz przyciski "Dodaj tabelę", "Usuń tabelę", "Dodaj wiersz", "Usuń wiersz" i 'Wyszukaj w tabeli". 
-  Okno dodawania tabeli powinno pozwalać na wpisanie nazwy tabeli oraz dodanie kolumn (nazwa i typ). 
-  Okno dodawania wiersza powinno wyświetlać nazwy kolumn i pola tekstowe służące wpisaniu danych.
-  Walidacja typów wpisanych danych powinna odbywać się przy próbie dodania wiersza (np. Jeśli pole tekstowe kolumny typu liczba całkowita zawiera tekst nie rzutujący się na liczbę całkowitą, to powinien zostać wyświetlony błąd - okienko, znacznik na polu tekstowym lub inne). 
-  Przed usunięciem tabeli/wiersza użytkownik powinien być proszony o potwierdzenie. 
  
  
**Ponadto interfejs projektu ma być napisany za pomocą html/css i javascript**

**Testy oraz opis zadania mogą ulec późniejszej zmianie.**

Testy   
1. Utworzenie tabeli "testi" z kolumnami riczbową "ID" (typ int), dwoma tekstowymi "imię" oraz "nazwisko" oraz liczbową "wzrost" (typ &ml). 
2. Dodanie wiersza do tabeli "testi" z danymi "1", "Roch", "Przyłbipięt", "1.50" -oczekiwane powodzenie. 
3. Dodanie wiersza do tabeli "testi" z danymi "2", "Ziemniaczysław", "Bulwiasty", "1.91" - oczekiwane powodzenie. 
4. Dodanie wiersza do tabeli "testi" z danymi "cztery", "bla", "bla", "-90" - oczekiwane niepowodzenie (dane tekstowe w polu liczbowym). 
5. Dodanie wiersza do tabeli "testi" z danymi "3.14", "pi", "ludolfina", "314e-2" -oczekiwane niepowodzenie (liczba rzeczywista w kolumnie z liczbę całkowitą). 
6. Wyświetlenie zawartości tabeli "testi". 
7. Dodanie trzech kolejnych wierszy do tabeli "testi" i usunięcie dwóch wierszy z niej (pierwszego i środkowego), w obu przypadkach najpierw anulowanie operacji, a potem jej akceptacja. 
8. Utworzenie tabeli "test2" z kolumnami "reserved" typu string oraz "kolor" typu liczba całkowita. 
9. Dodanie wiersza do tabeli "test2" z danymi (puste pole), "1337" -oczekiwane powodzenie. 
10. Dodanie wiersza do tabeli "test2" z danymi "bla", "1939b" - oczekiwane niepowodzenie (tekst w polu typu liczba całkowita). 
11. Usunięcie tabeli "test2", najpierw anulowanie operacji, a potem jej akceptacja. 
12. Próba utworzenia tabeli bez nazwy -oczekiwane niepowodzenie. 
13. Próba utworzenia tabeli o nazwie " " (spacja) - oczekiwane niepowodzenie. 
14. Próba utworzenia tabeli z kolumną bez nazwy - oczekiwane niepowodzenie. 
15. Próba utworzenia tabeli z kolumną o nazwie " (cztery spacje) - oczekiwane niepowodzenie, 
16. Wypełnij tabelę "testi" danymi testowymi (kolejne wartości "ID, 'wzrost" między 1.0 i 2.0) wyszukaj wiersze dla których "wzrost" ma wartość podaną przez prowadzącego oraz "ID" jest liczbą parzystą lub nieparzystą (zależnie od woli prowadzącego). 
