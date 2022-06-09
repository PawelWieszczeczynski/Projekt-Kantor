import datetime
import tkinter as tk
from tkinter import messagebox as msb
from kantor import *

root = tk.Tk()      # główna instancja Tkintera
kantor = Kantor()       # instancja Kantoru odpowiedzialna za cały kantor
profileName = tk.StringVar()    # StringVariable używane do Label wyświetlającej aktualne konto
kantor.loadKursy()      # ładowanie kursów z pliku
kantor.loadKonta()      # ładowanie kont
root.title("Kantor wymiany walut")  # tytuł okienka         \/ lista walut w kantorze potrzebna do Option menu
waluty = ["PLN", "EUR", "USD", "GBP", "CHF", "CAD", "AUD", "CZK", "SEK", "NOK", "DKK"]

start_frame = tk.Frame(root)
login_frame = tk.Frame(root)
register_frame = tk.Frame(root)     # wszytkie Frame odpowiedzialne za poszczególne okna GUI
menu_frame = tk.Frame(root)
profile_frame = tk.Frame(root)
transaction_frame = tk.Frame(root)


def kantorQuit():       # metoda pytająca czy zamknąć aplikację, zapisująca konta i kursy do pliku
    if msb.askyesno("Potwierdzenie", "Czy na pewno chcesz zamknąć?"):
        kantor.saveKonta()
        kantor.saveKursy()
        root.quit()


def refreshPortfel():
    portfelLB.delete(0, tk.END)                 # (portfel w oknie profilu)
    for money in kantor.konto.portfel:
        portfelLB.insert(tk.END, str(money))        # metoda odświeżająca wartości w portfelu po transakcji
    portfelLBT.delete(0, tk.END)                # lub wpłacie/wypłacie pieniędzy
    for money in kantor.konto.portfel:
        portfelLBT.insert(tk.END, str(money))       # (portfel w oknie transakcji)


def checkFloat(val):
    try:                # metoda sprawdzająca czy input może być zamieniony na float
        float(val)
        return True
    except ValueError:
        return False


# ====================START_FRAME====================


def startLogin():       # metoda przełączająca z okna startowego na okno logowania
    login_frame.pack(fill="both", expand=1)     # odkrywamy okno logowania
    start_frame.forget()                        # chowamy okno startu (wiele razy, więc opisuję to tylko tutaj)


def startRegister():    # metoda przełączająca z okna startowego na okno rejestracji
    register_frame.pack(fill="both", expand=1)
    start_frame.forget()


labelStart = tk.Label(
    start_frame, text="Witaj w kantorze wymiany walut", font=("Calibri Bold", 40)
)                   # Label z powitaniem
labelStart.grid()   # umieszczenie Label w gridzie

labelWalutex = tk.Label(
    start_frame, text="WALUTEX", font=("Verdana Bold", 40), fg="blue"
)                   # Label z nazwą kantoru
labelWalutex.grid()

btnSL = tk.Button(start_frame, text="Logowanie", command=startLogin)
btnSL.grid()        # przycisk przełączający na okno logowania (metoda startLogin)

btnSR = tk.Button(start_frame, text="Rejestracja", command=startRegister)
btnSR.grid()        # przycisk przełączający na okno rejestracji (metoda startRegister)

btnSQ = tk.Button(start_frame, text="Wyjście", command=kantorQuit)
btnSQ.grid()        # przycisk zamykający aplikację (metoda kantorQuit


# ====================LOGIN_FRAME====================


def loginMenu():        # metoda odpowiedzialna za logowanie i przełączenie okna z okna logowania na okno menu
    if kantor.login(loginE.get(), passE.get()):      # sprawdzamy czy podany login i hasło są poprawne
        profileName.set(        # jeśli tak ustawiamy StringVar profileName na [Imie] [Nazwisko] - [Login]
            kantor.konto.imie + " " + kantor.konto.nazwisko + " - " + kantor.konto.login
        )
        menu_frame.pack(fill="both", expand=1)  # odkrywamy menu
        login_frame.forget()                    # chowamy okno logowania
        msb.showinfo("Informacja", "Pomyślnie zalogowano")      # alert informujący o pomyślnym zalogowaniu
        refreshPortfel()            # odświeżamy portfel aby pokazały się pieniądze zalogowanego konta
    else:               # w przypadku niepowodzenia wyświetlamy Błąd informujący o niepoprawnym loginie lub haśle
        msb.showerror("Błąd", "Podano błędny login lub hasło")
    loginE.delete(0, tk.END)        # czyścimy Entry Loginu i Hasła
    passE.delete(0, tk.END)


def loginStart():   # metoda cofająca z okna logowania do okna startowego
    start_frame.pack(fill="both", expand=1)
    login_frame.forget()


labelLogTitle = tk.Label(login_frame, text="Logowanie", font=("Calibri Bold", 20))
labelLogTitle.grid(column=1, row=0)         # Label tytułowy

labelLogin = tk.Label(login_frame, text="Login")
labelLogin.grid(column=0, row=1)            # Label "login"

loginE = tk.Entry(login_frame)              # Entry w które wpisujemy login
loginE.grid(column=1, row=1)

labelPass = tk.Label(login_frame, text="Haslo")
labelPass.grid(column=0, row=2)             # Label "hasło

passE = tk.Entry(login_frame, show="*")     # Entry w które wpisujemy hasło
passE.grid(column=1, row=2)                 # dzięki 'show="*"' podczas wpisywania widoczne są tylko * zamiast hasla

btnLM = tk.Button(login_frame, text="Zaloguj", command=loginMenu)
btnLM.grid(column=1, row=3)                 # przycisk odpowiedzialny za logowanie (metoda loginMenu)

btnLS = tk.Button(login_frame, text="Wstecz", command=loginStart)
btnLS.grid(column=1, row=4)                 # przycisk odpowiedzialny za cofanie do okna startowego

btnLQ = tk.Button(login_frame, text="Wyjście", command=kantorQuit)
btnLQ.grid(column=1, row=5)                 # przycisk odpowiedzialny za zamykanie aplikacji


# ====================REGISTER_FRAME====================


def regLogin():      # metoda rejestrująca nowe konto i przenosząca do logowania
    flagName = True
    flagSurname = True         # flagi potrzebne żeby wiedzieć które pole zostało źle podane
    flagLogin = True
    flagPass = True
    if not str.isprintable(nameE.get()) or len(nameE.get()) < 1:
        flagName = False
    for char in nameE.get():       # sprawdzamy czy każde pole zawiera tylko znaki drukowalne (bez \t, \n, itp.),
        if str.isspace(char):      # czy nie ma długości mniejszej od 1 lub czy nie zawiera spacji
            flagName = False    # jeśli coś jest nie tak, ustawiamy odpowiednie flag na False

    if not str.isprintable(snameE.get()) or len(snameE.get()) < 1:
        flagSurname = False
    for char in snameE.get():
        if str.isspace(char):
            flagSurname = False

    if not str.isprintable(regLoginE.get()) or len(regLoginE.get()) < 1:
        flagLogin = False
    for char in regLoginE.get():
        if str.isspace(char):
            flagLogin = False

    if not str.isprintable(regPassE.get()) or len(regPassE.get()) < 1:
        flagPass = False
    for char in regPassE.get():
        if str.isspace(char):
            flagPass = False

    if flagSurname and flagName and flagLogin and flagPass:             # sprawdzamy czy podane dane są dobre
        if kantor.register(nameE.get(), snameE.get(), regLoginE.get(), regPassE.get()):
            msb.showinfo("Informacja", "Pomyślnie zarejestrowano")      # następnie próbujemy rejestrować
            nameE.delete(0, tk.END)         # jeśli się udało wyświetlamy informację o pomyślnej rejestracji
            snameE.delete(0, tk.END)        # i kasujemy wartości z wszystkich Entry
            regLoginE.delete(0, tk.END)
            regPassE.delete(0, tk.END)
            login_frame.pack(fill="both", expand=1)
            register_frame.forget()
        else:
            msb.showerror("Błąd", "Podany login jest zajęty")   # a jeśli podany login jest zajęty,
            regLoginE.delete(0, tk.END)     # wyświetlamy błąd i kasujemy to co było wpisane w Entry loginu
    else:
        msb.showerror("Błąd", "Podane dane są nieprawidłowe")
        if not flagName:            # a jeśli któreś z danych były niepoprawne (spacje, len=0, znaki niedrukowalne)
            nameE.delete(0, tk.END)
        if not flagSurname:             # to wyświetlamy błąd i kasujemy tylko błędne Entry
            snameE.delete(0, tk.END)
        if not flagLogin:
            regLoginE.delete(0, tk.END)
        if not flagPass:
            regPassE.delete(0, tk.END)


def regStart():     # metoda przełączająca z okna rejestracji na okno startowe
    start_frame.pack(fill="both", expand=1)
    register_frame.forget()


labelRegTitle = tk.Label(register_frame, text="Rejestracja", font=("Calibri Bold", 20))
labelRegTitle.grid(column=1, row=0)     # Label tytułowy

labelName = tk.Label(register_frame, text="Imię")
labelName.grid(column=0, row=1)         # Label "Imię"

nameE = tk.Entry(register_frame)        # Entry "Imię"
nameE.grid(column=1, row=1)

labelSname = tk.Label(register_frame, text="Nazwisko")
labelSname.grid(column=0, row=2)        # Label "Nazwisko"

snameE = tk.Entry(register_frame)       # Entry "Nazwisko"
snameE.grid(column=1, row=2)

labelRegLogin = tk.Label(register_frame, text="Login")
labelRegLogin.grid(column=0, row=3)     # Label "Login"

regLoginE = tk.Entry(register_frame)    # Entry "Login"
regLoginE.grid(column=1, row=3)

labelRegPass = tk.Label(register_frame, text="Haslo")
labelRegPass.grid(column=0, row=4)      # Label "Haslo"

regPassE = tk.Entry(register_frame, show="*")
regPassE.grid(column=1, row=4)          # Entry "Haslo" (ponownie pokazywane * zamiast znaków)

btnReg = tk.Button(register_frame, text="Rejestruj", command=regLogin)
btnReg.grid(column=1, row=5)            # Przycisk odpowiedzialny za rejestracją (metoda regLogin)

btnRS = tk.Button(register_frame, text="Wstecz", command=regStart)
btnRS.grid(column=1, row=6)             # Przycisk odpowiedzialny za cofanie do okna startowego

btnRQ = tk.Button(register_frame, text="Wyjście", command=kantorQuit)
btnRQ.grid(column=1, row=7)             # Przycisk odpowiedzialny za zamknięcie aplikacji


# ====================MENU_FRAME====================


def menuProfile():      # metoda przełączająca okno menu na okno profilu
    profile_frame.pack(fill="both", expand=1)
    menu_frame.forget()


def menuTransaction():  # metoda przełączająca okno menu na okno transakcji
    transaction_frame.pack(fill="both", expand=1)
    menu_frame.forget()


def menuStart():        # metoda wylogowująca i przełączająca na okno startu
    kantor.logout()     # wylogowanie
    msb.showinfo("Informacja", "Pomyślnie wylogowano")  # wyświetlenie komunikatu
    start_frame.pack(fill="both", expand=1)
    menu_frame.forget()


def refreshKursy():     # metoda odświeżająca kursy
    kantor.refreshKursy()   # odświeżamy kursy metodą z pliku kantor.py
    kursyLB.delete(0, tk.END)
    for kurs in kantor.kursy:          # odświeżamy ceny kursów w Listbox wyświetlanym w menu
        kursyLB.insert(tk.END, str(kurs))


labelMenuTitle = tk.Label(
    menu_frame, text="Witaj w menu kantoru wymiany walut", font=("Calibri Bold", 20)
)                               # Label powitalny w menu
labelMenuTitle.grid(row=0)

labelWalutex2 = tk.Label(
    menu_frame, text="WALUTEX", font=("Verdana Bold", 20), fg="blue"
)                               # Label z nazwą kantoru
labelWalutex2.grid(row=1)

labelKontoM1 = tk.Label(menu_frame, text="Zalogowano jako: ", font=("Calibri", 15))
labelKontoM1.grid(row=2)        # Label "Zalogowano jako: "

labelKontoM2 = tk.Label(
    menu_frame,
    textvariable=profileName,   # Label z textvariable które zmieni się po zmianie wartości profileName
    font=("Calibri", 15),       # np. przy logowaniu
)
labelKontoM2.grid(row=3)

btnMP = tk.Button(menu_frame, text="Profil", command=menuProfile)
btnMP.grid(row=4)               # Przycisk odpowiedzialny za przejście do okna profilu

labelKursy = tk.Label(menu_frame, text="Aktualne kursy:")
labelKursy.grid(row=5)          # Label "Aktualne kursy: "

btnRefresh = tk.Button(menu_frame, text="Odśwież kursy", command=refreshKursy)
btnRefresh.grid(row=6)          # Przycisk odświeżający kursy (metoda refreshKursy)

kursyLB = tk.Listbox(menu_frame, font=("Courier", 10))
for x in kantor.kursy:
    kursyLB.insert(tk.END, str(x))      # Listbox wyświetlający po kolei wszystkie kursy
kursyLB.grid(row=7)

btnMT = tk.Button(menu_frame, text="Nowa transakcja", command=menuTransaction)
btnMT.grid(row=8)               # Przycisk odpowiedzialny za przejście do okna transakcji

btnMS = tk.Button(menu_frame, text="Wyloguj", command=menuStart)
btnMS.grid(row=9)               # Przycisk odpowiedzialny za przejście do okna startowego i wylogowanie

btnMQ = tk.Button(menu_frame, text="Wyjście", command=kantorQuit)
btnMQ.grid(row=10)              # Przycisk odpowiedzialny za zamknięcie aplikacji


# ====================PROFILE_FRAME====================


def moneyIn():          # metoda odpowiedzialna za wpłacanie środków
    if checkFloat(walutaInE.get()):     # sprawdzamy czy wpisana w Entry wartość może być float'em
        kantor.wplata(walutaIn.get(), round(float(walutaInE.get()), 2))      # wpłacamy
        refreshPortfel()                # symbol wypłaty pobierany z OptionMenu, odświeżamy portfel
        msb.showinfo(
            "Informacja",
            "Pomyślnie wpłacono "       # wyświetlamy informację "Pomyślnie wpłacono ..."
            + str(round(float(walutaInE.get()), 2))
            + " "
            + walutaIn.get(),
        )
        walutaInE.delete(0, tk.END)     # czyścimy Entry
    else:
        msb.showerror("Błąd", "Podano złą kwotę")       # wyświetlamy błąd mówiący że podano złą wartość w Entry
        walutaInE.delete(0, tk.END)         # czyścimy Entry


def moneyOut():         # metoda odpowiadająca za wypłatę pieniędzy
    if checkFloat(walutaOutE.get()):        # sprawdamy czy podano wartość która może być float'em w Entry
        if kantor.wyplata(walutaOut.get(), round(float(walutaOutE.get()), 2)):  # próba wypłaty
            refreshPortfel()        # symbol wypłaty pobierany z OptionMenu, odświeżamy portfel
            msb.showinfo(
                "Informacja",
                "Pomyślnie wypłacono "          # wyświetlamy informację o pomyślnym wypłaceniu danej kwoty
                + str(round(float(walutaOutE.get()), 2))
                + " "
                + walutaOut.get(),
            )
            walutaOutE.delete(0, tk.END)        # czyścimy Entry
        else:
            msb.showerror("Błąd", "Nie posiadasz wystarczających środków na koncie")
            walutaOutE.delete(0, tk.END)        # jeśli nie powiodło się wypłacenie, oznacza to że mamy za mało
    else:                                   # środków, wyświetlamy stosowny Error
        msb.showerror("Błąd", "Podano złą kwotę")
        walutaOutE.delete(0, tk.END)        # Błąd mówiący o tym że podano złą wartość w Entry


def moneyCalc():
    msb.showinfo(       # metoda przeliczająca pieniądze w portfelu na walutę podaną w OptionMenu
        "Informacja",
        "Posiadasz aktualnie "
        + str(round(float(kantor.przeliczPortfel(walutaCalc.get())), 2))
        + " "           # informacja o tym ile potencjalnie pieniędzy jednej waluty posiadamy
        + walutaCalc.get(),
    )


def profileMenu():      # metoda przełączająca z okna profilu do okna menu
    profile_frame.forget()
    menu_frame.pack(fill="both", expand=1)


def export():       # metoda zapisująca raport z konta
    filename = (
        kantor.konto.imie           # nazwa pliku jako [Imie][Nazwisko][Login][Aktualny czas bez dwukropków]
        + kantor.konto.nazwisko     # aby można było generować kilka raportów
        + kantor.konto.login
        + str(datetime.datetime.now()).replace(":", "")
        + ".txt"
    )
    with open(filename, "w", encoding="utf-8") as f:
        f.write(kantor.konto.imie + " " + kantor.konto.nazwisko + "\n")
        f.write(kantor.konto.login + "\n")
        f.write("Portfel:\n")               # do pliku zapisujemy imie i nazwisko, login oraz pieniadze
        for money in kantor.konto.portfel:
            f.write(str(money) + "\n")          # informacja mówiąca że raport wygeneruje się po zamknięciu
        msb.showinfo("Informacja", "Raport zostanie wygenerowany po zamknięciu aplikacji")


labelKontoP1 = tk.Label(profile_frame, text="Zalogowano jako: ", font=("Calibri", 15))
labelKontoP1.grid(row=0, column=1)      # Label "Zalogowano jako: "

labelKontoP2 = tk.Label(
    profile_frame,
    textvariable=profileName,           # Label z profileName, taki sam jak w menu_frame
    font=("Calibri", 15),
)
labelKontoP2.grid(row=1, column=1)

labelPortfel = tk.Label(profile_frame, text="Twój portfel:")
labelPortfel.grid(row=2, column=1)      # Label "Twój portfel: "

portfelLB = tk.Listbox(profile_frame, font=("Courier", 10), height=11)
for x in kantor.konto.portfel:
    portfelLB.insert(tk.END, str(x))        # Listbox z wartościami w portfelu, dzięki height=11 wyświetlają
portfelLB.grid(row=3, column=1)             # wszystkie 11 walut a nie domyślne 10 z możliwością scrollowania

walutaIn = tk.StringVar(profile_frame)      # Tworzymy OptionMenu, za pomocą zmiennej StringVar która będzie przez
walutaIn.set(waluty[0])                     # OptionMenu zmieniana
walutaInDrop = tk.OptionMenu(profile_frame, walutaIn, *waluty)  # Option menu zmienia "walutaIn" i korzysta z
walutaInDrop.grid(row=4, column=0)          # tablicy "waluty" (parametr *waluty) zapisanej na samym początku

walutaInE = tk.Entry(profile_frame)         # Entry wpłacanej kwoty
walutaInE.grid(row=4, column=1)

btnIN = tk.Button(profile_frame, text="Wpłać środki", command=moneyIn)
btnIN.grid(row=4, column=2)                 # Przycisk odpowiedzialny za wpłacanie pieniędzy

walutaOut = tk.StringVar(profile_frame)
walutaOut.set(waluty[0])                    # Analogicznie jak w przypadku wpłacania pieniędzy
walutaOutDrop = tk.OptionMenu(profile_frame, walutaOut, *waluty)
walutaOutDrop.grid(row=5, column=0)

walutaOutE = tk.Entry(profile_frame)
walutaOutE.grid(row=5, column=1)            # Entry wypłacanej kwoty

btnOUT = tk.Button(profile_frame, text="Wypłać środki", command=moneyOut)
btnOUT.grid(row=5, column=2)                # Przycisk odpowiedzialny za wypłacanie kwoty

walutaCalc = tk.StringVar(profile_frame)
walutaCalc.set(waluty[0])                   # Kolejne OptionMenu
walutaCalcDrop = tk.OptionMenu(profile_frame, walutaCalc, *waluty)
walutaCalcDrop.grid(row=6, column=0)

btnCalc = tk.Button(profile_frame, text="Przelicz środki", command=moneyCalc)
btnCalc.grid(row=6, column=1)               # Przycisk odpowiedzialny za przeliczenie środków

btnExport = tk.Button(profile_frame, text="Eksportuj do pliku .txt", command=export)
btnExport.grid(row=7, column=1)             # Przycisk odpowiedzialny za eksport profilu do .txt

btnPM = tk.Button(profile_frame, text="Wstecz", command=profileMenu)
btnPM.grid(row=8, column=1)                 # Przycisk odpowiedzialny za przejście do menu z profilu

btnPQ = tk.Button(profile_frame, text="Wyjście", command=kantorQuit)
btnPQ.grid(row=9, column=1)                 # Przycisk odpowiedzialny za zamykanie aplikacji


# ====================TRANSACTION_FRAME====================


def transaction():      # Metoda odpowiedzialna za transakcję, najpierw sprawdzana jest podana wartość oraz
    if checkFloat(waluta1E.get()) and waluta1.get() != waluta2.get():   # czy nie są wybrane 2 takie same waluty
        if buyFlag.get() == "Kupno":        # Sprawdzamy czy jest to transakcja Kupna
            kursTemp = kantor.znajdzKurs(waluta1.get(), waluta2.get())
            if msb.askyesno(                # Szukamy odpowiedniego kursu
                "Potwierdzenie",            # Pytamy o potwierdzenie i wyświetlamy
                "Czy chcesz kupić "         # szczegóły transakcji
                + waluta1E.get()            # Czy Kupno/Sprzedaż jakiej waluty, ile i za ile jakiej waluty
                + waluta1.get()             # oraz informacja o kursie po jakim rozliczana jest transakcja
                + " za "
                + str(round(float(waluta1E.get()) * kursTemp.cena, 2))
                + waluta2.get()
                + "\npo kursie "
                + str(kursTemp)
                + "?",
            ):
                if kantor.transakcja(True, kursTemp, round(float(waluta1E.get()), 2)):
                    msb.showinfo(
                        "Informacja",       # Jeśli w oknie dialogowym kliknięto Tak
                        "Kupiono "          # Rozliczamy transakcję i wyświetlamy potwierdzenie
                        + waluta1E.get()
                        + waluta1.get()
                        + " za "
                        + str(round(float(waluta1E.get()) * kursTemp.cena, 2))
                        + waluta2.get(),
                    )
                    refreshPortfel()        # Odświeżamy portfel
                    waluta1E.delete(0, tk.END)  # Kasujemy Entry z ilością
                else:
                    msb.showerror("Błąd", "Posiadasz za mało środków")  # W przypadku braku środków
                    waluta1E.delete(0, tk.END)  # Wyświetlamy odpowiedni komunikat i czyścimy Entry
        else:
            kursTemp = kantor.znajdzKurs(waluta1.get(), waluta2.get())
            if msb.askyesno(            # Analogiczna sytuacja dla transakcji sprzedaży
                "Potwierdzenie",
                "Czy chcesz sprzedać "
                + waluta1E.get()
                + waluta1.get()
                + " za "
                + str(round(float(waluta1E.get()) * kursTemp.cena, 2))
                + waluta2.get()
                + "\npo kursie "
                + str(kursTemp)
                + "?",
            ):
                if kantor.transakcja(False, kursTemp, round(float(waluta1E.get()), 2)):
                    msb.showinfo(
                        "Informacja",
                        "Sprzedano "
                        + waluta1E.get()
                        + waluta1.get()
                        + " za "
                        + str(round(float(waluta1E.get()) * kursTemp.cena, 2))
                        + waluta2.get(),
                    )
                    refreshPortfel()
                    waluta1E.delete(0, tk.END)
                else:
                    msb.showerror("Błąd", "Posiadasz za mało środków")
                    waluta1E.delete(0, tk.END)
    else:
        msb.showerror("Błąd", "Podano złą kwotę lub wybrano takie same waluty")     # Jeśli podano złą wartość lub
        waluta1E.delete(0, tk.END)          # wybrano dwie takie same waluty czyścimy Entry


def transactionMenu():          # Metoda odpowiedzialna za cofnięcie do menu
    transaction_frame.forget()
    menu_frame.pack(fill="both", expand=1)


labelTransactionTitle = tk.Label(
    transaction_frame, text="Nowa transakcja", font=("Calibri Bold", 20)
)                               # Label tytułowy
labelTransactionTitle.grid()

labelPortfelT = tk.Label(transaction_frame, text="Twój portfel:")
labelPortfelT.grid()            # Label "Twój portfel: "

portfelLBT = tk.Listbox(transaction_frame, font=("Courier", 10), height=11)
for x in kantor.konto.portfel:
    portfelLBT.insert(tk.END, str(x))       # Listbox z pieniędzmi w portfelu
portfelLBT.grid()

buyFlag = tk.StringVar(transaction_frame)
buyFlag.set("Kupno")                        # Optionbox w którym wybieramy czy Kupno czy Sprzedaż
buyFlagDrop = tk.OptionMenu(transaction_frame, buyFlag, *["Kupno", "Sprzedaż"])
buyFlagDrop.grid()

waluta1 = tk.StringVar(transaction_frame)
waluta1.set(waluty[0])                      # Optionbox z wyborem pierwszej waluty (kupowanej/sprzedawanej)
waluta1Drop = tk.OptionMenu(transaction_frame, waluta1, *waluty)
waluta1Drop.grid()

waluta1E = tk.Entry(transaction_frame)      # Entry z ilością waluty
waluta1E.grid()

labelZa = tk.Label(transaction_frame, text="Za")
labelZa.grid()                              # Label "Za"

waluta2 = tk.StringVar(transaction_frame)
waluta2.set(waluty[0])                  # OptionMenu dla wyboru drugiej waluty (tej którą płacimy lub otrzymywanej)
waluta2Drop = tk.OptionMenu(transaction_frame, waluta2, *waluty)
waluta2Drop.grid()

btnTransaction = tk.Button(transaction_frame, text="Przelicz", command=transaction)
btnTransaction.grid()                   # Przycisk odpowiedzialny za transakcję

btnTM = tk.Button(transaction_frame, text="Wstecz", command=transactionMenu)
btnTM.grid()                            # Przycisk odpowiedzialny za cofnięcie do menu

btnTQ = tk.Button(transaction_frame, text="Wyjście", command=kantorQuit)
btnTQ.grid()                            # Przycisk odpowiedzialny za zamknięcie aplikacji

start_frame.pack(fill="both", expand=1)          # Jako pierwsze pokazuje sie okno startowe
root.mainloop()                                  # Włączenie aplikacji
