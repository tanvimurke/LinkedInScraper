# LinkedInScraper
<br>
This script uses Selenium to navigate the webpage and BeautifulSoup to scrape the data.
<br>
This script scrapes the following data:
"Name", "LinkedInURL", "Job Title", "Organization Name", "Employment Type", "Start Date", "End Date", "Time Period", "Location", "Location Type", "Job Description", "School", "Degree", "Field of Study", "Start Date", "End Date", "Education Description".
<br>
To successfully scrape LinkedIn profiles, it's essential to ensure that the scraper is logged in to your LinkedIn account. To achieve this, you'll need to input your LinkedIn account's email address and password within the Config file. I highly recommend that you activate all privacy settings to prevent other users from detecting your profile visits while utilizing the scraper. Additionally, you will be required to furnish the specific profile link that you intend to scrape. This link will serve as the target for the scraping process.
<br>
How to Run
Clone the repository
Setup Virtual environment
$ python3 -m venv env
Activate the virtual environment
$ source env/Source/activate
Install dependencies used in the code
Enter your email and Password in config file and run the scraper with links to profiles to scrape
<br>
About the performance
Upon start the module will open a headless browser session using Chromium.
Scraping usually takes a few seconds, because the script needs to scroll through the page and expand several elements in order for all the data to appear.
LinkedIn has some usage limits in place. Please respect those and use their options to increase limits. 
This script won't work if there is any change in the UI code of LinkedIn
This script will face connection issues if you run the script many times. There is a possibility that LinkedIn can detect scrapers.
