'''
Placutele colorate
Algoritmi euristici de explorare a grafurilor (cautarea A-star)

Se considera o grila dreptunghiulara plasata vertical. Aceasta este impartita in locatii patratice
(placute) de diverse culori (culorile vor fi notate cu cate o litera; se presupune ca nu avem mai
multe culori decat litere; literele a-z sunt suficiente).
La fiecare pas se alege o zona de o anumita culoare care are cel putin 3 patratele in componenta
sa. Pentru a forma o astfel de zona patratelele trebuie sa fie vecine pe orizontala si verticala cu
alte patratele din acea zona (nu se considera vecine si pe diagonala). Zona respectiva se elimina
si toate patratelele de deasupra ei "cad" in locurile ramase libere (nu putem avea loc liber care sa
aiba deasupra patratele). In cazul in care avem o coloana libera intre patratele, coloanele din
dreapta se muta la stanga, unind astfel zonele separate de coloana libera. Daca e prima coloana
libera, toate coloanele se muta la stanga cu o pozitie. Coloanele libere vor fi permise doar in
dreapta reprezentarii.

Scopul este sa nu mai avem patratele in grid.

Costul unei mutari este dat 1+(N-K)/N, unde N e numarul total de placute de culoare celor elimitate,
iar K este numarul de placute eliminate in acea mutare. Cu alte cuvinte, cu cat eliminam mai multe
placute cu atat costul e mai mic.
'''

import math
import copy
import time
from operator import itemgetter


def configuratii_identice(tabla1, tabla2):
    for i in range(len(tabla1)):
        for j in range(len(tabla1[i])):
            if tabla1[i][j] != tabla2[i][j]:
                return False
    return True


class Problema:
    NR_LINII = None
    NR_COLOANE = None
    GOL = ' '
    NR_MUTARI = 0
    COST_MUTARI = 0
    EURISTICA = None

    def __init__(self, configuratie_initiala):
        self.configuratie_initiala = configuratie_initiala


class Tabla:
    def __init__(self, configuratie_tabla, h=None):
        self.configuratie_tabla = configuratie_tabla

        # lista ce contine pentru fiecare bloc de cel putin 3 placute identice coordonatele pieselor ce formeaza blocul respectiv
        self.blocuri = self.identifica_blocuri()

        if h is None:
            if Problema.EURISTICA == 1:
                h = self.euristica_1()
            elif Problema.EURISTICA == 2:
                h = self.euristica_2()
            else:
                h = self.euristica_3()
        self.h = h

    def euristica_1(self):
        # neadmisibila: numarul de piese ramase pe tabla
        return self.nr_total_piese()

    def euristica_2(self):
        # numarul de blocuri (de culori diferite) ramase pe tabla
        culori_gasite = set()

        for bloc in self.blocuri:
            culoare_bloc = self.configuratie_tabla[bloc[0][0]][bloc[0][1]]
            culori_gasite.add(culoare_bloc)

        return len(culori_gasite)

    def euristica_3(self):
        # numarul de culori distincte ramase pe tabla
        return len(self.culori_distincte())

    def culori_distincte(self):
        culori = set()
        for linie in self.configuratie_tabla:
            for elem in linie:
                if elem != Problema.GOL:
                    culori.add(elem)
        return culori

    def configuratie_fara_solutii(self):
        culori = self.culori_distincte()
        for culoare in culori:
            if self.nr_piese(culoare) < 3:
                return True
        return False

    def identifica_piese_disponibile(self):
        piese_disponibile = []
        for i in range(len(self.configuratie_tabla)):
            for j in range(len(self.configuratie_tabla[i])):
                if self.configuratie_tabla[i][j] != Problema.GOL:
                    piese_disponibile.append((i, j))
        return piese_disponibile

    def verifica_apartenenta_bloc(self, x, y, culoare, x_vecin, y_vecin, piese_disponibile):
        if x_vecin in range(0, Problema.NR_LINII) and y_vecin in range(0, Problema.NR_COLOANE):
            if (x_vecin, y_vecin) in piese_disponibile:
                if self.configuratie_tabla[x_vecin][y_vecin] == culoare:
                    return True
        return False

    def identifica_blocuri(self):
        blocuri = []

        # lista ce contine coordonatele pieselor disponibile retinute sub forma de tupluri
        piese_disponibile = self.identifica_piese_disponibile()

        while len(piese_disponibile) != 0:
            # extragem o piesa
            coordonate_piesa = piese_disponibile.pop()
            culoare = self.configuratie_tabla[coordonate_piesa[0]
                                              ][coordonate_piesa[1]]

            # lista ce contine coordonatele pieselor din blocul curent
            bloc_curent = []
            bloc_curent.append(coordonate_piesa)

            # coada ce retine piesele ce fac parte din blocul curent si ai caror vecini urmeaza a fi verificati
            piese_de_verificat = []
            piese_de_verificat.append(coordonate_piesa)

            # cat timp exista piese de verificat pentru blocul curent
            while len(piese_de_verificat) != 0:
                coord_piesa_de_verificat = piese_de_verificat.pop(0)
                x_piesa = coord_piesa_de_verificat[0]
                y_piesa = coord_piesa_de_verificat[1]

                # verifica vecin STANGA
                x_vecin = x_piesa + 0
                y_vecin = y_piesa - 1
                if self.verifica_apartenenta_bloc(x_piesa, y_piesa, culoare, x_vecin, y_vecin, piese_disponibile):
                    bloc_curent.append((x_vecin, y_vecin))
                    piese_de_verificat.append((x_vecin, y_vecin))
                    piese_disponibile.remove((x_vecin, y_vecin))

                # verifica vecin DREAPTA
                x_vecin = x_piesa + 0
                y_vecin = y_piesa + 1
                if self.verifica_apartenenta_bloc(x_piesa, y_piesa, culoare, x_vecin, y_vecin, piese_disponibile):
                    bloc_curent.append((x_vecin, y_vecin))
                    piese_de_verificat.append((x_vecin, y_vecin))
                    piese_disponibile.remove((x_vecin, y_vecin))

                # verifica vecin JOS
                x_vecin = x_piesa + 1
                y_vecin = y_piesa + 0
                if self.verifica_apartenenta_bloc(x_piesa, y_piesa, culoare, x_vecin, y_vecin, piese_disponibile):
                    bloc_curent.append((x_vecin, y_vecin))
                    piese_de_verificat.append((x_vecin, y_vecin))
                    piese_disponibile.remove((x_vecin, y_vecin))

                # verifica vecin SUS
                x_vecin = x_piesa - 1
                y_vecin = y_piesa + 0
                if self.verifica_apartenenta_bloc(x_piesa, y_piesa, culoare, x_vecin, y_vecin, piese_disponibile):
                    bloc_curent.append((x_vecin, y_vecin))
                    piese_de_verificat.append((x_vecin, y_vecin))
                    piese_disponibile.remove((x_vecin, y_vecin))

            # s-a terminat de format blocul curent
            if len(bloc_curent) >= 3:
                blocuri.append(bloc_curent)

        return blocuri

    def nr_total_piese(self):
        nr = 0
        for linie in self.configuratie_tabla:
            for elem in linie:
                if elem != Problema.GOL:
                    nr += 1
        return nr

    def nr_piese(self, culoare):
        nr = 0
        for linie in self.configuratie_tabla:
            for elem in linie:
                if elem == culoare:
                    nr += 1
        return nr

    def __str__(self):
        sir = '\n    '

        for i in range(len(self.configuratie_tabla[0])):
            sir += str(i) + '   '
        sir += '\n  '
        for elem in self.configuratie_tabla[0]:
            sir += '____'
        sir += '\n'
        for i in range(len(self.configuratie_tabla)):
            if len(self.configuratie_tabla[i]) == 0:
                break

            sir += '  |'
            for elem in self.configuratie_tabla[i]:
                sir += '   |'
            sir += '\n'
            sir += str(i) + ' |'
            for elem in self.configuratie_tabla[i]:
                sir = sir + ' ' + elem + ' |'
            sir += '\n'
            sir += '  |'
            for elem in self.configuratie_tabla[i]:
                sir += '___|'
            sir += '\n'

        sir = sir + '\nh = ' + str(self.h)
        return sir

    def __repr__(self):
        return f"({self.configuratie_tabla}, h={self.h})"


class TablaParcurgere:

    problema = None

    def __init__(self, tabla, parinte=None, g=0, cost=None, f=None):
        self.tabla = tabla  	# obiect de tip Tabla
        self.parinte = parinte  	# obiect de tip Tabla
        self.g = g
        if f is None:
            self.f = self.g + self.tabla.h
        else:
            self.f = f
        if cost is None:
            cost = 0
        self.cost = cost

    def reconstruieste_drum(self):
        tabla_c = self
        drum = [tabla_c]
        while tabla_c.parinte is not None:
            drum = [tabla_c.parinte] + drum
            tabla_c = tabla_c.parinte
        return drum

    def calculeaza_nr_mutarii_si_cost(self):
        tabla_c = self
        Problema.COST_MUTARI += tabla_c.cost
        while tabla_c.parinte is not None:
            Problema.COST_MUTARI += tabla_c.parinte.cost
            Problema.NR_MUTARI += 1
            tabla_c = tabla_c.parinte

    def contine_in_drum(self, tabla):
        tabla_c = self
        while tabla_c.parinte is not None:
            if configuratii_identice(tabla.configuratie_tabla, tabla_c.tabla.configuratie_tabla):
                return True
            tabla_c = tabla_c.parinte
        return False

    def elimina_bloc(self, bloc):

        configuratie_noua = copy.deepcopy(self.tabla.configuratie_tabla)

        # ordonam  coordonatele pieselor care fac parte din blocul curent
        # crescator dupa coloana si crescator dupa linie
        bloc = sorted(bloc, key=itemgetter(1, 0))

        # pisele de deasupra "cad" in locurile ramase libere
        for i in range(len(bloc)):
            coordonate_piesa = bloc[i]
            linie = coordonate_piesa[0]
            col = coordonate_piesa[1]

            if linie == 0:
                configuratie_noua[linie][col] = Problema.GOL

            for i in range(linie - 1, -1, -1):
                configuratie_noua[linie][col] = configuratie_noua[i][col]
                if configuratie_noua[i][col] == Problema.GOL:
                    break
                configuratie_noua[i][col] = Problema.GOL
                linie = i

        # unim zonele separate de coloane libere
        for col in range(Problema.NR_COLOANE - 2, -1, -1):
            if configuratie_noua[Problema.NR_LINII - 1][col] == Problema.GOL:
                # coloanele din dreapta se muta cu o pozitie spre stanga
                col_stg = col
                for col_dr in range(col + 1, Problema.NR_COLOANE):
                    if configuratie_noua[Problema.NR_LINII - 1][col_dr] == Problema.GOL:
                        break
                    for linie in range(Problema.NR_LINII):
                        configuratie_noua[linie][col_stg] = configuratie_noua[linie][col_dr]
                        configuratie_noua[linie][col_dr] = Problema.GOL
                    col_stg = col_dr

        return configuratie_noua

    def expandeaza(self):
        l_succesori = []

        if self.tabla.configuratie_fara_solutii():
            return l_succesori

        for bloc in self.tabla.blocuri:
            culoare_bloc = self.tabla.configuratie_tabla[bloc[0]
                                                         [0]][bloc[0][1]]

            total_piese_de_culoare = self.tabla.nr_piese(culoare_bloc)

            cost_mutare = round(1 + (total_piese_de_culoare -
                                     len(bloc)) / total_piese_de_culoare, 3)

            configuratie_noua = self.elimina_bloc(bloc)

            l_succesori.append((Tabla(configuratie_noua), cost_mutare))

        return l_succesori

    def test_scop(self):
        for linie in self.tabla.configuratie_tabla:
            for elem in linie:
                if elem != Problema.GOL:
                    return False

        return True

    def __str__(self):
        return f"{self.tabla}, f = {round(self.f, 3)}, g = {self.g}\nCostul mutarii: {self.cost}\n\n"


def str_info(l):
    sir = ""
    for x in l:
        sir += str(x) + "  "
    return sir


def print_succesori(l_succesori):
    if len(l_succesori) == 0:
        print("Configuratie fara solutii!")
    for (succesor, cost) in l_succesori:
        print(succesor)
        print('cost = ', cost, '\n')


def in_lista(l, tabla):
    for i in range(len(l)):
        if configuratii_identice(l[i].tabla.configuratie_tabla, tabla.configuratie_tabla):
            return l[i]
    return None


def a_star():
    tabla_start = TablaParcurgere(Tabla(
        TablaParcurgere.problema.configuratie_initiala))

    if tabla_start.test_scop():
        print("\nGridul este deja vid!")
        fout.write("Gridul este deja vid!\n")
    else:
        open = [tabla_start]
        closed = []

        while len(open) > 0:
            tabla_curenta = open.pop(0)
            closed.append(tabla_curenta)

            if tabla_curenta.test_scop():
                break

            print('\n\nTabla curenta:')
            print(tabla_curenta)

            # l_succesori contine tupluri de tip (Tabla, numar)
            l_succesori = tabla_curenta.expandeaza()

            print('Lista succesorilor:')
            print_succesori(l_succesori)

            for (tabla_succesor, cost_succesor) in l_succesori:
                # "tabla_curenta" este tatal, "tabla_succesor" este fiul curent

                # daca fiul nu e in drumul dintre tabla_initiala si tatal sau (adica nu se creeaza un circuit)
                if (not tabla_curenta.contine_in_drum(tabla_succesor)):

                    # calculez valorile g si f pentru "tabla_succesor" (fiul)
                    g_succesor = tabla_curenta.g + cost_succesor
                    f_succesor = g_succesor + tabla_succesor.h  # g-ul fiului + h-ul fiului

                    # verific daca "tabla_succesor" se afla in closed
                    # (si il si sterg, returnand tabla stearsa in tabla_parcg_veche
                    tabla_parcg_veche = in_lista(closed, tabla_succesor)
                    tabla_noua = None

                    if tabla_parcg_veche is not None:
                        # "tabla_succesor" e in closed
                        # daca f-ul calculat pentru drumul actual este mai bun (mai mic) decat
                        # f-ul pentru drumul gasit anterior (f-ul tablei aflate in lista closed)
                        # atunci scot tabla din lista closed
                        # actualizez parintele, g si f
                        # si apoi voi adauga "tabla_noua" in lista open
                        if (f_succesor < tabla_parcg_veche.f):
                            closed.remove(tabla_parcg_veche)
                            tabla_parcg_veche.parinte = tabla_curenta
                            tabla_parcg_veche.g = g_succesor
                            tabla_parcg_veche.f = f_succesor
                            tabla_parcg_veche.cost = cost_succesor
                            # setez "tabla_noua", care va fi adaugat apoi in open
                            tabla_noua = tabla_parcg_veche

                    else:
                        # daca nu e in closed, verific daca "tabla_succesor" se afla in open
                        tabla_parcg_veche = in_lista(open, tabla_succesor)

                        if tabla_parcg_veche is not None:
                            # "tabla_succesor" e in open
                            # daca f-ul calculat pentru drumul actual este mai bun (mai mic) decat
                            # f-ul pentru drumul gasit anterior (f-ul tablei aflate in lista open)
                            # atunci scot tabla din lista open
                            # (pentru ca modificarea valorilor f si g imi va strica sortarea listei open)
                            # actualizez parintele, g si f
                            # si apoi voi adauga "tabla_noua" in lista open (la noua pozitie corecta in sortare)
                            if (f_succesor < tabla_parcg_veche.f):
                                open.remove(tabla_parcg_veche)
                                tabla_parcg_veche.parinte = tabla_curenta
                                tabla_parcg_veche.g = g_succesor
                                tabla_parcg_veche.f = f_succesor
                                tabla_parcg_veche.cost = cost_succesor
                                tabla_noua = tabla_parcg_veche

                        else:  # cand "tabla_succesor" nu e nici in closed, nici in open
                            tabla_noua = TablaParcurgere(
                                tabla_succesor, tabla_curenta, g_succesor, cost_succesor)
                            # se calculeaza f automat in constructor

                    if tabla_noua:
                        # inserare in lista sortata crescator dupa f
                        # (si pentru f-uri egale descrescator dupa g)
                        i = 0
                        while i < len(open):
                            if open[i].f < tabla_noua.f:
                                i += 1
                            else:
                                while i < len(open) and open[i].f == tabla_noua.f and open[i].g > tabla_noua.g:
                                    i += 1
                                break

                        open.insert(i, tabla_noua)

        print("\n------------------ Concluzie -----------------------")
        if len(open) == 0:
            print("Lista open e vida, nu putem obtine gridul vid!\n")
            fout.write("Lista open e vida, nu putem obtine gridul vid!\n")
        else:
            tabla_curenta.calculeaza_nr_mutarii_si_cost()

            print("Drum de cost minim: \n" +
                  str_info(tabla_curenta.reconstruieste_drum()))
            print(
                f"S-au realizat {Problema.NR_MUTARI} mutari cu costul {Problema.COST_MUTARI}!\n")

            fout.write('Euristica_' + str(Problema.EURISTICA))
            fout.write('\n')

            if Problema.EURISTICA == 1:
                fout.write(
                    "Euristica neadmisibila: numarul de piese ramase pe tabla\n")
            elif Problema.EURISTICA == 2:
                fout.write(
                    "Euristica: numarul de blocuri (de culori diferite) ramase pe tabla\n")
            else:
                fout.write(
                    "Euristica: numarul de culori distincte ramase pe tabla\n")

            fout.write("\nDrum de cost minim: \n" +
                       str_info(tabla_curenta.reconstruieste_drum()))
            fout.write(
                f"\nS-au realizat {Problema.NR_MUTARI} mutari cu costul {Problema.COST_MUTARI}!\n")


if __name__ == "__main__":

    fisiere_input = ['input1.txt', 'input2.txt', 'input3.txt', 'input4.txt']

    for i in range(len(fisiere_input)):

        Problema.NR_MUTARI = 0
        Problema.COST_MUTARI = 0

        # preiau timpul in milisecunde de dinainte de rularea fisierului
        t_inainte = int(round(time.time() * 1000))

        print("\n\n******* Se ruleaza fisierul de intrare " +
              fisiere_input[i] + '! *******')

        # initializare metoda de estimare a scorului
        raspuns_valid = False
        while not raspuns_valid:
            euristica = input(
                "\nEuristica folosita? (raspundeti cu 1, 2 sau 3)\n1. Numarul de piese ramase pe tabla (neadmisibila)\n2. Numarul de blocuri (de culori diferite) ramase pe tabla\n3. Numarul de culori distincte ramase pe tabla\n")
            if euristica in ['1', '2', '3']:
                Problema.EURISTICA = int(euristica)
                raspuns_valid = True
            else:
                print("Nu ati ales o varianta corecta.")

        fin = open(fisiere_input[i], 'r')
        fisier_output = 'output' + \
            str(i + 1) + '_euristica' + str(Problema.EURISTICA) + '.txt'
        fout = open(fisier_output, 'w')

        lines = fin.read().split('\n')

        configuratie_initiala = []

        for line in lines:
            if len(line):
                configuratie_initiala.append([])
                for elem in line:
                    configuratie_initiala[len(
                        configuratie_initiala) - 1].append(elem)

        Problema.NR_LINII = len(configuratie_initiala)
        Problema.NR_COLOANE = len(configuratie_initiala[0])

        problema = Problema(configuratie_initiala)
        TablaParcurgere.problema = problema
        a_star()

        print('Rezultatul rularii se afla in fisierul ' + fisier_output + '!')

        # preiau timpul de terminare a rularii
        t_dupa = int(round(time.time() * 1000))
        print("Algoritmul a rulat timp de " +
              str(t_dupa-t_inainte)+" milisecunde.")
        fout.write("\nAlgoritmul a rulat timp de " +
                   str(t_dupa-t_inainte)+" milisecunde.")

        fin.close()
        fout.close()


'''
EURISTICI:

    1. Numarul de piese ramase pe tabla.
       Euristica nu este admisibila, deoarece supraestimeaza costul (valoarea efectiva h).
       Aproximeaza ca fiecare piesa va avea cost de eliminare 1, doar ca, pentru a fi eliminate, 
       piesele vor fi grupate in blocuri de cel putin 3 (ceea ce va reduce efectiv valoarea reala h fata de cea supraestimata de euristica).


    2. Numarul de blocuri (de culori diferite) ramase pe tabla.
       Consideram costul minim necesar din configuratia curenta pana la finalul jocului ca fiind numarul blocurilor de culori distincte 
       (fiecare bloc avand asociat costul minim de spargere de 1). Euristica este admisibila (nu supraestimeaza costul, deorece 
       fiecare culoare distincta avand asociat cel putin un bloc va trebui eliminata cu un cost cel putin egal cu 1), dar nu este consistenta.
       Contraexemplu consistenta:  
       
            3 <= 1 + 0 (Fals) dupa eliminare a

                  0   1   2   3   4   5   
                ________________________
                |   |   |   |   |   |   |
              0 |   |   |   | g |   |   |
                |___|___|___|___|___|___|
                |   |   |   |   |   |   |
              1 | p | p | g | g | g |   |
                |___|___|___|___|___|___|
                |   |   |   |   |   |   |
              2 | p | a | a | a | a | a |
                |___|___|___|___|___|___|
                |   |   |   |   |   |   |
              3 | a | a | a | a | a | a |
                |___|___|___|___|___|___|
                |   |   |   |   |   |   |
              4 | a | a | v | a | v | a |
                |___|___|___|___|___|___|
                |   |   |   |   |   |   |
              5 | v | a | v | a | v | a |
                |___|___|___|___|___|___|

                  0   1   2   3   4   5   
                ________________________
                |   |   |   |   |   |   |
              0 |   |   |   |   |   |   |
                |___|___|___|___|___|___|
                |   |   |   |   |   |   |
              1 |   |   |   |   |   |   |
                |___|___|___|___|___|___|
                |   |   |   |   |   |   |
              2 |   |   |   |   |   |   |
                |___|___|___|___|___|___|
                |   |   |   |   |   |   |
              3 | p |   | g |   | g |   |
                |___|___|___|___|___|___|
                |   |   |   |   |   |   |
              4 | p |   | v | g | v |   |
                |___|___|___|___|___|___|
                |   |   |   |   |   |   |
              5 | v | p | v | g | v |   |
                |___|___|___|___|___|___|


    3. Numarul de culori distincte ramase pe tabla.
       Euristica este admisibila, deoarece fiecare culoare distincta va trebui pana la final eliminata,
       iar costul pentru a sparge un bloc este cel putin egal cu 1, deci functia aleasa (avand cost egal cu 1 asociat fiecarei piese de culoare distincta) 
       nu ajunge sa supraestimeze valoarea reala h.

       Contraexemplu consistenta:

            3 <= 1 + 3 (Fals)  dupa eliminare a

                  0   1   2   3   
                ________________
                |   |   |   |   |
              0 | c | c | b | b |
                |___|___|___|___|
                |   |   |   |   |
              1 | a | a | a | a |
                |___|___|___|___|
                |   |   |   |   |
              2 | a | a | a | a |
                |___|___|___|___|
                |   |   |   |   |
              3 | c | a | a | b |
                |___|___|___|___|
                |   |   |   |   |
              4 | c | a | b | a |
                |___|___|___|___|


                   0   1   2   3   
                ________________
                |   |   |   |   |
              0 |   |   |   |   |
                |___|___|___|___|
                |   |   |   |   |
              1 |   |   |   |   |
                |___|___|___|___|
                |   |   |   |   |
              2 | c |   |   | b |
                |___|___|___|___|
                |   |   |   |   |
              3 | c |   | b | b |
                |___|___|___|___|
                |   |   |   |   |
              4 | c | c | b | a |
                |___|___|___|___|

'''
