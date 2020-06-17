from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from time import sleep, gmtime, strftime
import labbot_telegram
import credentials


def check_exists_by_xpath(seldriver, xpath):
    try:
        seldriver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def main():
    # preliminary settings
    # Using Firefox to access web
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path=r'/usr/local/Cellar/geckodriver/0.26.0/bin/geckodriver')
    print ("Headless Firefox Initialized")


    # Open the website
    driver.get('https://www.lehrbetrieb.ethz.ch/laborpraktika/uebersicht.view')

    # find and click button
    driver.find_elements_by_xpath("//input[@class='submit' and @value='Start']")[0].click()

    # Log in
    sleep(4)
    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")

    username.send_keys(credentials.username)
    password.send_keys(credentials.password)
    driver.find_element_by_xpath(
        "/html/body/section/div[2]/div[1]/div/div/div[4]/form/fieldset/div[4]/div[1]/div/button").click()

    # go to next page
    sleep(2)
    driver.find_element_by_xpath("/html/body/div[3]/section/section[2]/div/div/div/a").click()

    # edit filter
    sleep(1)
    driver.find_element_by_xpath("/html/body/div[3]/section/section[1]/div[2]/div/form[1]/h3").click()
    sleep(1)
    select_element = Select(driver.find_element_by_xpath("//*[@id='departmentId']"))
    select_element.select_by_visible_text("D-MAVT")
    driver.find_elements_by_xpath("//*[@id='freePlaces1']")[0].click()
    driver.find_elements_by_xpath("//*[@id='applyFilters']")[0].click()
    driver.minimize_window()

    # Scrape page for Labs
    while True:
        currenttime = strftime("%H:%M:%S", gmtime())
        if check_exists_by_xpath(driver, "//*[@class='praktikumHeader']"):
            labs = driver.find_elements_by_xpath("//*[@class='praktikumHeader']")
            labs_list = ["Available labs:"]
            for lab in labs:
                head, sep, tail = lab.text.partition("anmeldbar")
                labs_list.append(head)

            labs_string = '\n'.join(labs_list)
            print(currenttime, "labs available. sending messages")

            for chat in credentials.chat_ids:
                labbot_telegram.telegram_send(labs_string, chat, credentials.token)

        else:
            print(currenttime, "No labs available")

        sleep(5 * 60)
        driver.refresh()


if __name__ == "__main__":
    main()
