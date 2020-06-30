# Dame 
# Algoritmii Minimax si Alpha-beta

import copy
import time

from os import system, name


def clear():

    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def coordonate_in_tabla(i, j):
    return 0 <= i and i <= Joc.NR_LINII - 1 and 0 <= j and j <= Joc.NR_COLOANE - 1


def culoare_opusa(culoare):
    if culoare == 'a' or culoare == 'A':
        return 'n'
    if culoare == 'n' or culoare == 'N':
        return 'a'


class Joc:
    NR_LINII = 8
    NR_COLOANE = 8
    JMIN = None
    JMAX = None
    GOL = ' '
    JOS = 1
    SUS = -1
    DREAPTA = 1
    STANGA = -1
    NIVEL_USOR = 2
    NIVEL_MEDIU = 3
    NIVEL_GREU = 5
    NR_MUTARI_JMIN = 0
    NR_MUTARI_JMAX = 0
    estimare_scor = None

    def __init__(self, tabla=None, coordonate_piese_JMAX=None, coordonate_piese_JMIN=None):
        if tabla is None:

            # in cadrul partidei de joc, vom pozitiona tabla in mod firesc atfel:
            # calculatorul JMAX intotdeauna in partea de sus a tablei
            # jucatorul JMIN intotdeauna in partea de jos a tablei

            tabla = [[None for coloana in range(
                Joc.NR_COLOANE)] for linie in range(Joc.NR_LINII)]

            for i in range(0, Joc.NR_COLOANE, 2):
                tabla[0][i] = Joc.GOL
            for i in range(1, Joc.NR_COLOANE, 2):
                tabla[0][i] = Joc.JMAX

            for i in range(0, Joc.NR_COLOANE, 2):
                tabla[1][i] = Joc.JMAX
            for i in range(1, Joc.NR_COLOANE, 2):
                tabla[1][i] = Joc.GOL

            for i in range(0, Joc.NR_COLOANE, 2):
                tabla[2][i] = Joc.GOL
            for i in range(1, Joc.NR_COLOANE, 2):
                tabla[2][i] = Joc.JMAX

            for i in range(Joc.NR_COLOANE):
                tabla[3][i] = Joc.GOL
            for i in range(Joc.NR_COLOANE):
                tabla[4][i] = Joc.GOL

            for i in range(0, Joc.NR_COLOANE, 2):
                tabla[5][i] = Joc.JMIN
            for i in range(1, Joc.NR_COLOANE, 2):
                tabla[5][i] = Joc.GOL

            for i in range(0, Joc.NR_COLOANE, 2):
                tabla[6][i] = Joc.GOL
            for i in range(1, Joc.NR_COLOANE, 2):
                tabla[6][i] = Joc.JMIN

            for i in range(0, Joc.NR_COLOANE, 2):
                tabla[7][i] = Joc.JMIN
            for i in range(1, Joc.NR_COLOANE, 2):
                tabla[7][i] = Joc.GOL

        self.configuratie_tabla = tabla

        if coordonate_piese_JMAX is None or coordonate_piese_JMIN is None:
            coordonate_piese_JMAX = []
            coordonate_piese_JMIN = []
            for linie in range(len(self.configuratie_tabla)):
                for col in range(len(self.configuratie_tabla[linie])):
                    if self.configuratie_tabla[linie][col].lower() == Joc.JMAX:
                        coordonate_piese_JMAX.append((linie, col))
                    elif self.configuratie_tabla[linie][col].lower() == Joc.JMIN:
                        coordonate_piese_JMIN.append((linie, col))
        self.coordonate_piese_JMAX = coordonate_piese_JMAX
        self.coordonate_piese_JMIN = coordonate_piese_JMIN

    def final(self):
        # verifica daca a castigat cineva (return simbolul castigatorului),
        # daca a fost remiza (return "remiza"),
        # sau daca nu s-a terminat jocul (return False)

        # nu mai exista piese ale jucatorului JMIN pe tabla
        if len(self.coordonate_piese_JMIN) == 0:
            return Joc.JMAX
        # nu mai exista piese ale jucatorului JMAX pe tabla
        if len(self.coordonate_piese_JMAX) == 0:
            return Joc.JMIN

        # atunci cand un jucator nu se mai poate deplasa pe tabla declaram remiza
        if self.nr_pozitii_deschise(Joc.JMIN) == 0 or self.nr_pozitii_deschise(Joc.JMAX) == 0:
            return 'remiza'

        return False

    def pozitie_de_capturare(self, linie, coloana, directie_i):

        linie_mijloc = linie + directie_i
        linie_noua = linie_mijloc + directie_i

        coloana_mijloc = coloana + Joc.STANGA
        coloana_noua = coloana_mijloc + Joc.STANGA
        if self.este_posibila_capturarea(self.configuratie_tabla[linie][coloana], linie_mijloc, coloana_mijloc, linie_noua, coloana_noua):
            return True

        coloana_mijloc = coloana + Joc.DREAPTA
        coloana_noua = coloana_mijloc + Joc.DREAPTA
        if self.este_posibila_capturarea(self.configuratie_tabla[linie][coloana], linie_mijloc, coloana_mijloc, linie_noua, coloana_noua):
            return True

        if self.configuratie_tabla[linie][coloana].isupper():
            linie_mijloc = linie + (-directie_i)
            linie_noua = linie_mijloc + (-directie_i)

            coloana_mijloc = coloana + Joc.STANGA
            coloana_noua = coloana_mijloc + Joc.STANGA
            if self.este_posibila_capturarea(self.configuratie_tabla[linie][coloana], linie_mijloc, coloana_mijloc, linie_noua, coloana_noua):
                return True

            coloana_mijloc = coloana + Joc.DREAPTA
            coloana_noua = coloana_mijloc + Joc.DREAPTA
            if self.este_posibila_capturarea(self.configuratie_tabla[linie][coloana], linie_mijloc, coloana_mijloc, linie_noua, coloana_noua):
                return True

        return False

    def pozitie_de_avansare(self, linie, coloana, directie_i):
        if linie + directie_i in range(0, 8):
            if coloana + Joc.STANGA in range(0, 8) and self.configuratie_tabla[linie + directie_i][coloana + Joc.STANGA] == Joc.GOL:
                return True
            if coloana + Joc.DREAPTA in range(0, 8) and self.configuratie_tabla[linie + directie_i][coloana + Joc.DREAPTA] == Joc.GOL:
                return True

        if self.configuratie_tabla[linie][coloana].isupper():
            if linie + (-directie_i) in range(0, 8):
                if coloana + Joc.STANGA in range(0, 8) and self.configuratie_tabla[linie + (-directie_i)][coloana + Joc.STANGA] == Joc.GOL:
                    return True
                if coloana + Joc.DREAPTA in range(0, 8) and self.configuratie_tabla[linie + (-directie_i)][coloana + Joc.DREAPTA] == Joc.GOL:
                    return True

        return False

    def nr_pozitii_de_capturare(self, jucator):
        nr_pozitii_de_capturare = 0

        if jucator == Joc.JMIN:
            # damele lui JMIN se pot deplasa doar in sus, regii lui JMIN se pot deplasa in sus si in jos
            for coordonate_piesa in self.coordonate_piese_JMIN:
                if self.pozitie_de_capturare(coordonate_piesa[0], coordonate_piesa[1], Joc.SUS):
                    nr_pozitii_de_capturare += 1
        else:
            # damele lui JMAX se pot deplasa doar in jos, regii lui JMAX se pot deplasa in sus si in jos
            for coordonate_piesa in self.coordonate_piese_JMAX:
                if self.pozitie_de_capturare(coordonate_piesa[0], coordonate_piesa[1], Joc.JOS):
                    nr_pozitii_de_capturare += 1

        return nr_pozitii_de_capturare

    def nr_pozitii_deschise(self, jucator):
        nr_pozitii_deschise = 0

        if jucator == Joc.JMIN:
            # damele lui JMIN se pot deplasa doar in sus, regii lui JMIN se pot deplasa in sus si in jos
            for coordonate_piesa in self.coordonate_piese_JMIN:
                if self.pozitie_de_avansare(coordonate_piesa[0], coordonate_piesa[1], Joc.SUS) or self.pozitie_de_capturare(coordonate_piesa[0], coordonate_piesa[1], Joc.SUS):
                    nr_pozitii_deschise += 1
        else:
            # damele lui JMAX se pot deplasa doar in jos, regii lui JMAX se pot deplasa in sus si in jos
            for coordonate_piesa in self.coordonate_piese_JMAX:
                if self.pozitie_de_avansare(coordonate_piesa[0], coordonate_piesa[1], Joc.JOS) or self.pozitie_de_capturare(coordonate_piesa[0], coordonate_piesa[1], Joc.JOS):
                    nr_pozitii_deschise += 1

        return nr_pozitii_deschise

    def este_posibila_capturarea(self, piesa_curenta, i_next_poz, j_next_poz, i_next_next_poz, j_next_next_poz):
        return coordonate_in_tabla(i_next_poz, j_next_poz) and coordonate_in_tabla(i_next_next_poz, j_next_next_poz) and self.este_piesa_de_culoare_opusa(piesa_curenta, i_next_poz, j_next_poz) and self.configuratie_tabla[i_next_next_poz][j_next_next_poz] == Joc.GOL

    def este_piesa_de_culoare_opusa(self, piesa, i, j):
        return self.configuratie_tabla[i][j].lower() == culoare_opusa(piesa)

    def captureaza(self, l_mutari, tabla, i_start, j_start, deplasare_i, deplasare_j):
        i_next_poz = i_start + deplasare_i
        j_next_poz = j_start + deplasare_j
        i_next_next_poz = i_next_poz + deplasare_i
        j_next_next_poz = j_next_poz + deplasare_j
        configuratie_tabla_noua = None

        if self.este_posibila_capturarea(self.configuratie_tabla[i_start][j_start], i_next_poz, j_next_poz, i_next_next_poz, j_next_next_poz):
            configuratie_tabla_noua = copy.deepcopy(tabla)

        while self.este_posibila_capturarea(self.configuratie_tabla[i_start][j_start], i_next_poz, j_next_poz, i_next_next_poz, j_next_next_poz):
            # print(f'Avansare in capturare din pozitia ({i_start}, {j_start}) in pozitia ({i_next_next_poz}, {j_next_next_poz})')
            configuratie_tabla_noua[i_next_next_poz][j_next_next_poz] = configuratie_tabla_noua[i_start][j_start]
            configuratie_tabla_noua[i_start][j_start] = Joc.GOL
            configuratie_tabla_noua[i_next_poz][j_next_poz] = Joc.GOL

            i_start = i_next_next_poz
            j_start = j_next_next_poz

            # dama de pe linie terminala devine rege si capturarea se opreste
            if (i_start == 0 or i_start == Joc.NR_LINII - 1) and configuratie_tabla_noua[i_start][j_start].islower():
                configuratie_tabla_noua[i_start][j_start] = configuratie_tabla_noua[i_start][j_start].upper(
                )
                break

            i_next_poz = i_start + deplasare_i
            j_next_poz = j_start + deplasare_j
            i_next_next_poz = i_next_poz + deplasare_i
            j_next_next_poz = j_next_poz + deplasare_j

            # apelam capturarea si pentru diagonala opusa (directia opusa lui j)
            self.captureaza(l_mutari, configuratie_tabla_noua,
                            i_start, j_start, deplasare_i, -deplasare_j)

            # regele apeleaza capturarea si pentru ambele diagonale pe directia opusa lui i
            if configuratie_tabla_noua[i_start][j_start].isupper():
                self.captureaza(l_mutari, configuratie_tabla_noua,
                                i_start, j_start, -deplasare_i, deplasare_j)
                self.captureaza(l_mutari, configuratie_tabla_noua,
                                i_start, j_start, -deplasare_i, -deplasare_j)

        if configuratie_tabla_noua is not None:
            l_mutari.append(Joc(configuratie_tabla_noua))

    def avanseaza_o_casuta(self, i_start, j_start, i_end, j_end):
        configuratie_tabla_noua = copy.deepcopy(
            self.configuratie_tabla)
        configuratie_tabla_noua[i_start][j_start] = Joc.GOL
        # dama a ajuns pe o linie terminala => trebuie transformata in rege
        if self.configuratie_tabla[i_start][j_start].islower() and (i_end == 0 or i_end == Joc.NR_LINII - 1):
            configuratie_tabla_noua[i_end][j_end] = self.configuratie_tabla[i_start][j_start].upper(
            )
        else:
            configuratie_tabla_noua[i_end][j_end] = self.configuratie_tabla[i_start][j_start]
        return configuratie_tabla_noua

    def avanseaza(self, i, j, deplasare_i, deplasare_j, l_mutari):
        if coordonate_in_tabla(i + deplasare_i, j + deplasare_j):
            # verificam daca este posibila avansarea simpla
            if self.configuratie_tabla[i + deplasare_i][j + deplasare_j] == Joc.GOL:
                # print(f'Avansare simpla din pozitia ({i}, {j}) in pozitia ({i + deplasare_i}, {j + deplasare_j})')
                configuratie_tabla_noua = self.avanseaza_o_casuta(
                    i, j, i + deplasare_i, j + deplasare_j)
                l_mutari.append(Joc(configuratie_tabla_noua))
            # verificam daca este posibila avansarea in capturare
            else:
                self.captureaza(l_mutari, self.configuratie_tabla,
                                i, j, deplasare_i, deplasare_j)

    def muta_piesa(self, i, j, directie_avansare, l_mutari):
        self.avanseaza(i, j, directie_avansare, Joc.STANGA, l_mutari)
        self.avanseaza(i, j, directie_avansare, Joc.DREAPTA, l_mutari)
        if self.configuratie_tabla[i][j].isupper():
            # regele se poate deplasa si pe diagonala in spate
            self.avanseaza(i, j, -directie_avansare, Joc.STANGA, l_mutari)
            self.avanseaza(i, j, -directie_avansare, Joc.DREAPTA, l_mutari)

    def genereaza_mutari(self, jucator):
        """
        Pentru configuratia curenta de joc "self.configuratie_tabla" (de tip matrice),
        vom returna o lista "l_mutari" cu elemente de tip Joc,
        corespunzatoare tuturor configuratiilor-succesor posibile.
        "jucator" este simbolul jucatorului care face mutarea
        """
        l_mutari = []

        # pentru o dama alba de coordonate (i,j)
        # miscarile de avansare posibile vor fi (i + 1, j - 1) si (i + 1, j + 1) - avansare in jos-stanga, jos-dreapta
        # pentru o dama neagra de coordonate (i,j)
        # miscarile de avansare posibile vor fi (i - 1, j - 1) si (i - 1, j + 1) - avansare in sus-stanga, sus-dreapta
        # pentru un rege alb / negru de coordonate (i,j)
        # miscarile de avansare posibile vor fi (i + 1, j - 1), (i + 1, j + 1), (i - 1, j - 1), (i - 1, j + 1) - avansare in jos/sus - stanga/dreapta

        if jucator == Joc.JMIN:
            for coordonate_piesa in self.coordonate_piese_JMIN:
                # JMIN este pozitionat intodeauna in josul tablei => piesele lui JMIN se vor deplasa in SUS
                self.muta_piesa(
                    coordonate_piesa[0], coordonate_piesa[1], Joc.SUS, l_mutari)
        else:
            for coordonate_piesa in self.coordonate_piese_JMAX:
                # JMAX este pozitionat intotdeauna in susul tablei => piesle lui JMAX se vor deplasa in JOS
                self.muta_piesa(
                    coordonate_piesa[0], coordonate_piesa[1], Joc.JOS, l_mutari)

        # print("\nprinteaza mutarile generate in genereaza_mutari:")
        # for mutare in l_mutari:
        #     print(mutare)

        return l_mutari

    def genereaza_capturari_posibile(self, linie, coloana, directie_i, directie_j):

        capturari_posibile = []

        # verificam daca este posibila capturarea pastrand directia pe i si pe j
        linie_mijloc = linie + directie_i
        linie_noua = linie_mijloc + directie_i
        coloana_mijloc = coloana + directie_j
        coloana_noua = coloana_mijloc + directie_j

        if self.este_posibila_capturarea(self.configuratie_tabla[linie][coloana], linie_mijloc, coloana_mijloc, linie_noua, coloana_noua):
            capturare = {
                "coordonate": (linie_noua, coloana_noua),
                "directie_i": directie_i,
                "directie_j": directie_j
            }
            capturari_posibile.append(capturare)

        # verificam daca este posibila capturarea pastrand directia pe i, dar alegand diagonala opusa (directia opusa pe j)
        linie_mijloc = linie + directie_i
        linie_noua = linie_mijloc + directie_i
        coloana_mijloc = coloana + (-directie_j)
        coloana_noua = coloana_mijloc + (-directie_j)
        if self.este_posibila_capturarea(self.configuratie_tabla[linie][coloana], linie_mijloc, coloana_mijloc, linie_noua, coloana_noua):
            capturare = {
                "coordonate": (linie_noua, coloana_noua),
                "directie_i": directie_i,
                "directie_j": -directie_j
            }
            capturari_posibile.append(capturare)

        # daca piesa curenta este rege, verificam si diagonalele fomate pe directia opusa lui i
        if self.configuratie_tabla[linie][coloana].isupper():

            # pastrand directia pe j
            linie_mijloc = linie + (-directie_i)
            linie_noua = linie_mijloc + (-directie_i)
            coloana_mijloc = coloana + directie_j
            coloana_noua = coloana_mijloc + directie_j
            if self.este_posibila_capturarea(self.configuratie_tabla[linie][coloana], linie_mijloc, coloana_mijloc, linie_noua, coloana_noua):
                capturare = {
                    "coordonate": (linie_noua, coloana_noua),
                    "directie_i": -directie_i,
                    "directie_j": directie_j
                }
                capturari_posibile.append(capturare)

            # alegand directia opusa pe j
            linie_mijloc = linie + (-directie_i)
            linie_noua = linie_mijloc + (-directie_i)
            coloana_mijloc = coloana + (-directie_j)
            coloana_noua = coloana_mijloc + (-directie_j)
            if self.este_posibila_capturarea(self.configuratie_tabla[linie][coloana], linie_mijloc, coloana_mijloc, linie_noua, coloana_noua):
                capturare = {
                    "coordonate": (linie_noua, coloana_noua),
                    "directie_i": -directie_i,
                    "directie_j": -directie_j
                }
                capturari_posibile.append(capturare)

        return capturari_posibile

    def estimeaza_scor(self, adancime):
        t_final = self.final()
        if t_final == Joc.JMAX:
            return (99 + adancime)
        elif t_final == Joc.JMIN:
            return (-99 - adancime)
        elif t_final == 'remiza':
            return 0
        else:
            if Joc.estimare_scor == 1:
                return len(self.coordonate_piese_JMAX) - len(self.coordonate_piese_JMIN)
            else:
                return self.nr_pozitii_de_capturare(Joc.JMAX) - self.nr_pozitii_de_capturare(Joc.JMIN)

    def __str__(self):

        sir = "\n"
        sir += ""

        for col in range(Joc.NR_COLOANE):
            sir += f'     {col}'
        sir += '\n'
        sir += "   "

        for col in range(Joc.NR_COLOANE):
            sir += "______"
        sir += '\n'

        for i in range(len(self.configuratie_tabla)):
            sir += '  |'
            for elem in self.configuratie_tabla[i]:
                sir += '     |'
            sir += '\n'

            sir += f'{i} |'
            for elem in self.configuratie_tabla[i]:
                sir = sir + '  ' + elem + '  |'
            sir += '\n'

            sir += '  |'
            for elem in self.configuratie_tabla[i]:
                sir += '_____|'
            sir += '\n'

        sir += '\n'

        sir = sir + "Nr. piese capturate de JMIN: " + \
            str(12 - len(self.coordonate_piese_JMAX)) + "\n"
        sir = sir + "Nr. piese capturate de JMAX: " + \
            str(12 - len(self.coordonate_piese_JMIN)) + "\n"
        return sir


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita genereaza_mutari() care ofera lista cu
    configuratiile posibile in urma mutarii unui jucator
    """

    ADANCIME_MAX = None

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, scor=None):
        self.tabla_joc = tabla_joc  # un obiect de tip Joc => „tabla_joc.configuratie_tabla”
        self.j_curent = j_curent  # simbolul jucatorului curent

        # adancimea in arborele de stari
        #	(scade cu cate o unitate din „tata” in „fiu”)
        self.adancime = adancime

        # scorul starii (daca e finala, adica frunza a arborelui)
        # sau scorul celei mai bune stari-fiice (pentru jucatorul curent)
        self.scor = scor

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []  # lista va contine obiecte de tip Stare

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def jucator_opus(self):
        if self.j_curent == Joc.JMIN:
            return Joc.JMAX
        return Joc.JMIN

    def genereaza_mutari_posibile(self):
        l_mutari = self.tabla_joc.genereaza_mutari(self.j_curent)
        juc_opus = self.jucator_opus()

        l_stari_mutari = [
            Stare(mutare, juc_opus, self.adancime-1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari

    def este_mutare_valida(self, linie, coloana, linie_noua, coloana_noua, detalii_mutare):
        if self.tabla_joc.configuratie_tabla[linie_noua][coloana_noua] == Joc.GOL:
            # verificam daca mutarea poate fi o avansare simpla
            if linie_noua == linie + Joc.SUS:
                if coloana_noua == coloana + Joc.STANGA:
                    detalii_mutare["tip_mutare"] = "avansare_simpla"
                    detalii_mutare["directie_i"] = Joc.SUS
                    detalii_mutare["directie_j"] = Joc.STANGA
                    return True
                if coloana_noua == coloana + Joc.DREAPTA:
                    detalii_mutare["tip_mutare"] = "avansare_simpla"
                    detalii_mutare["directie_i"] = Joc.SUS
                    detalii_mutare["directie_j"] = Joc.DREAPTA
                    return True

            if self.tabla_joc.configuratie_tabla[linie][coloana].isupper():
                if linie_noua == linie + Joc.JOS:
                    if coloana_noua == coloana + Joc.STANGA:
                        detalii_mutare["tip_mutare"] = "avansare_simpla"
                        detalii_mutare["directie_i"] = Joc.JOS
                        detalii_mutare["directie_j"] = Joc.STANGA
                        return True
                    if coloana_noua == coloana + Joc.DREAPTA:
                        detalii_mutare["tip_mutare"] = "avansare_simpla"
                        detalii_mutare["directie_i"] = Joc.JOS
                        detalii_mutare["directie_j"] = Joc.DREAPTA
                        return True

            # verificam daca mutarea poate fi o avansare in capturare
            linie_mijloc = linie + Joc.SUS
            if linie_noua == linie_mijloc + Joc.SUS:
                coloana_mijloc = coloana + Joc.STANGA
                if coloana_noua == coloana_mijloc + Joc.STANGA and self.tabla_joc.este_piesa_de_culoare_opusa(self.tabla_joc.configuratie_tabla[linie][coloana], linie_mijloc, coloana_mijloc):
                    detalii_mutare["tip_mutare"] = "avansare_in_capturare"
                    detalii_mutare["directie_i"] = Joc.SUS
                    detalii_mutare["directie_j"] = Joc.STANGA
                    return True

                coloana_mijloc = coloana + Joc.DREAPTA
                if coloana_noua == coloana_mijloc + Joc.DREAPTA and self.tabla_joc.este_piesa_de_culoare_opusa(self.tabla_joc.configuratie_tabla[linie][coloana], linie_mijloc, coloana_mijloc):
                    detalii_mutare["tip_mutare"] = "avansare_in_capturare"
                    detalii_mutare["directie_i"] = Joc.SUS
                    detalii_mutare["directie_j"] = Joc.DREAPTA
                    return True

            if self.tabla_joc.configuratie_tabla[linie][coloana].isupper():
                linie_mijloc = linie + Joc.JOS
                if linie_noua == linie_mijloc + Joc.JOS:
                    coloana_mijloc = coloana + Joc.STANGA
                    if coloana_noua == coloana_mijloc + Joc.STANGA and self.tabla_joc.este_piesa_de_culoare_opusa(self.tabla_joc.configuratie_tabla[linie][coloana], linie_mijloc, coloana_mijloc):
                        detalii_mutare["tip_mutare"] = "avansare_in_capturare"
                        detalii_mutare["directie_i"] = Joc.JOS
                        detalii_mutare["directie_j"] = Joc.STANGA
                        return True

                    coloana_mijloc = coloana + Joc.DREAPTA
                    if coloana_noua == coloana_mijloc + Joc.DREAPTA and self.tabla_joc.este_piesa_de_culoare_opusa(self.tabla_joc.configuratie_tabla[linie][coloana], linie_mijloc, coloana_mijloc):
                        detalii_mutare["tip_mutare"] = "avansare_in_capturare"
                        detalii_mutare["directie_i"] = Joc.JOS
                        detalii_mutare["directie_j"] = Joc.DREAPTA
                        return True
        return False

    def __str__(self):
        sir = str(self.tabla_joc) + "(Mutare facuta de: " + self.j_curent+")\n"
        return sir


""" Algoritmul MiniMax """


def min_max(stare):
    # Daca am ajuns la o frunza a arborelui, adica:
    # - daca am expandat arborele pana la adancimea maxima permisa
    # - sau daca am ajuns intr-o configuratie finala de joc
    if stare.adancime == 0 or stare.tabla_joc.final():
        # calculam scorul frunzei apeland "estimeaza_scor"
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # Altfel, calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.genereaza_mutari_posibile()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutari_scor = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu scorul maxim
        stare.stare_aleasa = max(mutari_scor, key=lambda x: x.scor)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu scorul minim
        stare.stare_aleasa = min(mutari_scor, key=lambda x: x.scor)

    # actualizez scorul „tatalui” = scorul „fiului” ales
    stare.scor = stare.stare_aleasa.scor
    return stare


""" Algoritmul AlphaBeta """


def alpha_beta(alpha, beta, stare):
    # Daca am ajuns la o frunza a arborelui, adica:
    # - daca am expandat arborele pana la adancimea maxima permisa
    # - sau daca am ajuns intr-o configuratie finala de joc
    if stare.adancime == 0 or stare.tabla_joc.final():
        # calculam scorul frunzei apeland "estimeaza_scor"
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # Conditia de retezare:
    if alpha >= beta:
        return stare  # este intr-un interval invalid, deci nu o mai procesez

    # Calculez toate mutarile posibile din starea curenta (toti „fiii”)
    stare.mutari_posibile = stare.genereaza_mutari_posibile()

    if stare.j_curent == Joc.JMAX:
        scor_curent = float('-inf')  # scorul „tatalui” de tip MAX

        # pentru fiecare „fiu” de tip MIN:
        for mutare in stare.mutari_posibile:
            # calculeaza scorul fiului curent
            stare_noua = alpha_beta(alpha, beta, mutare)

            # incerc sa imbunatatesc (cresc) scorul si alfa
            # „tatalui” de tip MAX, folosind scorul fiului curent
            if scor_curent < stare_noua.scor:
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if alpha < stare_noua.scor:
                alpha = stare_noua.scor
                if alpha >= beta:  # verific conditia de retezare
                    break  # NU se mai extind ceilalti fii de tip MIN

    elif stare.j_curent == Joc.JMIN:
        scor_curent = float('inf')  # scorul „tatalui” de tip MIN

        # pentru fiecare „fiu” de tip MAX:
        for mutare in stare.mutari_posibile:
            stare_noua = alpha_beta(alpha, beta, mutare)

            # incerc sa imbunatatesc (scad) scorul si beta
            # „tatalui” de tip MIN, folosind scorul fiului curent
            if scor_curent > stare_noua.scor:
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if beta > stare_noua.scor:
                beta = stare_noua.scor
                if alpha >= beta:  # verific conditia de retezare
                    break  # NU se mai extind ceilalti fii de tip MAX

    # actualizez scorul „tatalui” = scorul „fiului” ales
    stare.scor = stare.stare_aleasa.scor

    return stare


def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()
    if(final):

        clear()
        print()
        print("GAME OVER!")

        if (final == "remiza"):
            print("Remiza!")
        else:
            print("A castigat " + final + "!")

        return True

    return False


def main():
    # preiau timpul in milisecunde inainte de inceperea jocului
    start_game_time = int(round(time.time() * 1000))
    exit = False

    # initializare algoritm
    raspuns_valid = False
    while not raspuns_valid:
        tip_algoritm = input(
            "Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-Beta\n ")
        if tip_algoritm in ['1', '2']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")

    # initializare metoda de estimare a scorului
    raspuns_valid = False
    while not raspuns_valid:
        estimare_scor = input(
            "\nMetoda de estimare a scorului pentru starile nefinale? (raspundeti cu 1 sau 2)\n 1.Diferenta numarului pieselor ramase pe tabla pentru fiecare jucator\n 2.Diferenta numarului pozitiilor de capturare corespunzatoare fiecarui jucator\n ")
        if estimare_scor in ['1', '2']:
            Joc.estimare_scor = estimare_scor
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")

    # initializare ADANCIME_MAX
    raspuns_valid = False
    while not raspuns_valid:
        n = input(
            "\nNivel de dificultate? (raspundeti cu 1, 2 sau 3)\n1.Usor\n2.Mediu\n3.Greu\n")
        if n.isdigit():
            n = int(n)
            if n in range(1, 4):
                if n == 1:
                    Stare.ADANCIME_MAX = Joc.NIVEL_USOR
                elif n == 2:
                    Stare.ADANCIME_MAX = Joc.NIVEL_MEDIU
                else:
                    Stare.ADANCIME_MAX = Joc.NIVEL_GREU
                raspuns_valid = True
            else:
                print("\nNumarul introdus trebuie sa fie cuprins intre 1 - 3!")
        else:
            print("\nTrebuie sa introduceti un numar!")

    # initializare jucatori
    # vizualizarea fireasca tablei:
    # jucatorul JMIN - userul, indiferent de culoarea aleasa (alb sau negru), va avea piesele pozitionate intotdeauna in partea de jos a tablei
    # in timp ce jucatorul JMAX - calculatorul va avea piesele pozitionate intotdeauna in partea de sus a tablei

    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = input("\nDoriti sa jucati cu a sau cu n?\n").lower()
        if (Joc.JMIN in ['a', 'n']):
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie a sau n.")
    Joc.JMAX = 'a' if Joc.JMIN == 'n' else 'n'

    time.sleep(1)
    clear()
    print()
    print()
    print()
    print("************************ Loading game ************************")
    print()
    print()
    print()
    time.sleep(2)
    clear()

    # initializare tabla
    tabla_curenta = Joc()
    print("\nTabla initiala")
    print(str(tabla_curenta))

    print()
    input("Apasati tasta enter pentru a merge mai departe!")
    clear()

    if Joc.JMIN == 'n':
        print("\nFaceti prima miscare!")
        print(str(tabla_curenta))

    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, 'n', Stare.ADANCIME_MAX)

    while True:
        if (stare_curenta.j_curent == Joc.JMIN):
            # muta jucatorul JMIN, pozitionat intotdeauna in josul tablei

            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))

            print("\n\nEste randul dumneavoastra! Trebuie sa faceti o mutare!")

            piesa_valida = False
            mutare_valida = False
            detalii_mutare = {
                "tip_mutare": "unknown",
                "directie_i": 0,
                "directie_j": 0
            }

            while not piesa_valida:
                try:
                    print("\nPiesa de mutat:")
                    linie = int(input("linie="))
                    coloana = int(input("coloana="))

                    if (linie in range(0, 8) and coloana in range(0, 8)):
                        if (linie, coloana) in stare_curenta.tabla_joc.coordonate_piese_JMIN:
                            if stare_curenta.tabla_joc.pozitie_de_avansare(linie, coloana, Joc.SUS) or stare_curenta.tabla_joc.pozitie_de_capturare(linie, coloana, Joc.SUS):
                                piesa_valida = True
                            else:
                                print(
                                    f'Din pozitia ({linie}, {coloana}) nu se mai poate face nicio mutare!')
                        else:
                            print(
                                f'Pe pozitia ({linie}, {coloana}) nu exista nicio piesa de culoare {Joc.JMIN}!')
                    else:
                        print(
                            "Linie sau coloana invalida (trebuie sa fie unul dintre numerele 0 - 7.")

                except ValueError:
                    print("Linia si coloana trebuie sa fie numere intregi")

            while not mutare_valida:
                try:
                    print("\nNoua pozitie:")
                    linie_noua = int(input("linie="))
                    coloana_noua = int(input("coloana="))

                    if (linie_noua in range(0, 8) and coloana_noua in range(0, 8)):
                        if stare_curenta.este_mutare_valida(linie, coloana, linie_noua, coloana_noua, detalii_mutare):
                            mutare_valida = True
                        else:
                            print(
                                f'Piesa din pozitia ({linie}, {coloana}) nu poate fi mutata in pozitia ({linie_noua}, {coloana_noua})!')
                    else:
                        print(
                            "Linie sau coloana invalida (trebuie sa fie unul dintre numerele 0 - 7.")

                except ValueError:
                    print("Linia si coloana trebuie sa fie numere intregi")

            # dupa iesirea din while sigur am valide atat linia si coloana, cat si linia_noua si coloana_noua
            # deci pot plasa simbolul pe "tabla de joc" in pozitia corespunzatoare conform detaliilor mutarii
            if detalii_mutare["tip_mutare"] == "avansare_simpla":

                # print(f'Avansare simpla din pozitia ({linie}, {coloana}) in pozitia ({linie_noua}, {coloana_noua})')

                if stare_curenta.tabla_joc.configuratie_tabla[linie][coloana].islower() and (linie_noua == 0 or linie_noua == Joc.NR_LINII - 1):
                    stare_curenta.tabla_joc.configuratie_tabla[linie_noua][
                        coloana_noua] = stare_curenta.tabla_joc.configuratie_tabla[linie][coloana].upper()
                else:
                    stare_curenta.tabla_joc.configuratie_tabla[linie_noua][
                        coloana_noua] = stare_curenta.tabla_joc.configuratie_tabla[linie][coloana]

                stare_curenta.tabla_joc.configuratie_tabla[linie][coloana] = Joc.GOL
                stare_curenta.tabla_joc.coordonate_piese_JMIN.remove(
                    (linie, coloana))
                stare_curenta.tabla_joc.coordonate_piese_JMIN.append(
                    (linie_noua, coloana_noua))

            elif detalii_mutare["tip_mutare"] == "avansare_in_capturare":

                deplasare_linie = detalii_mutare["directie_i"]
                deplasare_coloana = detalii_mutare["directie_j"]

                while True:

                    # print(f'Avansare in capturare din pozitia ({linie}, {coloana}) in pozitia ({linie_noua}, {coloana_noua})')

                    linie_mijloc = linie + deplasare_linie
                    coloana_mijloc = coloana + deplasare_coloana

                    piesa_de_mutat = stare_curenta.tabla_joc.configuratie_tabla[linie][coloana]
                    stare_curenta.tabla_joc.configuratie_tabla[linie][coloana] = Joc.GOL
                    stare_curenta.tabla_joc.coordonate_piese_JMIN.remove(
                        (linie, coloana))
                    stare_curenta.tabla_joc.coordonate_piese_JMIN.append(
                        (linie_noua, coloana_noua))
                    stare_curenta.tabla_joc.configuratie_tabla[linie_mijloc][coloana_mijloc] = Joc.GOL
                    stare_curenta.tabla_joc.coordonate_piese_JMAX.remove(
                        (linie_mijloc, coloana_mijloc))

                    if piesa_de_mutat.islower() and (linie_noua == 0 or linie_noua == Joc.NR_LINII - 1):
                        # dama ajunsa pe linie terminala devine rege si capturarea se opreste
                        stare_curenta.tabla_joc.configuratie_tabla[linie_noua][coloana_noua] = piesa_de_mutat.upper(
                        )
                        break
                    else:
                        stare_curenta.tabla_joc.configuratie_tabla[linie_noua][coloana_noua] = piesa_de_mutat

                    # genereaza noile capturari posibile ale lui JMIN
                    linie = linie_noua
                    coloana = coloana_noua
                    capturari_posibile = stare_curenta.tabla_joc.genereaza_capturari_posibile(
                        linie, coloana, deplasare_linie, deplasare_coloana)
                    if len(capturari_posibile) == 0:
                        break

                    print(
                        f'\nDin pozitia ({linie}, {coloana}) se impune o noua capturare.')
                    print(stare_curenta.tabla_joc)

                    print("Alegeti coordonatele de deplasare:")
                    for capturare in capturari_posibile:
                        print(capturare["coordonate"])
                    print()

                    capturare_valida = False
                    while not capturare_valida:
                        try:
                            linie_noua = int(input("linie="))
                            coloana_noua = int(input("coloana="))

                            if (linie_noua in range(0, 8) and coloana_noua in range(0, 8)):
                                capturare_gasita = None
                                for capturare in capturari_posibile:
                                    if capturare["coordonate"] == (linie_noua, coloana_noua):
                                        capturare_gasita = capturare
                                        break
                                if capturare_gasita is not None:
                                    capturare_valida = True
                                else:
                                    print(
                                        f'Coordonatele alese nu se afla in lista capturarilor valide din pozitia ({linie}, {coloana})!')
                            else:
                                print(
                                    "Linie sau coloana invalida (trebuie sa fie unul dintre numerele 0 - 7.")

                        except ValueError:
                            print("Linia si coloana trebuie sa fie numere intregi")

                    # dupa iesirea din while, am sigur valide coordonatele unde trebuie mutata piesa in capturare din pozitia (linie, coloana) in pozitia (linie_noua, coloana_noua)
                    # si directiile de deplasare
                    deplasare_linie = capturare_gasita["directie_i"]
                    deplasare_coloana = capturare_gasita["directie_j"]

                print("\nCapturare incheiata!")

            Joc.NR_MUTARI_JMIN += 1

            print()
            raspuns = input(
                "Apasati tasta enter pentru a merge mai departe sau tastati EXIT pentru a iesi!\n")
            if raspuns.lower() == "exit":
                exit = True
                break
            clear()

            # afisarea starii jocului in urma mutarii utilizatorului
            print("\nTabla dupa mutarea jucatorului")
            print(str(stare_curenta))

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Jucatorul a gandit timp de " +
                  str(t_dupa-t_inainte)+" milisecunde.")

            print()
            raspuns = input(
                "Apasati tasta enter pentru a merge mai departe sau tastati EXIT pentru a iesi!\n")
            if raspuns.lower() == "exit":
                exit = True
                break
            clear()

            # testez daca jocul a ajuns intr-o stare finala
            # si afisez un mesaj corespunzator in caz ca da
            if (afis_daca_final(stare_curenta)):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()

        # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator

            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == '1':
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm==2
                stare_actualizata = alpha_beta(-500, 500, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc

            Joc.NR_MUTARI_JMAX += 1

            clear()
            print("\nTabla dupa mutarea calculatorului")
            print(str(stare_curenta))

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " +
                  str(t_dupa-t_inainte)+" milisecunde.")

            if (afis_daca_final(stare_curenta)):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()

    if exit == True:
        clear()
        print("\nGAME EXITED!")

    print()
    print("SCOR:")
    print(f'Jucatorul a capturat {12 - len(stare_curenta.tabla_joc.coordonate_piese_JMAX)} piese     vs.    Calculatorul a capturat {12 - len(stare_curenta.tabla_joc.coordonate_piese_JMIN)} piese!')

    print("\nMutari:")
    print(f'Jucator ({Joc.NR_MUTARI_JMIN} mutari efectuate)     vs.     Calculator ({Joc.NR_MUTARI_JMAX} mutari efectuate)!')

    # preiau timpul in milisecunde la finalul jocului
    end_game_time = int(round(time.time() * 1000))
    print("\nTIMP:")
    print("Jocul a durat timp de " +
          str(end_game_time-start_game_time)+" milisecunde.")


if __name__ == "__main__":
    main()


'''
    Metode de estimare a scorului pentru starile nefinale 
        1. Diferenta dintre numarul de piese ramase pe tabla pentru jucatorul JMAX si numarul de piese ramase pe tabla pentru jucatorul JMIN.
          Functia de estimare ordoneaza starile in functie de cat de prielnice ii sunt lui MAX (cu cat diferenta este mai mare, 
          cu atat JMAX are mai multe piese pe tabla in comparatie cu JMIN si, ca urmare, mai multe sanse de castig.

        2. Diferenta dintre numarul de piese aflate in pozitie de capturare ale lui JMAX si numarul de piese aflate in pozitie de capturare ale lui JMIN;
           o piesa se afla in pozitie de capturare daca la mutarea curenta poate captura cel putin o piesa a adversarului.
           Functia de estimare ordoneaza starile in functie de cat de prielnice ii sunt lui MAX (cu cat diferenta este mai mare, 
           cu atat JMAX are mai multe piese in pozitie de capturare in comparatie cu JMIN si, ca urmare, are mai multe sanse de a captura piesele adversarului,
           deci mai multe sanse de castig.

        3. Diferenta dintre valoarea totala estimata a tablei lui JMAX si valoarea totala estimata a tablei lui JMIN (neimplementat).
           Valoarea tablei unui jucator se estimeaza in functie de numarul pieselor ramase si de "insemnatatea" acestora.
              Se aduna:
                - 3 puncte pentru fiecare pion aflat in "casa" (primele trei linii din zona jucatorului - JMIN zona jos, JMAX zona sus)
                - 7 puncte pentru fiecare pion avansat din casa
                - 10 puncte pentru fiecare rege
           Functia de estimare ordoneaza starile in functie de cat de prielnice ii sunt lui MAX (cu cat diferenta este mai mare, 
           cu atat JMAX are o tabla mai valoroasa in comparatie cu cea a lui JMIN si, ca urmare, mai multe piese in pozitii strategice,
           deci mai multe sanse de castig.
'''
