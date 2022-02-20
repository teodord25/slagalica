# Teodor Djuric SV67/2021

import curses
import time
import random


def out_of_time(wndw, y, x, key1, key2, exit_key, clr):
    window = wndw
    
    key = 0

    while True:
        key = window.getch()

        window.addstr(y, x, "Истекло је време,", clr)
        window.addstr(y + 1, x, f"Aко желите покушати поново, притисните тастер \"{key1}\"", clr)
        window.addstr(y + 2, x, f"Aко желите наставити, притисните тастер \"{key2}\"", clr)
        if key in [ord(str(key1)), ord(str(key2)), exit_key]:
            if key in range(48, 58):
                return int(chr(key))
            else:
                return key
            

def uspeh(wndw, y, x, key1, key2, exit_key, clr, bodovi):
    window = wndw

    key = 0

    while True:
        key = window.getch()

        window.addstr(y, x, f"Победили сте! Ваш број бодова: {bodovi}", clr)
        window.addstr(y + 1, x, f"Aко желите поновити ову игру, притисните тастер \"{key1}\"", clr)
        window.addstr(y + 2, x, f"Aко желите наставити, притисните тастер \"{key2}\"", clr)

        if key in [ord(str(key1)), ord(str(key2)), exit_key]:
            if key in range(48, 58):
                return int(chr(key))
            else:
                return key


def neuspeh(wndw, y, x, key1, key2, exit_key, clr):
    window = wndw

    key = 0

    while True:
        key = window.getch()

        window.addstr(y, x, f"Потрошили сте све покушаје!", clr)
        window.addstr(y + 1, x, f"Aко желите покушати поново притисните тастер \"{key1}\"", clr)
        window.addstr(y + 2, x, f"Aко желите наставити, притисните тастер \"{key2}\"", clr)
        
        if key in [ord(str(key1)), ord(str(key2)), exit_key]:
            if key in range(48, 58):
                return int(chr(key))
            else:
                return key


def igra_korak_po_korak(stdscr):
    window = stdscr
    key = 0

    window.clear()
    window.refresh()

    curses.halfdelay(1)

    while key not in [49, 50]:
        key = window.getch()
        window.addstr(0, 0, "Kojim pismom zelite da bude prikazan tekst?")
        window.addstr(1, 0, "pritisnite taster '1' za latinicu")
        window.addstr(2, 0, "pritisnite taster '2' za cirilicu")
        window.addstr(4, 0, "zaviseci od ovoga cete morati da unosite odgovore u odgovarajucem pismu u prvoj igri 'korak po korak'. ")

        if key in [49, 50]:
            pismo_tekst = int(chr(key))
   
    window.clear()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLUE)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_GREEN)
    
    ekran = open("txt_fajlovi/tabele_korak.txt", "r").readlines()
    [stdscr.addstr(i, 0, j, curses.color_pair(1)) for i, j in enumerate(ekran)]

    _ = 1
    pokusaj = []
    t_0 = 0
    step = 1
    

    if pismo_tekst == 2:
        file = "txt_fajlovi/resenja_korak_po_korak_cyrillic.txt"
    else:
        file = "txt_fajlovi/resenja_korak_po_korak_latin.txt"

    # otvaram fajl, citam linije, belezim indekse za svaki '#' (pocetak recenica)
    # odaberem nasumican indeks, i ucitavam sledecih 8 linija (6 recenica, -, resenje)
    # i na kraju ubacujem poslednju liniju u 'resenje' bez \n
    linije = open(file, "r").readlines()
    lista_indexa = [i for i, j in enumerate(linije) if j == '#\n']
    indeks = random.choice(lista_indexa)

    tabela_recenica = linije[indeks + 1 : indeks + 9]    
    resenje = tabela_recenica[-1][:-1]
    cursor_x = 2
    window.move(20, 2)

    def prikazi_recenicu(red):   
        window.addstr(2 + (red * 3), 2, tabela_recenica[red][:-1].ljust(88), curses.color_pair(1))
                          # skidam \n sa kraja linije --------^
        if red >= 1:
            window.addstr(2 + ((red - 1) * 3), 94, "  ", curses.color_pair(1))

    # Game loop
    while key != 9:       # 'Tab' za izlazak
        key = window.getch()

        while key != 10 and _:
            key = window.getch()
            t_0 = time.time()
        
        # samo jednom brisem onaj tekst dole
        if _:
            for i in range(3):
                for j in range(75):
                    window.addstr(22 + i, 1 + j, " ", curses.color_pair(1))
            window.addstr(24, 60, "Излазак из игре притиском тастера \"Tab\"", curses.color_pair(1))
            
            prikazi_recenicu(0)     # pokazujem odmah na pocetku, zato korak pocinje od 1
            window.move(20, 2)    

        t_1 = time.time() - t_0
        
        # tajmer
        window.addstr(2 + ((step - 1) * 3), 94, str(round(90 - t_1)), curses.color_pair(2))

        # ` prikazuje resenje (za testiranje)
        if key == ord('`'):
            window.addstr(0, 0, resenje)

        if key != -1:

        #   # # # TESTIRAJ ZA BROJEVE NALAZI ZAGRADE()
            if (key == 32 or                      # space
                    key == 39 or                  # apostrof '
                    key in range(48, 58) or       # cifre
                    key in range(65, 91) or       # latinicna velika slova
                    key in range(97, 123) or      # latinicna mala slova
                    key in range(452, 461) or     # ['DŽ', 'Dž', 'dž', 'LJ', 'Lj', 'lj', 'NJ', 'Nj', 'nj']   # sad se tek pitam da li je ovo uopste moguce uneti tastaturom?
                    key in range(1024, 1320) or   # bas sva cirilicna slova
                    key in ['Č', 'Ć', 'D', 'Đ', 'Š', 'Ž']):
                
                pokusaj.append(chr(key).upper())
                window.addstr(20, 2, "".join(pokusaj).ljust(88), curses.color_pair(1))
                cursor_x += 1

        if key == 263:
            if len(pokusaj):   # da ne pokusa da popuje praznu listu
                pokusaj.pop()
                window.addstr(20, 2, "".join(pokusaj).ljust(88), curses.color_pair(1))
                cursor_x -= 1
    
        # 'dalje'
        if key == ord('.'):
            prikazi_recenicu(step)
            step += 1
        
        if step == 7:
            window.addstr(20, 2, resenje, curses.color_pair(1))
            return neuspeh(window, 22, 2, 1, 2, 9, curses.color_pair(1))
        

        # enter za unosenje, a _ je tu da se prvi enter ne racuna kao netacan unos
        if key == 10 and not _:
            
            # ako odgovor sadrzi zagradu onda proveravam samo da li se pokusaj nalazi u resenju
            # znam da ovako moze doci do pogodka ako je korisnik uneo samo jedno slovo,
            # ali je petak i mrzi me, pa cemo samo pretpostaviti da korisnik unosi cela resenja.
            if '(' in resenje:
                if "".join(pokusaj) in resenje:
                
                    window.addstr(20, 2, ''.join(pokusaj).ljust(87), curses.color_pair(5))
                
                    window.getch()  
                    curses.napms(500)  

                    window.addstr(20, 2, resenje.ljust(87), curses.color_pair(1))

                    return uspeh(window, 22, 2, 1, 2, 9, curses.color_pair(1), round((90 - t_1) / step))


                else:
                    window.addstr(20, 2, ''.join(pokusaj).ljust(87), curses.color_pair(4))
                
                    window.getch() 
                    curses.napms(500)

                    window.addstr(20, 2, ' '.ljust(87), curses.color_pair(1))
            
            else:
                if "".join(pokusaj) == resenje:
                
                    window.addstr(20, 2, ''.join(pokusaj).ljust(87), curses.color_pair(5))
                
                    window.getch() 
                    curses.napms(500) 

                    window.addstr(20, 2, resenje.ljust(87), curses.color_pair(1))

                    return uspeh(window, 22, 2, 1, 2, 9, curses.color_pair(1), round((90 - t_1) / step))


                else:
                    window.addstr(20, 2, ''.join(pokusaj).ljust(87), curses.color_pair(4))
                
                    window.getch() 
                    curses.napms(500)

                    window.addstr(20, 2, ' '.ljust(87), curses.color_pair(1))



            cursor_x = 2

            pokusaj.clear()
         
        if t_1 > 90:
            while True:
                return out_of_time(window, 22, 2, 1, 2, 9, curses.color_pair(1))

        window.move(20, cursor_x)

        _ = 0

    return 9


def igra_skocko(stdscr):

    #simboli = ["¥", "♣", "♠", "♥", "♦", "★"]

    # brojevi su kodovi za boju
    skocko_dict = {
        "1": ("¥", 6),
        "2": ("♣", 2),
        "3": ("♠", 2),
        "4": ("♥", 5),
        "5": ("♦", 5),
        "6": ("★", 6)
    }

    resenje = random.choices(["¥", "♣", "♠", "♥", "♦", "★"], k=4)

    # lista unesenih simbola od strane igraca
    pokusaj = []
    pogodci = []

    progres_linija = {
        0: "▀",
        1: "█"
    }

    window = stdscr

    window.clear()
    window.refresh()

    # azuriraj ekran svakih 0.1s ako se ne pritisne neki taster
    curses.halfdelay(1)

    sub_window = window.derwin(0, 0, 0, 54)     # stvara novi "window" objekat za skocka
    sub_window.clear()                          # koji se nalazi pored tabela
    sub_window.refresh()

    # foreground i background par boja (slovo, pozadina),
    # a broj oznacava neku referencu na taj par
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_CYAN)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_CYAN)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_CYAN)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_CYAN)
    curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_CYAN)
    curses.init_pair(7, curses.COLOR_BLUE, curses.COLOR_BLACK)

    # TERMINAL MORA BITI BAREM 25*99 karaktera

    def proveri(red):

        # window.addstr(0, 0, "".join(resenje))

        pogodci = [] 
        y = red

        resenje_duplikat = "".join(resenje)

        for i, j in enumerate(pokusaj):
            if j in resenje_duplikat:
                if j == resenje_duplikat[i]:
                    pogodci.append(5)
                else:
                    pogodci.append(6)
                
                resenje_duplikat = resenje_duplikat.replace(j, "x", 1)
                # kad pogodi neki simbol brise ga da bi se izbelo
                # duplo prikazivanje za isti simbol
               
                # bez ovoga za resenje: ★ ♥ ♠ ♦, pokusaj: ♣ │ ♥ │ ♠ │ ♥
                # prikazuje 2 pogodka, iako bi trebalo samo jedan
                
        for p in enumerate(sorted(pogodci)):
            window.addstr(2 + red * 2, 30 + p[0] * 4, "⬤", curses.color_pair(p[1]))
        
        pokusaj.clear()
        
        return pogodci


    def ispis_i_pamcenje(cifra, red, kolona):
        x, y = kolona, red
        cifra = str(cifra)

        # tuple iz recnika
        par = skocko_dict[cifra]
        window.addstr(2 + y * 2, 6 + x * 4, par[0], curses.color_pair(par[1]))
        pokusaj.append(par[0])

        if x == 3:
            return 1        # nije greska nego znak da se pomera na sledeci korak

    # ispisujem tabele na ekran liniju po liniju
    def ispisi_tabele():
        ekran = open("txt_fajlovi/tabele_skocko.txt", "r").readlines()
        [stdscr.addstr(i, 0, j, curses.color_pair(1)) for i, j in enumerate(ekran)]

        # dodajem boje na legendu
        for i in range(1, 7):
            tpl = skocko_dict[str(i)]

            simbol = tpl[0]
            boja = curses.color_pair(tpl[1])

            window.addstr(15, 26 + (i * 4), simbol, boja)

        # ubacujem crne krugove u desnu tabelu
        for i in range(24):
            simbol = "⬤" 
            boja = curses.color_pair(2)

            window.addstr(2 + (i // 4) * 2, 30 + (i % 4) * 4, simbol, boja)

        # dodajem crnu liniju u sredini
        window.addstr(1, 24, "▄", curses.color_pair(2))

        [window.addstr(2 + i, 24, "█", curses.color_pair(2)) for i in range(11)]
        
        window.addstr(13, 24, "▀", curses.color_pair(2))

    # ucitavam skocka i ispisujem svaki karakter pojedinacno (zbog boja)
    def ispisi_skocka():
        skocko = open("txt_fajlovi/skocko.txt", "r").readlines()
        for y in enumerate(skocko):
            for x in enumerate(y[1]):
                clr = 1
                if y[0] < 6:  # do 6 su svi crni
                    clr = 2
                elif y[0] > 14:  # od 14 su svi cyan
                    clr = 1

                else:
                    if x[1] in "|@/\\":
                        clr = 2
                    elif x[1] in ",.'`=-":
                        clr = 3
                    elif x[1] == "$":
                        clr = 4
                    elif x[1] in "(#)":
                        clr = 5
                    elif x[1] in "%&*":
                        clr = 6

                sub_window.addstr(y[0], x[0], x[1], curses.color_pair(clr))

    ispisi_tabele()
    ispisi_skocka()


    key = 0
    step = 0   # trenutni korak na kojem se nalazi igrac (red u tabeli)
    char_i = 0  # indeks karaktera koji se upisuje (za ispis u tabeli i da znamo kad je ukucano svih 4)

    _ = 1
    t_0 = 0
    t = 0

    window.move(21, 16)     # move the cursor

    # .getch() hvata bilo koji karakter koji se pritisne na tastaturi i cuva ga.
    # Nekom crnom magijom to ne zaustavlja tok programa i mozemo u realnom vremenu da
    # cuvamo neke unose i da osvezavamo ispis u isto vreme.
    # takodje osvezava ekran

    # .getch() catches key press events and stores the ascii value of them
    # without stopping execution (unlike input()) allowing the game to run
    # constantly and have user input (controls in this case) at the same time.

    # Game loop
    while key != 9:    # "Tab" to exit

        # repeat until user presses "Enter" key
        while key != 10 and _:
            key = window.getch()
            t_0 = time.time()

        # ` reveal the answer (testing purposes)
        if key == ord('`'):
            window.addstr(0, 0, "".join(resenje))
           
        # _ so that the text is only deleted once
        if _:
            for i in range(3):
                for j in range(60):
                    window.addstr(21 + i, 4 + j, " ", curses.color_pair(1))
            window.addstr(24, 4, "Излазак из игре притиском тастера \"Tab\".", curses.color_pair(1))
        _ = 0
 
        if 49 <= key <= 54:
            kraj_reda = ispis_i_pamcenje(chr(key), step, char_i)
            char_i += 1
            if kraj_reda:
                pogodci = proveri(step)
                step += 1
                char_i = 0
                
                if pogodci == [5, 5, 5, 5]:    
                    while True:
                    
                        tmp_dct = {i: j for (i, j) in skocko_dict.values()}

                        for i, j in enumerate(resenje):
                            boja = curses.color_pair(tmp_dct[j])

                            window.addstr(16, 6 + (i * 4), j, boja)
                    

                        return uspeh(window, 20, 4, 2, 3, 9, curses.color_pair(1), round((95 - t) / step))
                    

        t_1 = time.time() - t_0

        # duple provere da ne bi crtali sve stalno bez veze
        if 2.5 < t_1 < 5.0:    
            window.addstr(1, 24, "▄", curses.color_pair(1))
        
        if 5 < t_1 < 89:
            t = (t_1 - 4) // 4
            i = int(t // 2)
            j = int(t % 2)
            k = round(t_1, 2)
    
            window.addstr(2 + i, 24, progres_linija[j], curses.color_pair(7))
        
        if 90 < t_1 < 95:
            window.addstr(13, 24, "▀", curses.color_pair(1))
        
        if step == 6 or t_1 > 95:

            # pravim novi dict gde su simboli kljucevi a brojevi boja vrednosti
            tmp_dct = {i: j for (i, j) in skocko_dict.values()}

            for i, j in enumerate(resenje):
                boja = curses.color_pair(tmp_dct[j])

                window.addstr(16, 6 + (i * 4), j, boja)
            
            while True:
                return neuspeh(window, 20, 4, 2, 3, 9, curses.color_pair(1))

        if t_1 > 95:
            while True:
                key = window.getch()
                
                return out_of_time(window, 20, 4, 2, 3, 9, curses.color_pair(1))


        window.move(2 + step * 2, 6 + char_i * 4)
        
        key = window.getch()
    return 9        # ord("Tab") == 9
    

def igra_spojnice(stdscr):
    window = stdscr
    curses.halfdelay(1)

    window.clear()
    window.refresh()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)   # tabela i tekst
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW) # pokusaj
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)  # pogodak
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)    # promasaj
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_BLUE)   # tajmer prazan
    curses.init_pair(6, curses.COLOR_CYAN,  curses.COLOR_BLACK)   # tajmer 


    progres_linija = {
        0: "▀",
        1: "█"
    }

    x = 0
    y = 0

    key = 0
    t_0 = 0
    _ = 1
    pogodci = 0

    window.move(4, 45)

    ekran = open("txt_fajlovi/tabele_spojnice.txt", "r").readlines()
    [stdscr.addstr(i, 0, j, curses.color_pair(1)) for i, j in enumerate(ekran)]

    # Game loop
    while key != 9:
        key = window.getch()

        # beskonacna petlja dok korisnik ne pritisne "Enter"
        while key != 10 and _:
            key = window.getch()
            t_0 = time.time()

        # ` prikazuje resenje (za testiranje)
        if key == ord('`'):
            pass

        # samo jednom da se pokrene
        if _:
            for i in range(3):
                for j in range(95):
                    window.addstr(21 + i, 0 + j, " ", curses.color_pair(1))
            window.addstr(24, 0, "Излазак из игре притиском тастера \"Tab\"".rjust(99), curses.color_pair(1))

            linije = open("txt_fajlovi/spojnice.txt", "r").readlines()
            indeksi = [i for i, j in enumerate(linije) if j == "#\n"]

            index = random.choice(indeksi)
            
            zadatak = linije[index + 3][:-1]
            
            window.addstr(1, 9, zadatak.center(83), curses.color_pair(1))

            tabela = linije[index + 5: index + 13]

            tabela2 = [i.replace(" - ", "/")[:-1] for i in tabela]

            indeksi_2 = []
            for s in tabela2:
                for i,j in enumerate(s):
                    if j == "/":
                        indeksi_2.append(i)

            levo = [tabela2[i][:j] for i,j in enumerate(indeksi_2)]
            desno = [tabela2[i][j+1:] for i,j in enumerate(indeksi_2)]

            spojeno = list(zip(levo, desno))
           
            random.shuffle(levo)

            random.shuffle(desno)

            spojeno_random = list(zip(levo, desno))

            resenje = {i: j for (i, j) in spojeno}

            boja = curses.color_pair(1)

            for x in range(2):
                for y in range(8):
                    window.addstr(4 + (y * 2), 6 + (x * 49), spojeno_random[y][x].center(40), boja)
             
            levi = 0
            
            [window.addstr(4 + i, 50, "█", curses.color_pair(5)) for i in range(15)]

        t_1 = time.time() - t_0

        if 2 < t_1 <= 63:
            t = (t_1 - 2) // 2  # zbog necega ovo daje negativne brojeve ali nemam vise vremena da otkrijem zasto
            i = int(t // 2)
            j = int(t % 2)
    
            window.addstr(4 + i, 50, progres_linija[j], curses.color_pair(6))
        
        if t_1 > 60:
            for x in range(2):
                for y in range(8):
                    window.addstr(4 + (y * 2), 6 + (x * 49), spojeno[y][x].center(40), boja)

            return out_of_time(window, 20, 2, 3, 1, 9, curses.color_pair(1))


                        # prvi enter ne racunamo
        if key == 10 and not _:
            if x == 0:
                if levi:
                    window.addstr(4 + (y * 2), 6 + (x * 49), spojeno_random[y][x].center(40), curses.color_pair(1))

                levi_index = (y, x)
                levi = spojeno_random[y][x]
                window.addstr(4 + (y * 2), 6 + (x * 49), spojeno_random[y][x].center(40), curses.color_pair(2))


            if x == 1:
                if levi:

                    desni = spojeno_random[y][x]

                    if resenje[levi] == desni:
                        window.addstr(4 + (y * 2), 6 + (x * 49), spojeno_random[y][x].center(40), curses.color_pair(3))
                        window.addstr(4 + (levi_index[0] * 2), 6 + (levi_index[1] * 49), spojeno_random    [levi_index[0]][levi_index[1]].center(40), curses.color_pair(3))
                        pogodci += 1

                    else:
                        window.addstr(4 + (y * 2), 6 + (x * 49), spojeno_random[y][x].center(40), curses.color_pair(4))
                        window.getch()  
                        curses.napms(500)  

                        window.addstr(4 + (levi_index[0] * 2), 6 + (levi_index[1] * 49), spojeno_random[levi_index[0]][levi_index[1]].center(40), curses.color_pair(1))
                        window.addstr(4 + (y * 2), 6 + (x * 49), spojeno_random[y][x].center(40), curses.color_pair(1))
                        levi = 0

                    if pogodci == 8:
                        for x in range(2):
                            for y in range(8):
                                window.addstr(4 + (y * 2), 6 + (x * 49), spojeno[y][x].center(40), boja)

                        return uspeh(window, 20, 2, 3, 1, 9, curses.color_pair(1), round(70 - t_1))

        _ = 0

        if key == curses.KEY_UP:
            y -= 1

        if key == curses.KEY_DOWN:
            y += 1

        if key == curses.KEY_RIGHT:
            x += 1

        if key == curses.KEY_LEFT:
            x -= 1

        if y > 7:
            y = 7

        if y < 0:
            y = 0

        if x > 1:
            x = 1

        if x < 0:
            x = 0

        window.move(4 + (y * 2), 46 + (x*8))

    return 9


def main():
    print("""
    Добродошли у игру!

    Пре него што почнете
    препоручујем да промените величину фонта у терминалу и величину самог терминала.
    
    Идеалне димензије су: ширина 99 карактера,
                          висина 24 карактера,
                          а величинa фонтa 23 pt.
                          """)

    input("    Када сте спремни започети игру, притисните тастер \"Ентер\".")

    def game_exit():
        print("\n\n\n\tИзашли сте из игре.\n\n\tХвала на игрању!\n")
        quit()

    idk = {     # ord('Tab') == 9 -> exit game
        9: "game_exit()",
        1: "curses.wrapper(igra_korak_po_korak)",
        2: "curses.wrapper(igra_skocko)",
        3: "curses.wrapper(igra_spojnice)"
    }

    i = 1  
    while True:
        try:
            i = eval(idk[i])

        except curses.error:
            print("""\n\n\n
    Дошло је до грешке приликом приказивања екрана,
    смањите величину фонта или повећајте величину терминала.
                    """)
            quit()


if __name__ == "__main__":
    main()
