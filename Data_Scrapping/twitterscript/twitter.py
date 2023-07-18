
import pandas as pd

from selenium import webdriver

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.common.keys import Keys
import time
from webdriver_manager.chrome import ChromeDriverManager
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-popup-blocking")

# options.add_experimental_option("debuggerAddress", "localhost:9222")

from selenium import webdriver
import re

# Set up the Selenium web driver




# Find the search input field and enter your desired search query

file = open('twitter.txt', mode='r')
lines = file.readlines()
n=lines[3].split('|')[1]

driver = webdriver.Chrome(ChromeDriverManager().install(),options=options) # Enter your path here
# fetches the login page
driver.get('https://twitter.com/login')
# adjust the sleep time according to your internet speed
time.sleep(5)

email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@autocomplete="username"]')))
time.sleep(2)
email.send_keys(str(lines[0].split('|')[1]))
time.sleep(2)
try:
 driver.find_element(By.XPATH,'//*[text()="Next"]').click()
except:
  print()
password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@autocomplete="current-password"]')))
time.sleep(2)
password.send_keys(str(lines[1].split('|')[1]))
time.sleep(2)
try:
    driver.find_element(By.XPATH,
        '//*[text()="Log in"]'
    ).click()
except:
 print()

# sends the password to the password input
l='https://twitter.com/home'
time.sleep(5)
driver.get(str(l))
time.sleep(5)
search_input = driver.find_element(By.XPATH,'//input[@data-testid="SearchBox_Search_Input"]')
search_input.send_keys('from:'+str(lines[2].split('|')[1])+')   until:2023-07-16 since:2023-07-09')
search_input.send_keys(Keys.RETURN)  # Press Enter to initiate the search
print('Start scraping...')
time.sleep(10)
tweets = []

k=0
data1 = []

while True:
    tweess1 = ''
    twees2 = ''
    twees3 = ''
    tweess = ''
    print(k)
    try:
        # make = WebDriverWait(driver, 25).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@data-testid="cellInnerDiv"]//article')))

        driver.execute_script('document.getElementsByTagName("article")['+str(k)+'].click()')
    except Exception as e:
        print(e)
        print('break')
        body = driver.find_element(By.TAG_NAME, 'body')
        for _ in range(4):  # Adjust the number of times you want to scroll to load more tweets
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)  # Wait for the page to load
        k=0
        continue
    print('ok')
    body = driver.find_element(By.TAG_NAME, 'body')
    for _ in range(2):  # Adjust the number of times you want to scroll to load more tweets
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)  # Wait for the page to load
    try:
      WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.XPATH,'//*[@class="css-18t94o4 css-1dbjc4n r-1niwhzg r-42olwf r-sdzlij r-1phboty r-rs99b7 r-15ysp7h r-4wgw6l r-1ny4l3l r-ymttw5 r-f727ji r-j2kj52 r-o7ynqc r-6416eg r-lrvibr"]'))).click()
    except :
        print()


    try:
      tweets = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@data-testid="tweetText"]')))
    except:
       print()

    for i in range(1, len(tweets)):
        twees1 = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,
                                                                                      '//*[@data-testid="tweetText"]//..//..//*[@class="css-1dbjc4n r-zl2h9q"]//*[@data-testid="User-Name"]')))
        twees = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@data-testid="tweetText"]')))
        try:
            print(twees1[0].text.strip())
            print(twees[0].text)
            tweess = twees1[0].text.strip()
            tweess1 = twees[0].text
        except:
            print()
        try:
            print(twees1[i].text)
            print(twees[i].text)
            twees2 = twees1[i].text
            twees3 = twees[i].text

        except:
            print()



        link = driver.current_url
        try:  # data dictionary
            record = {
                'Tweeturl': link,
                'Username': str(tweess).replace('Ãª ','') ,
                'Tweet': str(tweess1).replace('Ãª ','') ,
                'ReplyUsername':  str(twees2).replace('Ãª ','') ,
                'Replies':  str(twees3).replace('Ãª ','') ,

            }
            data1.append(record)


        except:
            print()
        p = pd.DataFrame(data1)
        p.to_csv(r'HM.csv',encoding = 'utf-8-sig', index = False)  # Give  file name

        time.sleep(1.5)
    driver.back()
    k+=1
    time.sleep(5)

#




