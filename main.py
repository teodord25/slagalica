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
            

def success(wndw, y, x, key1, key2, exit_key, clr, points):
    window = wndw

    key = 0

    while True:
        key = window.getch()

        window.addstr(y, x, f"Победили сте! Ваш број бодова: {points}", clr)
        window.addstr(y + 1, x, f"Aко желите поновити ову игру, притисните тастер \"{key1}\"", clr)
        window.addstr(y + 2, x, f"Aко желите наставити, притисните тастер \"{key2}\"", clr)

        if key in [ord(str(key1)), ord(str(key2)), exit_key]:
            if key in range(48, 58):
                return int(chr(key))
            else:
                return key


def failure(wndw, y, x, key1, key2, exit_key, clr):
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
            lang_script = int(chr(key))
   
    window.clear()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLUE)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_GREEN)
    
    screen = open("txt_files/tabele_korak.txt", "r").readlines()
    [stdscr.addstr(i, 0, j, curses.color_pair(1)) for i, j in enumerate(screen)]

    _ = 1
    attempt = []
    t_0 = 0
    step = 1

    if lang_script == 2:
        file = "txt_files/resenja_korak_po_korak_cyrillic.txt"
    else:
        file = "txt_files/resenja_korak_po_korak_latin.txt"

    lines = open(file, "r").readlines()
    indicies = [i for i, j in enumerate(lines) if j == '#\n']
    index = random.choice(indicies)

    sentence_table = lines[index + 1: index + 9]
    answer = sentence_table[-1][:-1]
    cursor_x = 2
    window.move(20, 2)

    def show_sentence(row):
        window.addstr(2 + (row * 3), 2, sentence_table[row][:-1].ljust(88), curses.color_pair(1))
        if row >= 1:
            window.addstr(2 + ((row - 1) * 3), 94, "  ", curses.color_pair(1))

    # Game loop
    while key != 9:       # 'Tab' to exit
        key = window.getch()

        while key != 10 and _:
            key = window.getch()
            t_0 = time.time()
        
        if _:
            for i in range(3):
                for j in range(75):
                    window.addstr(22 + i, 1 + j, " ", curses.color_pair(1))
            window.addstr(24, 60, "Излазак из игре притиском тастера \"Tab\"", curses.color_pair(1))
            
            show_sentence(0)  # pokazujem odmah na pocetku, zato korak pocinje od 1
            window.move(20, 2)    

        t_1 = time.time() - t_0

        # timer
        window.addstr(2 + ((step - 1) * 3), 94, str(round(90 - t_1)), curses.color_pair(2))

        # ` show answer (testing)
        if key == ord('`'):
            window.addstr(0, 0, answer)

        if key != -1:
            if (key == 32 or                      # space
                    key == 39 or                  # '
                    key in range(48, 58) or       # digits
                    key in range(65, 91) or       # latin upper
                    key in range(97, 123) or      # latin lower
                    key in range(452, 461) or     # ['DŽ', 'Dž', 'dž', 'LJ', 'Lj', 'lj', 'NJ', 'Nj', 'nj']   # sad se tek pitam da li je ovo uopste moguce uneti tastaturom?
                    key in range(1024, 1320) or   # cyrillic
                    key in ['Č', 'Ć', 'D', 'Đ', 'Š', 'Ž']):
                
                attempt.append(chr(key).upper())
                window.addstr(20, 2, "".join(attempt).ljust(88), curses.color_pair(1))
                cursor_x += 1

        if key == 263:
            if len(attempt):
                attempt.pop()
                window.addstr(20, 2, "".join(attempt).ljust(88), curses.color_pair(1))
                cursor_x -= 1
    
        # 'dalje' next
        if key == ord('.'):
            show_sentence(step)
            step += 1
        
        if step == 7:
            window.addstr(20, 2, answer, curses.color_pair(1))
            return failure(window, 22, 2, 1, 2, 9, curses.color_pair(1))
        
        if key == 10 and not _:
            if '(' in answer:
                if "".join(attempt) in answer:
                
                    window.addstr(20, 2, ''.join(attempt).ljust(87), curses.color_pair(5))
                
                    window.getch()  
                    curses.napms(500)  

                    window.addstr(20, 2, answer.ljust(87), curses.color_pair(1))

                    return success(window, 22, 2, 1, 2, 9, curses.color_pair(1), round((90 - t_1) / step))

                else:
                    window.addstr(20, 2, ''.join(attempt).ljust(87), curses.color_pair(4))
                
                    window.getch() 
                    curses.napms(500)

                    window.addstr(20, 2, ' '.ljust(87), curses.color_pair(1))
            
            else:
                if "".join(attempt) == answer:
                
                    window.addstr(20, 2, ''.join(attempt).ljust(87), curses.color_pair(5))
                
                    window.getch() 
                    curses.napms(500) 

                    window.addstr(20, 2, answer.ljust(87), curses.color_pair(1))

                    return success(window, 22, 2, 1, 2, 9, curses.color_pair(1), round((90 - t_1) / step))

                else:
                    window.addstr(20, 2, ''.join(attempt).ljust(87), curses.color_pair(4))
                
                    window.getch() 
                    curses.napms(500)

                    window.addstr(20, 2, ' '.ljust(87), curses.color_pair(1))

            cursor_x = 2

            attempt.clear()
         
        if t_1 > 90:
            while True:
                return out_of_time(window, 22, 2, 1, 2, 9, curses.color_pair(1))

        window.move(20, cursor_x)

        _ = 0

    return 9


def igra_skocko(stdscr):
    skocko_dict = {
        "1": ("¥", 6),
        "2": ("♣", 2),
        "3": ("♠", 2),
        "4": ("♥", 5),
        "5": ("♦", 5),
        "6": ("★", 6)
    }

    answer = random.choices(["¥", "♣", "♠", "♥", "♦", "★"], k=4)

    attempt = []
    correct = []

    progress_bar = {
        0: "▀",
        1: "█"
    }

    window = stdscr

    window.clear()
    window.refresh()

    # refresh the screen every 0.1s if no key was pressed
    curses.halfdelay(1)

    sub_window = window.derwin(0, 0, 0, 54)
    sub_window.clear()
    sub_window.refresh()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_CYAN)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_CYAN)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_CYAN)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_CYAN)
    curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_CYAN)
    curses.init_pair(7, curses.COLOR_BLUE, curses.COLOR_BLACK)

    def check(row):
        correct = []
        y = row

        answer_copy = "".join(answer)

        for i, j in enumerate(attempt):
            if j in answer_copy:
                if j == answer_copy[i]:
                    correct.append(5)
                else:
                    correct.append(6)
                
                answer_copy = answer_copy.replace(j, "x", 1)
                # whenever a symbol is correctly guessed,
                # "delete it" to avoid counting the same symbol twice

                # e.g. of false positive
                #
                # answer: ★ ♥ ♠ ♦, attempt: ♣ │ ♥ │ ♠ │ ♥
                # this would register 2 hits for the same heart
                
        for p in enumerate(sorted(correct)):
            window.addstr(2 + row * 2, 30 + p[0] * 4, "⬤", curses.color_pair(p[1]))
        
        attempt.clear()
        
        return correct

    def show_attempt(digit, row, column):
        x, y = column, row
        digit = str(digit)

        pair = skocko_dict[digit]
        window.addstr(2 + y * 2, 6 + x * 4, pair[0], curses.color_pair(pair[1]))
        attempt.append(pair[0])

        if x == 3:
            return 1

    def show_tables():
        screen = open("txt_files/tabele_skocko.txt", "r").readlines()
        [stdscr.addstr(i, 0, j, curses.color_pair(1)) for i, j in enumerate(screen)]

        for i in range(1, 7):
            tpl = skocko_dict[str(i)]

            symbol = tpl[0]
            color = curses.color_pair(tpl[1])

            window.addstr(15, 26 + (i * 4), symbol, color)

        for i in range(24):
            symbol = "⬤"
            color = curses.color_pair(2)

            window.addstr(2 + (i // 4) * 2, 30 + (i % 4) * 4, symbol, color)

        window.addstr(1, 24, "▄", curses.color_pair(2))

        [window.addstr(2 + i, 24, "█", curses.color_pair(2)) for i in range(11)]
        
        window.addstr(13, 24, "▀", curses.color_pair(2))

    def show_skocko():
        skocko = open("txt_files/skocko.txt", "r").readlines()
        for y in enumerate(skocko):
            for x in enumerate(y[1]):
                clr = 1
                if y[0] < 6:
                    clr = 2
                elif y[0] > 14:
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

    show_tables()
    show_skocko()

    key = 0
    step = 0
    char_i = 0

    _ = 1
    t_0 = 0
    t = 0

    window.move(21, 16)     # move the cursor
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
            window.addstr(0, 0, "".join(answer))
           
        # _ so that the text is only deleted once
        if _:
            for i in range(3):
                for j in range(60):
                    window.addstr(21 + i, 4 + j, " ", curses.color_pair(1))
            window.addstr(24, 4, "Излазак из игре притиском тастера \"Tab\".", curses.color_pair(1))
        _ = 0
 
        if 49 <= key <= 54:
            row_end = show_attempt(chr(key), step, char_i)
            char_i += 1
            if row_end:
                correct = check(step)
                step += 1
                char_i = 0
                
                if correct == [5, 5, 5, 5]:
                    while True:
                    
                        tmp_dct = {i: j for (i, j) in skocko_dict.values()}

                        for i, j in enumerate(answer):
                            color = curses.color_pair(tmp_dct[j])

                            window.addstr(16, 6 + (i * 4), j, color)

                        return success(window, 20, 4, 2, 3, 9, curses.color_pair(1), round((95 - t) / step))
                    
        t_1 = time.time() - t_0

        if 2.5 < t_1 < 5.0:
            window.addstr(1, 24, "▄", curses.color_pair(1))
        
        if 5 < t_1 < 89:
            t = (t_1 - 4) // 4
            i = int(t // 2)
            j = int(t % 2)
            k = round(t_1, 2)
    
            window.addstr(2 + i, 24, progress_bar[j], curses.color_pair(7))
        
        if 90 < t_1 < 95:
            window.addstr(13, 24, "▀", curses.color_pair(1))
        
        if step == 6 or t_1 > 95:

            # {symbol: color}
            tmp_dct = {i: j for (i, j) in skocko_dict.values()}

            for i, j in enumerate(answer):
                color = curses.color_pair(tmp_dct[j])

                window.addstr(16, 6 + (i * 4), j, color)
            
            while True:
                return failure(window, 20, 4, 2, 3, 9, curses.color_pair(1))

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
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(6, curses.COLOR_CYAN,  curses.COLOR_BLACK)

    progress_bar = {
        0: "▀",
        1: "█"
    }

    x = 0
    y = 0

    key = 0
    t_0 = 0
    _ = 1
    correct = 0

    window.move(4, 45)

    screen = open("txt_files/tabele_spojnice.txt", "r").readlines()
    [stdscr.addstr(i, 0, j, curses.color_pair(1)) for i, j in enumerate(screen)]

    # Game loop
    while key != 9:
        key = window.getch()
        while key != 10 and _:
            key = window.getch()
            t_0 = time.time()

        if key == ord('`'):
            pass

        if _:
            for i in range(3):
                for j in range(95):
                    window.addstr(21 + i, 0 + j, " ", curses.color_pair(1))
            window.addstr(24, 0, "Излазак из игре притиском тастера \"Tab\"".rjust(99), curses.color_pair(1))

            lines = open("txt_files/spojnice.txt", "r").readlines()
            indicies = [i for i, j in enumerate(lines) if j == "#\n"]

            index = random.choice(indicies)
            
            task = lines[index + 3][:-1]
            
            window.addstr(1, 9, task.center(83), curses.color_pair(1))

            table = lines[index + 5: index + 13]

            table2 = [i.replace(" - ", "/")[:-1] for i in table]

            indicies_2 = []
            for s in table2:
                for i,j in enumerate(s):
                    if j == "/":
                        indicies_2.append(i)

            left = [table2[i][:j] for i, j in enumerate(indicies_2)]
            right = [table2[i][j + 1:] for i, j in enumerate(indicies_2)]

            zipped = list(zip(left, right))
           
            random.shuffle(left)

            random.shuffle(right)

            zipped_random = list(zip(left, right))

            answer = {i: j for (i, j) in zipped}

            color = curses.color_pair(1)

            for x in range(2):
                for y in range(8):
                    window.addstr(4 + (y * 2), 6 + (x * 49), zipped_random[y][x].center(40), color)

            left_side = 0
            
            [window.addstr(4 + i, 50, "█", curses.color_pair(5)) for i in range(15)]

        t_1 = time.time() - t_0

        if 2 < t_1 <= 63:
            t = (t_1 - 2) // 2  # zbog necega ovo daje negativne brojeve ali nemam vise vremena da otkrijem zasto
            i = int(t // 2)
            j = int(t % 2)
    
            window.addstr(4 + i, 50, progress_bar[j], curses.color_pair(6))
        
        if t_1 > 60:
            for x in range(2):
                for y in range(8):
                    window.addstr(4 + (y * 2), 6 + (x * 49), zipped[y][x].center(40), color)

            return out_of_time(window, 20, 2, 3, 1, 9, curses.color_pair(1))

        if key == 10 and not _:
            if x == 0:
                if left_side:
                    window.addstr(4 + (y * 2), 6 + (x * 49), zipped_random[y][x].center(40), curses.color_pair(1))

                left_index = (y, x)
                left_side = zipped_random[y][x]
                window.addstr(4 + (y * 2), 6 + (x * 49), zipped_random[y][x].center(40), curses.color_pair(2))

            if x == 1:
                if left_side:

                    right_side = zipped_random[y][x]

                    if answer[left_side] == right_side:
                        window.addstr(4 + (y * 2), 6 + (x * 49), zipped_random[y][x].center(40), curses.color_pair(3))
                        window.addstr(4 + (left_index[0] * 2), 6 + (left_index[1] * 49), zipped_random[left_index[0]][left_index[1]].center(40), curses.color_pair(3))
                        correct += 1

                    else:
                        window.addstr(4 + (y * 2), 6 + (x * 49), zipped_random[y][x].center(40), curses.color_pair(4))
                        window.getch()  
                        curses.napms(500)  

                        window.addstr(4 + (left_index[0] * 2), 6 + (left_index[1] * 49), zipped_random[left_index[0]][left_index[1]].center(40), curses.color_pair(1))
                        window.addstr(4 + (y * 2), 6 + (x * 49), zipped_random[y][x].center(40), curses.color_pair(1))
                        left_side = 0

                    if correct == 8:
                        for x in range(2):
                            for y in range(8):
                                window.addstr(4 + (y * 2), 6 + (x * 49), zipped[y][x].center(40), color)

                        return success(window, 20, 2, 3, 1, 9, curses.color_pair(1), round(70 - t_1))

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
