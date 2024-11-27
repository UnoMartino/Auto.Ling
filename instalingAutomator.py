from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import json
from sys import platform
import random


#declare variables
def variables():
    global usernames
    global passwords
    global driver
    global lastTwoWords
    global slowInternetMode
    global randomWordTimeMode

    usernames = []
    passwords = []
    options = webdriver.FirefoxOptions()
    slowInternetMode = False
    randomWordTimeMode = False

    if platform == "linux" or platform == "linux2":
        driver = webdriver.Firefox(options=options)
        driver.get("https://google.com/")
    elif platform == "darwin":
        driver = webdriver.Firefox(options=options)
        driver.get("https://google.com/")
    elif platform == "win32":
        options.binary_location = "Mozilla Firefox\\firefox.exe"
        driver = webdriver.Firefox(options=options)
        driver.get("https://google.com/")
    lastTwoWords = []


# get secrets
def getSecrets():
    file = open("./secrets.txt", "r")
    secretsFile = file.readlines()
    file.close()
    for i in secretsFile:
        i = i.split(":")
        print(i)
        usernames.append(i[0])
        i[1] = i[1].replace("\n", "")
        print(i)
        passwords.append(i[1])


def login(id):
    driver.get("https://instaling.pl/")
    sleep(2)
    assert "Insta.Ling" in driver.title
    try:
        cookiesButton = driver.find_element(By.CSS_SELECTOR, "body > div.fc-consent-root > div.fc-dialog-container > div.fc-dialog.fc-choice-dialog > div.fc-footer-buttons-container > div.fc-footer-buttons > button.fc-button.fc-cta-consent.fc-primary-button")
        cookiesButton.click()
    except:
        pass
    loginButton = driver.find_element(By.CSS_SELECTOR, "#navbar > a.btn.navbar-profile.p-0.m-0.pr-2 > div.btn.btn-secondary.btn-login.d-none.d-sm-none.d-lg-block.mr-3")
    loginButton.click()
    username = driver.find_element(By.NAME, "log_email")
    sleep(random.uniform(2.1, 4.8))
    username.clear()
    username.send_keys(usernames[id])
    password = driver.find_element(By.NAME, "log_password")
    sleep(random.uniform(2.1, 4.8))
    password.clear()
    password.send_keys(passwords[id])
    sleep(random.uniform(2.1, 4.8))
    password.send_keys(Keys.RETURN)
    # loginButton = driver.find_element(By.CSS_SELECTOR, "#main-container > div:nth-child(3) > form > div > div:nth-child(3) > button")
    # loginButton.click()

def logout():
    driver.get("https://instaling.pl/")
    button = driver.find_element(By.CSS_SELECTOR, "#navbar > a.btn.navbar-profile.p-0.m-0.pr-2 > div.login-img > div:nth-child(2) > img")
    button.click()
    sleep(1)
    button = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/p[10]/a")
    button.click()
    sleep(1)


# save words
def saveWords():
    driver.get("https://instaling.pl/")
    button = driver.find_element(By.CSS_SELECTOR, "#navbar > a.btn.navbar-profile.p-0.m-0.pr-2 > div.login-img > div:nth-child(2) > img")
    button.click()
    sleep(1)
    button = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/p[5]/a")
    button.click()
    sleep(1)
    button = driver.find_element(By.XPATH, "/html/body/div/div[3]/div/a[1]/h4")
    button.click()
    sleep(1)
    button = driver.find_element(By.XPATH, '//*[@id="show_words"]')
    button.click()
    sleep(1)

    rows = len(driver.find_elements(By.XPATH, '//*[@id="assigned_words"]/tr'))

    wordsTuple = []

    for r in range(2, rows+1):
        value = driver.find_element(By.XPATH, '//*[@id="assigned_words"]/tr['+str(r)+']/td['+str(1)+']').text
        germanWord = value  
        value = driver.find_element(By.XPATH, '//*[@id="assigned_words"]/tr['+str(r)+']/td['+str(2)+']').text
        polishWord = value
        wordsTuple.append({"germanWord": germanWord, "polishWord": polishWord})

    with open('words.json', 'w') as outfile:
        json.dump(wordsTuple, outfile)

    print(wordsTuple)

def doOneWord():
    # read words from json
    with open('words.json') as json_file:
        words = json.load(json_file)

    polishWord = driver.find_element(By.CSS_SELECTOR, "#question > div.caption > div.translations").text
    print("polishWord: ", polishWord)

    #log last two words in table
    if len(lastTwoWords) == 2:
        lastTwoWords.pop(0)
    lastTwoWords.append(polishWord)

    # check if last two words are the same and if so, delete first occurence from json and append it to the end
    if len(lastTwoWords) == 2:
        if lastTwoWords[0] == lastTwoWords[1]:
            for i in words:
                if i["polishWord"] == lastTwoWords[0]:
                    words.remove(i)
                    words.append(i)
                    break
            print("removed and appended")
            with open('words.json', 'w') as outfile:
                json.dump(words, outfile)

    for i in words:
        if i["polishWord"] == polishWord:
            germanWord = i["germanWord"]
            print("germanWord: ", germanWord)
            answer = driver.find_element(By.CSS_SELECTOR, "#answer")
            answer.send_keys(germanWord)
            if randomWordTimeMode:
                sleep(random.uniform(2.1, 4.8))
            answer.send_keys(Keys.RETURN)
            sleep(0.5 if not slowInternetMode else 1)
            button = driver.find_element(By.CSS_SELECTOR, "#next_word")
            button.click()
            sleep(0.5 if not slowInternetMode else 1)
            return
        
    print("not found")
    button = driver.find_element(By.CSS_SELECTOR, "#check > h4")
    button.click()
    sleep(0.5 if not slowInternetMode else 1)
    germanWord = driver.find_element(By.CSS_SELECTOR, "#word").text
    print("germanWord: ", germanWord)
    appendWord(polishWord, germanWord)
    button = driver.find_element(By.CSS_SELECTOR, "#next_word")
    button.click()
    sleep(0.5 if not slowInternetMode else 1)


def knowNewWord():
    button = driver.find_element(By.CSS_SELECTOR, "#know_new")
    button.click()
    sleep(0.5 if not slowInternetMode else 1)
    button = driver.find_element(By.CSS_SELECTOR, "#skip > h4:nth-child(1)")
    button.click()
    sleep(0.5 if not slowInternetMode else 1)

def doSession():
    driver.get("https://instaling.pl/")
    button = driver.find_element(By.CSS_SELECTOR, "#navbar > a.btn.navbar-profile.p-0.m-0.pr-2 > div.login-img > div:nth-child(2) > img")
    button.click()
    sleep(1)
    button = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/p[1]/a")
    button.click()
    sleep(1)

    try:
        button = driver.find_element(By.CSS_SELECTOR, "#continue_session_button > h4")
        button.click()
        print("Continue session")
        sleep(1)
    except:
        print("New session")
        button = driver.find_element(By.CSS_SELECTOR, "#start_session_button > h4:nth-child(1)")
        button.click()
        sleep(1)

    while True:
        try: 
            doOneWord()
        except:
            try:
                knowNewWord()
            except:
                break
            

def appendWord(polishWord, germanWord):
    json_file = open('words.json', "r")
    words = json.load(json_file)
    json_file.close()
    words.append({"germanWord": germanWord, "polishWord": polishWord})
    with open('words.json', 'w') as outfile:
        json.dump(words, outfile)


