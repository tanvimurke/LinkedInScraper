import time
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
file_path = '/Users/tanvimurke/Desktop/output.txt' 
def updateFile(section):
    
    ul = section.find('ul',{'class': 'pvs-list'}) 
    listofLi = ul.find_all('li',{'class':'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column'}) #list of all job exp/education
    for li in listofLi:
        #case 1: first 3 rows
        listofdiv = li.find_all('div',{'class':'display-flex flex-column full-width align-self-center'})
        for div in listofdiv:
            listofExp = div.find_all('div',{'class':'display-flex flex-row justify-space-between'})
            for exp in listofExp:
                listofSpan = exp.find_all('span',{'class': 'visually-hidden'})
                with open(file_path, 'a') as file: 
                    file.write('\n')
                    for s in listofSpan:
                        text = s.text
                        file.write(text)
                        file.write('\n')
        #case2 : desc
            listofDes = div.find_all('div',{'class':'pvs-list__outer-container'})
            for des in listofDes:
                listofSpanDes = des.find_all('span',{'class': 'visually-hidden'})
                with open(file_path, 'a') as file:
                    file.write("Description")
                    file.write('\n')
                    for desSpa in listofSpanDes:
                        text = desSpa.text
                        file.write(text)
                        file.write('\n')
                break    #to remove duplicates    
                                  

def chrome(headless=False):
    # support to get response status and headers
    print("Script started")
    d = webdriver.DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'performance': 'ALL'}
    opt = webdriver.ChromeOptions()
    if headless:
        opt.add_argument("--headless")
    opt.add_experimental_option('excludeSwitches', ['enable-logging'])
    opt.add_argument("--disable-popup-blocking")
    browser = webdriver.Chrome(executable_path=r'/Users/tanvimurke/Documents/chromedriver_mac64/chromedriver', options=opt,desired_capabilities=d)
    browser.implicitly_wait(10)
    print("Chrome Connected")
    #browser.set_page_load_timeout(10) 
    return browser
start = time.time()
## Pass True if you want to hide chrome browser
browser = chrome(True)

browser.get('https://www.linkedin.com/uas/login')
browser.implicitly_wait(3)
#print("after wait for login")
file = open('config.txt')
lines = file.readlines()
username = lines[0]
password = lines[1]

elementID = browser.find_element_by_id('username')
#print("element id is ",elementID)
elementID.send_keys(username)
elementID = browser.find_element_by_id('password')
elementID.send_keys(password)
elementID.submit()

print("Logged in successfully")

info = []

links = ['https://www.linkedin.com/in/lee-branstetter-93966717/', 
         'https://www.linkedin.com/in/tanvi-murke/'
        ]

for link in links:
    browser.get(link)
    print("Scraping Link: ",link)
    browser.implicitly_wait(1)
    def scroll_down_page(speed=8):
        #print("inside scroll")
        current_scroll_position, new_height= 0, 1
        while current_scroll_position <= new_height:
            current_scroll_position += speed
            browser.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
            new_height = browser.execute_script("return document.body.scrollHeight")

    scroll_down_page(speed=8)

    src = browser.page_source
    soup = BeautifulSoup(src, 'lxml')
 
    # Get Name of the person
    try:
        vlaue = soup.find('h1', {'class': 'text-heading-xlarge inline t-24 v-align-middle break-words'})
        name = vlaue.get_text(strip=True)
        #print("Name:", name)
        with open(file_path, 'a') as file:
            file.write('\n')
            file.write("**************************************************************************")
            file.write('\n')
            file.write("Name: ")
            file.write(name)
            file.write('\n')
    except:
        name = None

    #Get Job and Education

    section_tags = soup.findAll('section', {'class': 'artdeco-card ember-view relative break-words pb3 mt2'}) #to get all the sections
    for section in section_tags:
        divs = section.find_all('div')
        for div in divs:
            id_tag = div.get('id')
            if id_tag == "experience":
                updateFile(section)
                break 
            if id_tag == "education": 
                updateFile(section)
                break

end = time.time() 
print("The time of execution of above program is :",(end-start), "seconds")           
print(".................Done Scraping!.................")
browser.quit()

