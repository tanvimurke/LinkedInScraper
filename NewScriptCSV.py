import time
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import re

info = []
file_path = '/Users/tanvimurke/Desktop/output.csv' 
#Name, LinkedIn URL, Job Title, Organization Name, Employment Type, Start Date, End Date, Time Period, Location, Location Type, Job Description, 
#                    School, Degree, Field of Study, Start Date, End Date, Education Description
name = link = title = orgname = emptype = startdate = enddate = period = location = loctype = desc = None


def updateFile(section, sectionType):
    print("inside update")
    #print(section)
    print(sectionType)
    global name , link , title , orgname , emptype , startdate , enddate , period , location , loctype , desc
    ul = section.find('ul',{'class': 'pvs-list'}) 
    #print("**********************")
    #print("ul",ul)
    #artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column
    listofLi = ul.find_all('li',{'class':'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column pvs-list--ignore-first-item-top-padding'}) #list of all job exp/education
    print("listofLi",listofLi)
    for li in listofLi:
        print("inside li",li)
        #case 1: first 3 rows
        listofdiv = li.find_all('div',{'class':'display-flex flex-column full-width align-self-center'})
        for div in listofdiv:
            listofExp = div.find_all('div',{'class':'display-flex flex-row justify-space-between'})
            for exp in listofExp:
                listofSpan = exp.find_all('span',{'class': 'visually-hidden'})

                if listofSpan[0].text is not None:
                    title = listofSpan[0].text
                
                if len(listofSpan) >= 2:
                    secondrow = listofSpan[1].text
                    secondrow_parts = re.split(r'[·.,]', secondrow)
                    if len(secondrow_parts) == 2:
                        orgname = secondrow_parts[0].strip()
                        emptype = secondrow_parts[1].strip()
                    else:
                        orgname = secondrow.strip()
                        emptype = None

                if len(listofSpan) >= 3:
                    thirdrow = listofSpan[2].text
                    thirdrow_parts = re.split(r'[-·]', thirdrow)
                    #thirdrow_parts = [part.strip() for part in thirdrow_parts if part.strip()]  # Remove empty parts
                    if len(thirdrow_parts) >= 3:
                        startdate = thirdrow_parts[0]
                        enddate = thirdrow_parts[1]
                        period = thirdrow_parts[2]
                    elif len(thirdrow_parts) == 2:
                        startdate = thirdrow_parts[0]
                        enddate = thirdrow_parts[1]
                        period = None
                    else:
                        startdate = thirdrow_parts[0]
                        enddate = None
                        period = None
                
                if len(listofSpan) >= 4:
                    fourthrow = listofSpan[3].text
                    fourthrow_parts = re.split(r'[-·]', fourthrow)
                    if len(fourthrow_parts) == 2:
                        location = fourthrow_parts[0].strip()
                        loctype = fourthrow_parts[1].strip()
                    else:
                        location = secondrow.strip()
                        loctype = None
                if sectionType == 'experience':
                    info.append([None, None, title, orgname, emptype, startdate, enddate, period, location, loctype, None, None, None, None, None, None, None])
                elif sectionType == 'education':
                    info.append([None, None, None, None, None, None, None, None, None, None, None, title, orgname, emptype, startdate, enddate, None])
        #case2 : desc
            listofDes = div.find_all('div',{'class':'pvs-list__outer-container'})
            for des in listofDes:
                listofSpanDes = des.find_all('span',{'class': 'visually-hidden'})
                if len(listofSpanDes) >=1:
                    desc = listofSpanDes[0].text
                    if sectionType == 'experience':
                        info.append([None, None, None, None, None, None, None, None, None, None, desc, None, None, None, None, None, None])
                    elif sectionType == 'education':
                        info[-1][-1] = desc
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


links = ['https://www.linkedin.com/in/lee-branstetter-93966717/', 
         'https://www.linkedin.com/in/sumantmurke/',
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
    except:
        name = None
    info.append([name, link, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None])

    #Get Job and Education
    section_tags = soup.findAll('section', {'class': 'artdeco-card ember-view relative break-words pb3 mt2'}) #to get all the sections
    for section in section_tags:
        divs = section.find_all('div')
        for div in divs:
            id_tag = div.get('id')
            if id_tag == "experience":
                sectionType = "experience"
                updateFile(section, sectionType)
                break
            if id_tag == "education": 
                sectionType = "education"
                updateFile(section, sectionType)
                break

end = time.time() 
#info.append([name,title])
#Name, LinkedIn URL, Job Title, Organization Name, Employment Type, Start Date, End Date, Time Period, Location, Location Type, Job Description, 
#                    School, Degree, Field of Study, Start Date, End Date, Education Description

column_names = ["Name", "LinkedIn URL", "Job Title", "Organization Name","Employment Type", "Start Date", "End Date", "Time Period", "Location", "Location Type", "Job Description", "School", "Degree", "Field of Study", "Start Date", "End Date", "Education Description"]
df = pd.DataFrame(info, columns=column_names)
df.to_csv(file_path, index=False)
print("The time of execution of above program is :",(end-start), "seconds")           
print(".................Done Scraping!.................")
browser.quit()

