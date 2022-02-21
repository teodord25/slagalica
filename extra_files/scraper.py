import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def main():
    login_url = "https://slagalica.tv/korisnik/prijava"
    driver = webdriver.Firefox()
    # requires geckodriver (?),
    # which can be installed using the included bash script
    # "geckodriver-install.sh" courtesy of github user brunoao86

    driver.get(login_url)
    driver.find_element(By.ID, "openid").send_keys("dizutfaggqceculkew@mrvpm.net")  # courtesy of 10minutemail
    driver.find_element(By.ID, "lozinka").send_keys("dizutfaggqceculkew@mrvpm.net")

    driver.find_element(By.CLASS_NAME, "button").click()

    time.sleep(15)

    for month in range(1, 3):
        for day in range(1, 28):
            month = str(month).zfill(2)
            day = str(day).zfill(2)

            date = f"2021-{month}-{day}"

            driver.find_element(By.XPATH, f"//a[@title='Igraj igre za {date}']").click()
            driver.find_element(By.LINK_TEXT, f"Spojnice").click()
            driver.find_element(By.CLASS_NAME, "playbutton").click()

            task_text = f"{driver.find_element(By.CLASS_NAME, 'minititle').text}\n"

            driver.find_element(By.ID, "kraj").click()

            table_ = driver.find_element(By.CLASS_NAME, "ui-dialog-content").text
            answer_table = table_[20:-71]

            with open("../txt_files/spojnice.txt", "a") as f:
                f.write("#\n")
                f.write(f"2016-{month}-{day}\n\n")
                f.write(f"{task_text}\n")
                f.write(f"{answer_table}\n")

            driver.find_element(By.XPATH, "//a[@href='/korisnik/']").click()

    driver.quit()


if __name__ == "__main__":
    main()
