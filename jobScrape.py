# importing modules
import requests
from bs4 import BeautifulSoup
import pandas as pd


# function to access a page given a number and extracting the data
def extract(page):
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"}
    url = f"https://www.simplyhired.com/search?q=python&l=Houston%2C+TX&pn={page}&job=hWU1DVDIFACfIAUVaFlp4DHFSFe4He6H8G9YSk-33J7voXUdccCbMQ"
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

# function to access the job listing's title, company, and other important details
def transform(soup): 

    # Finds jobs in page
    divs = soup.find_all('div', class_ = 'SerpJob-jobCard')

    # iterates through every job and extracts data
    for job in divs:
        title = job.find('a').text.strip()
        company = job.find('span', class_ = 'JobPosting-labelWithIcon jobposting-company').text.strip()

        # Used try/except statements here due to not being able to extract certain text data
        try:
            salary = job.find('div', class_ = 'jobposting-salary SerpJob-salary').text
        except:
            salary = job.find('div', class_ = 'SerpJob-metaInfoLeft').text

        try:
            rating = job.find('span', class_ = 'CompanyRatings-serp').text
        except:
            rating = "No rating given."
        
        summary = job.find('p', class_ = 'jobposting-snippet').text

        # dictionary containing all data
        job = { 
             'title': title,
             'company': company,
             'rating': rating,
             'summary': summary,
             'salary': salary
        }

        # dictionary data being stored in a list
        joblist.append(job)
    return

joblist = []

for i in range(0, 3):
    c = extract(1)
    transform(c)

df = pd.DataFrame(joblist)

print(df.head())

df.to_csv('jobs.csv')
