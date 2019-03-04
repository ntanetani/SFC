from selenium import webdriver
import getpass
import requests
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.options import Options

url = "https://wellness.sfc.keio.ac.jp/v3/index.php?page=top&limit=9999&semester=20185&lang=ja"

html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

span = soup.find_all("td")

state = 0
state2 = 0
sports = []
periods = []
dates = []
currentDate = ""
currentPeriod = ""
currentSport = ""
variousThings = ""

for tag in span:

    try:
        string_ = tag.get("class").pop(0)

        if string_ in "w3-hide-small":
            state = state + 1

            if ((state-1)%5) == 0:
                state2 = state2 + 1
                variousThings = tag.string
                if variousThings != None :
                    currentDate = variousThings
                dates.append(currentDate)

            if ((state-2)%5) == 0:
                variousThings = tag.string
                if variousThings != None :
                    currentPeriod = variousThings
                periods.append(currentPeriod)

            if ((state-3)%5) == 0:
                if "セミエキスパート" in str(tag):
                    currentSport = str(tag).replace('<td class="">', '').replace('<em>*組</em></td>', '').strip()
                    sports.append(str(tag).replace('<td class="">', '').replace('<em>*組</em></td>', '').strip())
                else:
                    currentSport = tag.string
                    sports.append(tag.string)
                print(str(state2)+ ". " + currentDate + " " + currentPeriod+ " " + currentSport)

    except:
        pass


username = input("ログイン名:")
password = getpass.getpass()
chosenNumber = int(input("番号:"))
print(dates[chosenNumber-1] + " " + periods[chosenNumber-1] + " " + sports[chosenNumber - 1])
options = Options()
# ヘッドレスモードを有効にする（次の行をコメントアウトすると画面が表示される）。
#options.add_argument('--headless')
# ChromeのWebDriverオブジェクトを作成する。
browser = webdriver.Chrome(chrome_options=options)

loginUrl= "https://wellness.sfc.keio.ac.jp/v3/index.php?page=top&limit=9999&semester=20185&lang=ja"

browser.get(loginUrl)

userNameField = browser.find_element_by_xpath('//*[@id="maincontents"]/form/div/table/tbody/tr[1]/td/input')
userNameField.send_keys(username)

passwordField = browser.find_element_by_xpath('//*[@id="maincontents"]/form/div/table/tbody/tr[2]/td/input')
passwordField.send_keys(password)

submitButton = browser.find_element_by_xpath('//*[@id="maincontents"]/form/div/table/tbody/tr[3]/td[2]/input')
submitButton.click()

reserveButton = browser.find_element_by_xpath('//*[@id="navbar"]/div/a[1]')
reserveButton.click()

browser.get(browser.current_url + "&limit=9999")

url = browser.current_url

html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

span = soup.find_all("td")

state = 0
sports2 = []
currentDate = ""
currentPeriod = ""
currentSport = ""
variousThings = ""

for tag in span:

    try:
        string_ = tag.get("class").pop(0)

        if string_ in "w3-hide-small":
            state = state + 1

            if ((state-1)%5) == 0:
                variousThings = tag.string
                if variousThings != None :
                    currentDate = variousThings

            if ((state-2)%5) == 0:
                variousThings = tag.string
                if variousThings != None :
                    currentPeriod = variousThings

            if ((state-3)%5) == 0:
                if "セミエキスパート" in str(tag):
                    currentSport = str(tag).replace('<td class="">', '').replace('<em>*組</em></td>', '').strip()
                    sports2.append(str(tag).replace('<td class="">', '').replace('<em>*組</em></td>', '').strip())
                else:
                    currentSport = tag.string
                    sports2.append(tag.string)
                if currentDate == dates[chosenNumber - 1] :
                    if currentPeriod == periods[chosenNumber - 1] :
                        if currentSport == sports[chosenNumber - 1] :
                            break


    except:
        pass

sportState = str(len(sports2))


reserveSportButton = browser.find_element_by_xpath('//*[@id="maincontents"]/div[5]/table/tbody/tr[' + sportState + ']/td[8]/a').get_attribute('href')
browser.get(reserveSportButton)

reserveButton = browser.find_element_by_xpath('//*[@id="maincontents"]/form/p/input[1]')
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
reserveButton.click()

reserveButton = browser.find_element_by_xpath('//*[@id="maincontents"]/form/p/input[1]')
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
reserveButton.click()

print("処理が完了しました")

confirmButton = browser.find_element_by_xpath('//*[@id="navbar"]/div/a[2]')
confirmButton.click()

state = 0
state2 = 0
currentDate2 = ""
currentPeriod2 = ""
currentSport2 = ""
variousThings = ""
reserveState = False

print("予約している授業一覧")
print("---------------------------------")

url = browser.current_url

html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

span = soup.find_all("td")

for tag in span:

    try:
        string_ = tag.get("class").pop(0)

        if string_ in "w3-hide-small":
            state = state + 1

            if ((state-1)%6) == 0:
                state2 = state2 + 1
                variousThings = tag.string
                if variousThings != None :
                    currentDate2 = variousThings

            if ((state-2)%6) == 0:
                variousThings = tag.string
                if variousThings != None :
                    currentPeriod2 = variousThings

            if ((state-3)%6) == 0:
                if "セミエキスパート" in str(tag):
                    currentSport2 = str(tag).replace('<td class="">', '').replace('<em>*組</em></td>', '').strip()
                else:
                    currentSport2 = tag.string
                print(str(state2)+ ". " + currentDate2 + " " + currentPeriod2+ " " + currentSport2)
                if currentDate == currentDate2 :
                    if currentPeriod == currentPeriod2 :
                        if currentSport == currentSport2 :
                            reserveState = True

    except:
        pass

browser.quit()

if reserveState :
    print("予約に成功しました")
else:
    print("予約に失敗しました")
