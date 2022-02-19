import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def main():
    login_url = "https://slagalica.tv/korisnik/prijava"
    driver = webdriver.Firefox()
    # tu je potreban neki geckodriver da bi se pokrenuo firefox
    # script ./geckodriver-install.sh github korisnika brunoao86
    # radi na Arch linuxu 2021-11-23

    # krecemo se na login stranicu, ubacujemo potrebne podatke i klikcemo "prijavi se"
    driver.get(login_url)
    driver.find_element(By.ID, "openid").send_keys("dizutfaggqceculkew@mrvpm.net")  # courtesy of 10minutemail
    driver.find_element(By.ID, "lozinka").send_keys("dizutfaggqceculkew@mrvpm.net")

    driver.find_element(By.CLASS_NAME, "button").click()

    # treba sacekati da se potpuno ucita stranica, to bi trebao selenium da radi vec sam od sebe,
    # ali zbog necega nije tako, pokusao sam i sa EC.presence_of_element_located, ali ne radi ni to,
    # ovako je malo glupo ali barem radi
    time.sleep(15)

    for mesec in range(1, 3):
        for dan in range(1, 28):
            mesec = str(mesec).zfill(2)
            dan = str(dan).zfill(2)

            datum = f"2021-{mesec}-{dan}"

            # klikcemo na sve strane dok ne stignemo do igre
            driver.find_element(By.XPATH, f"//a[@title='Igraj igre za {datum}']").click()
            driver.find_element(By.LINK_TEXT, f"Spojnice").click()
            driver.find_element(By.CLASS_NAME, "playbutton").click()

            # cuvamo tekst zadatka
            text_zadatka = f"{driver.find_element(By.CLASS_NAME, 'minititle').text}\n"

            # klikcemo na dugme "kraj" da bismo prikazali rezultate
            driver.find_element(By.ID, "kraj").click()

            # cuvamo tekst tabele i formatiramo ga
            tabela_ = driver.find_element(By.CLASS_NAME, "ui-dialog-content").text
            tabela_resenja = tabela_[20:-71]

            with open("../txt_fajlovi/spojnice.txt", "a") as f:
                f.write("#\n")
                f.write(f"2016-{mesec}-{dan}\n\n")
                f.write(f"{text_zadatka}\n")
                f.write(f"{tabela_resenja}\n")

            driver.find_element(By.XPATH, "//a[@href='/korisnik/']").click()

    driver.quit()


if __name__ == "__main__":
    main()
