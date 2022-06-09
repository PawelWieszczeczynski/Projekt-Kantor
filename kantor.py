import requests


class Pieniadz:     # klasa pieniądz, odpowiadająca za przechowywanie danej ilości pieniędzy w danej walucie
    def __init__(self, waluta, ilosc):
        self.waluta = waluta
        self.ilosc = ilosc

    def __str__(self):  # metoda pozwalająca zapisać instancję klasy jako String w formacie [Symbol]: [Ilość]
        return self.waluta + ": " + str(round(self.ilosc, 2))


class Konto:        # klasa Konto, przechowująca imie, nazwisko, login oraz hasło przypisane do konta
    def __init__(self, *args):          # konstruktor klasy
        if len(args) == 1:              # 1 wersja konstruktora, tworząca instancję klasy kiedy przekazana jest
            line = args[0].split()      # tylko linijka odczytana z pliku konta.txt
            self.imie = line[11]        # linijka jest konwertowana na tablicę i odpowiednim polom są przypisane
            self.nazwisko = line[12]    # odpowiednie wartości
            self.login = line[13]
            self.haslo = line[14]
            self.portfel = [            # tworzenie pustego portfela
                Pieniadz("PLN", 0.0),   # PLN
                Pieniadz("EUR", 0.0),   # EUR
                Pieniadz("USD", 0.0),   # USD
                Pieniadz("GBP", 0.0),   # GBP
                Pieniadz("CHF", 0.0),   # CHF
                Pieniadz("CAD", 0.0),   # CAD
                Pieniadz("AUD", 0.0),   # AUD
                Pieniadz("CZK", 0.0),   # CZK
                Pieniadz("SEK", 0.0),   # SEK
                Pieniadz("NOK", 0.0),   # NOK
                Pieniadz("DKK", 0.0),   # DKK
            ]
            for x in range(0, 11):                          # wczytywanie do portfela pieniędzy z
                self.portfel[x].ilosc = float(line[x])      # przekazanej w parametrach linijki
        else:
            self.imie = args[0]             # druga wersja kontruktora
            self.nazwisko = args[1]         # kiedy przekazane są imie, nazwisko, login oraz haslo
            self.login = args[2]
            self.haslo = args[3]
            self.portfel = [                # tworzony jest wtedy pusty portfel dla nowego użytkownika
                Pieniadz("PLN", 0.0),
                Pieniadz("EUR", 0.0),
                Pieniadz("USD", 0.0),
                Pieniadz("GBP", 0.0),
                Pieniadz("CHF", 0.0),
                Pieniadz("CAD", 0.0),
                Pieniadz("AUD", 0.0),
                Pieniadz("CZK", 0.0),
                Pieniadz("SEK", 0.0),
                Pieniadz("NOK", 0.0),
                Pieniadz("DKK", 0.0),
            ]

    def __str__(self):          # reprezentacja kont jako String w formacie [I] [N] [L] [H]
        return self.imie + " " + self.nazwisko + " " + self.login + " " + self.haslo
                                # wykorzystywane przy zapisywaniu kont do pliku

class Kurs:             # klasa Kurs przechowywująca kursy w kantorze składają się na nią symbol waluty bazowej
    def __init__(self, *args):          # symbol waluty kwotowanej oraz cena jako float
        if len(args) == 1:              # pierwsza wersja kontruktora, która tworzy instancję kursu
            line = args[0].split()      # kiedy przekazana jest tylko linijka z pliku kursy.txt
            self.walutaBaz = line[0]    # konwertujemy linijkę na tablicę (dzieląc na spacjach)
            self.walutaKwot = line[1]   # i przypisujemy do odpowiednich pól
            self.cena = float(line[2])
        else:
            self.walutaBaz = args[0]    # druga wersja konstruktora, tworząca instancję po przekazaniu
            self.walutaKwot = args[1]   # obu walut oraz ceny
            self.cena = round(args[2], 4)

    def __str__(self):          # reprezentacja kursu jako String w formacie [WB]/[WK] - [Cena]
        return self.walutaBaz + "/" + self.walutaKwot + " - " + str(self.cena)


class Kantor:       # klasa odpowiedzialna za cały kantor
    konta = []      # pola klasy, tablica kont do której wczytywane są konta
    kursy = []      # tablica kursów, do której są wczytywane kursy
    konto = Konto("", "", "", "")       # aktualnie zalogowane konto, przed zalogowaniem "puste" konto
                                        # po to żeby Label w GUI działały bez problemu
    def loadKonta(self):
        with open("konta.txt", encoding="utf-8") as f:  # metoda ładująca konta do tablicy konta
            read_data = f.read()            # odczyt z pliku konta
        f.close()
        read_data = read_data.splitlines()      # podział na linie
        for x in read_data:                 # każda linia jest przekazywana do konstruktora klasy Konto
            self.konta.append(Konto(x))     # i stworzona instancja jest dodawana do tablicy

    def loadKursy(self):                # metoda ładująca kursy do tablicy
        with open("kursy.txt", encoding="utf-8") as f:
            read_data = f.read()
        f.close()                                   # analogicznie jak w przypadku kont
        read_data = read_data.splitlines()
        for x in read_data:
            self.kursy.append(Kurs(x))

    def saveKonta(self):                # metoda zapisująca konta do pliku
        with open("konta.txt", "w", encoding="utf-8") as f:
            for x in self.konta:            # plik jest czyszczony przez argument "w" w metodzie open
                line = ""                   # tworzona jest nowa linijka
                for y in x.portfel:     # dodawane są po kolei kwoty w portfelu
                    line = line + str(y.ilosc) + " "       # oraz rozdzielająca spacja
                line = line + str(x) + "\n"     # oraz po wszystkich kwotach reprezentacja konta w Stringu
                f.write(line)               # (metoda __str__ z klasy konta) oraz wpisywane do pliku

    def saveKursy(self):                # metoda zapisująca konta do pliku
        with open("kursy.txt", "w", encoding="utf-8") as f:
            for x in self.kursy:            # analogicznie jak w przypadku kont
                line = x.walutaBaz + " " + x.walutaKwot + " " + str(x.cena) + "\n"
                f.write(line)

    def refreshKursy(self):        #metoda odświeżająca kursy za pomocą API "ExchangeRate-API"
        url = "https://v6.exchangerate-api.com/v6/26863ccb2f04ce30ef458354/latest/PLN"
        response = requests.get(url)    # ^URL potrzebne do pobrania danych z API
        data = response.json()          # pobranie danych i konwersja na słownik
        for x in self.kursy:            # cena każdego kursu jest aktualizowana poprzez znalezienie w słowniku
            x.cena = round(1 / data["conversion_rates"][x.walutaBaz], 4)    #listy kursów oraz odpowiedniego kursu
        self.saveKursy()        # cena jest odwrotnością ponieważ API zwraca kursy np. PLN/EUR, PLN/GBP, a potrzebne
        # zapis do pliku metodą opisaną wyżej                 są kursy EUR/PLN, GBP/PLN (wystarczy odwrotność kursu)
    def register(self, imie, nazwisko, login, haslo):
        for x in self.konta:        # metoda rejestrująca nowe konta
            if x.login == login:    # sprawdzamy czy login nie znajduje się już w tabeli kont
                return False        # jeśli tak zwracamy False aby później GUI wiedziało co się stało
        self.konta.append(Konto(imie, nazwisko, login, haslo))  # jeśli nie ma takiego loginu dodajemy
        self.saveKonta()            # nowe konto do tabeli kont i zapisujemy
        return True                 # zwracamy True żeby GUI wiedziało że pomyślnie zapisano

    def login(self, login, haslo):  # metoda odpowiadająca za logowanie
        for x in self.konta:
            if x.login == login and x.haslo == haslo:       # sprawdzamy czy login i hasło któregoś konta
                self.konto = x          # pasuje do podanych, jeśli tak pole konto kantoru jest ustawiane na
                return True             # konto którego dane zostały podane i zwracane jest True dla GUI
        return False                # jeśli żadne dane nie pasują, zwracany jest False dla GUI

    def logout(self):               # metoda odpowiadająca za wylogowanie
        self.konto = None           # usuwamy konto z pola konto w kantorze
        self.saveKonta()            # i zapisujemy ewentualne zmiany w portfelu

    def znajdzKurs(self, WalutaBaz, walutaSprz):           # metoda znajdująca wymagany kurs
        kurs = None                 # kurs który będzie zwracany
        if WalutaBaz == "PLN" or walutaSprz == "PLN":       # jeśli jedną z walut jest PLN to szukamy
            for x in self.kursy:            # jednego kursu
                if x.walutaBaz == WalutaBaz and x.walutaKwot == walutaSprz: # jeśli potrzebny jest kurs XXX/PLN
                    kurs = x            # to jest znajdywany oraz zwracany ten kurs
                    break
                if x.walutaBaz == walutaSprz and x.walutaKwot == WalutaBaz:     # a jeśli potrzebny jest kurs PLN/XXX
                    kurs = Kurs(x.walutaKwot, x.walutaBaz, round(1 / x.cena, 4))
                    break               # szukamy kursu XXX/PLN i odwracamy (analogicznie jak przy aktualizowaniu)
        else:
            kurs1 = None    # kiedy danego kursu (np. XX1/XX2) nie ma w bazie, potrzebny jest kurs krzyżowy,
            kurs2 = None    # dlatego szukamy dwóch kursów XX1/PLN i XX2/PLN
            for x in self.kursy:        # szukamy w liście kursów obu kursów
                if x.walutaBaz == WalutaBaz:
                    kurs1 = x           # kurs którego walutę chcemy kupić/sprzedać jest zapisywany jako 1
                if x.walutaBaz == walutaSprz:
                    kurs2 = x           # kurs waluty którą chcemy płacić/otrzymać jest zapisywany jako 2
            if kurs1 is not None and kurs2 is not None:
                kurs = Kurs(            # jeśli kursy są znalezione, tworzymy nowy kurs, walutą bazową jest XX1
                    kurs1.walutaBaz, kurs2.walutaBaz, round(kurs1.cena / kurs2.cena, 4)
                )                       # walutą kwotowaną jest XX2, a cena to cena kursu 1 podzielona przez cenę
        return kurs                     # kursu drugiego (kursy krzyżowe), zwracamy stworzony lub znaleziony kurs

    def transakcja(self, czyKupno, kurs, ilosc):    # metoda odpowiadająca za transakcję
        if czyKupno:    #czyKupno odpowiada za to czy jest to transakcja kupna czy sprzedaży
            for x in self.konto.portfel:    # szukamy w portfelu odpowiednich walut
                if x.waluta == kurs.walutaKwot and x.ilosc >= kurs.cena * ilosc: # najpierw szukamy waluty którą
                    x.ilosc = round(x.ilosc - kurs.cena * ilosc, 2)       # płacimy, i odpowiednia kwota jest
                    for y in self.konto.portfel:          # odejmowana, nastepnie szukamky drugiej waluty
                        if y.waluta == kurs.walutaBaz:                  # i dodajemy odpowiednią kwotę
                            y.ilosc = round(y.ilosc + ilosc, 2)         # jeśli wszystko się udało
                            return True     # (była odpowiednia ilosć pieniędzy), zwracamy True dla GUI
        else:
            for x in self.konto.portfel:
                if x.waluta == kurs.walutaBaz and x.ilosc >= ilosc:
                    x.ilosc = round(x.ilosc - ilosc, 2)
                    for y in self.konto.portfel:    # analogiczna sytuacja, tylko odejmujemy ilość którą sprzedajemy
                        if y.waluta == kurs.walutaKwot:
                            y.ilosc = round(y.ilosc + kurs.cena * ilosc, 2)
                            return True
        return False        # zwracamy False, jeśli np. zabrakło środków

    def wplata(self, waluta, ilosc):    # metoda wpłacająca odpowiednią ilość pieniędzy danej waluty
        for x in self.konto.portfel:
            if x.waluta == waluta:
                x.ilosc = round(x.ilosc + ilosc, 2)

    def wyplata(self, waluta, ilosc):   # metoda odpowiadająca za wyplate srodkow
        for x in self.konto.portfel:
            if x.waluta == waluta:      # sprawdzamy czy jest odpowiednia ilosc na koncie i jesli tak, wyplacamy
                if x.ilosc >= ilosc:
                    x.ilosc = round(x.ilosc - ilosc, 2)
                    return True         # jesli wyplata sie powiodla zwracamy True, jesli nie False dla GUI
                else:
                    return False

    def przeliczPortfel(self, waluta):  # metoda odpowiedzialna za przeliczanie wszystkich pieniedzy na jedna walute
        suma = 0.0  # suma do ktorej beda dodawane poszczegolne kwoty
        for x in self.konto.portfel:    # wszystkie pieniadze z portfela przeliczamy na jedna walute
            if x.waluta != waluta:  # jesli waluta z pętli jest inna niż ta na która przeliczamy
                suma = suma + self.znajdzKurs(x.waluta, waluta).cena * x.ilosc  # szukamy odpowiedniego kursu i mnozymy
            else:                   # razy ilosc danej waluty
                suma = suma + x.ilosc   # jesli np. przeliczamy na GBP i z pętli jest teraz wybrane GBP to po prostu
        return suma                  # dodajemy, po przejsciu petli zwracamy sumę