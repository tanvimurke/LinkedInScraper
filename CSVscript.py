import time
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import re
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

exp_list = []
edu_list = []
exp_desc = []
edu_desc = []
name_list = []

file_path = '/Users/tanvimurke/Desktop/output.csv' 
#Name, LinkedIn URL, Job Title, Organization Name, Employment Type, Start Date, End Date, Time Period, Location, Location Type, Job Description, 
#                    School, Degree, Field of Study, Start Date, End Date, Education Description
name = title = orgname = emptype = startdate = enddate = period = location = loctype = desc = None


def updateFile(section, sectionType, url):
    #print("inside update")
    #print(section, sectionType, url)
    global name , link , title , orgname , emptype , startdate , enddate , period , location , loctype , desc
    ul = section.find('ul',{'class': 'pvs-list'}) 
    listofLi = ul.find_all('li',{'class':'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column pvs-list--ignore-first-item-top-padding'}) #list of all job exp/education
    for li in listofLi:
        #print("inside li")
        #case 1: first 3 rows
        listofdiv = li.find_all('div',{'class':'display-flex flex-column full-width align-self-center'})
        for div in listofdiv:
            listofExp = div.find_all('div',{'class':'display-flex flex-row justify-space-between'})
            for exp in listofExp:
                #print("inside list")
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
                    
                    exp_list.append([url, title, orgname, emptype, startdate, enddate, period, location, loctype])
                    #print("exp listtt")
                    #print([url, title, orgname, emptype, startdate, enddate, period, location, loctype])
                    #info.append([None, None, title, orgname, emptype, startdate, enddate, period, location, loctype, None, None, None, None, None, None, None])
                elif sectionType == 'education':
                    edu_list.append([url, title, orgname, emptype, startdate, enddate,])
                    #info.append([None, None, None, None, None, None, None, None, None, None, None,  None])
        #case2 : desc
            listofDes = div.find_all('div',{'class':'pvs-list__outer-container'})
            for des in listofDes:
                listofSpanDes = des.find_all('span',{'class': 'visually-hidden'})
                if len(listofSpanDes) >=1:
                    desc = listofSpanDes[0].text
                    if sectionType == 'experience':
                        exp_desc.append([url, desc])
                        #info.append([None, None, None, None, None, None, None, None, None, None, desc, None, None, None, None, None, None])
                    elif sectionType == 'education':
                        edu_desc.append([url, desc])
                        #info[-1][-1] = desc
                    break    #to remove duplicates    
                                  

def chrome(headless=False):
    # support to get response status and headers
    print("Script started")
    d = webdriver.DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'performance': 'ALL'}
    opt = webdriver.ChromeOptions()
    time.sleep(10)
    if headless:
        opt.add_argument("--headless")
    opt.add_experimental_option('excludeSwitches', ['enable-logging'])
    opt.add_argument("--disable-popup-blocking")
    browser = webdriver.Chrome(executable_path=r'/Users/tanvimurke/Documents/chromedriver_mac64/chromedriver', options=opt,desired_capabilities=d)
    browser.implicitly_wait(10)
    print("Chrome Connected")
    browser.set_page_load_timeout(30) 
    return browser
start = time.time()
## Pass True if you want to hide chrome browser
browser = chrome(True)

browser.get('https://www.linkedin.com/uas/login')
browser.implicitly_wait(10)
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
time.sleep(10)

links = ['https://www.linkedin.com/in/ruta-d/', 
         'https://www.linkedin.com/in/kaushal-kulkarni-/'
        ]
# links = ['https://www.linkedin.com/in/lee-branstetter-93966717/', 
#          'https://www.linkedin.com/in/sumantmurke/',
#          'https://www.linkedin.com/in/tanvi-murke/'
#         ]


for link in links:
    browser.get(link)
    print("Scraping Link: ",link)
    browser.implicitly_wait(10)
    wait = WebDriverWait(browser, 10)
    # try:
    #     element_present = EC.presence_of_element_located((By.CLASS_NAME, 'text-heading-xlarge'))
    #     wait.until(element_present)
    # except Exception as e:
    #     print("Page Load Error", e)
    #     continue
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
    name_list.append([name, link])    
    

    #Get Job and Education
    section_tags = soup.findAll('section', {'class': 'artdeco-card ember-view relative break-words pb3 mt2'}) #to get all the sections
    for section in section_tags:
        divs = section.find_all('div')
        for div in divs:
            id_tag = div.get('id')
            if id_tag == "experience":
                sectionType = "experience"
                #print(section, sectionType, link)
                updateFile(section, sectionType, link)
                break
            if id_tag == "education": 
                sectionType = "education"
                updateFile(section, sectionType, link)
                break

end = time.time() 

df_name = pd.DataFrame(name_list, columns=["Name", "LinkedInURL"])
df_exp = pd.DataFrame(exp_list, columns=["LinkedInURL", "Job Title", "Organization Name", "Employment Type", "Start Date", "End Date", "Time Period", "Location", "Location Type"])
df_edu = pd.DataFrame(edu_list, columns=["LinkedInURL", "School", "Degree", "Field of Study", "Start Date", "End Date"])
df_exp_desc = pd.DataFrame(exp_desc, columns=["LinkedInURL", "Job Description"])
df_edu_desc = pd.DataFrame(edu_desc, columns=["LinkedInURL", "Education Description"])


df_exp['Exp_ID'] = df_exp.groupby("LinkedInURL").cumcount() + 1
df_edu['Edu_ID'] = df_edu.groupby("LinkedInURL").cumcount() + 1
df_exp_desc['Exp_ID'] = df_exp_desc.groupby("LinkedInURL").cumcount() + 1
df_edu_desc['Edu_ID'] = df_edu_desc.groupby("LinkedInURL").cumcount() + 1

# Merging based on LinkedInURL and the unique identifiers
merged_exp = df_exp.merge(df_exp_desc, on=["LinkedInURL", "Exp_ID"], how="left")
merged_edu = df_edu.merge(df_edu_desc, on=["LinkedInURL", "Edu_ID"], how="left")

# Merging the dataframes with df_name
merged_df = df_name.merge(merged_exp, on="LinkedInURL", how="left") \
                   .merge(merged_edu, on="LinkedInURL", how="left")

# Drop the Exp_ID and Edu_ID columns
merged_df.drop(columns=['Exp_ID', 'Edu_ID'], inplace=True)


print("The time of execution of above program is :",(end-start), "seconds")           
print(".................Done Scraping!.................")
browser.quit()

