import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

# Initialize lists to store data
titles, companies, locations, links, dates, job_skills, exp_needed, salary = [], [], [], [], [], [], [], []

# Loop through pages
for i in range(5):  # Adjust the range for more pages
    # Fetch the page content
    res = requests.get(f'https://wuzzuf.net/search/jobs/?a=hpb&q=machine%20learning&start={i}')
    soup = BeautifulSoup(res.text, 'lxml')

    # Extract data from the main search page
    job_titles = soup.find_all('h2', {'class': 'css-m604qf'})
    company_names = soup.find_all('a', {'class': 'css-17s97q8'})
    job_locations = soup.find_all('span', {'class': 'css-5wys0k'})
    job_links = soup.find_all('h2', {'class': 'css-m604qf'})
    job_dates = soup.find_all('div', {'class': re.compile(r'css-do6t5g|css-4c4ojb')})

    # Iterate over the jobs on the page
    for j in range(len(job_titles)):
        try:
            # Append the data for each job
            titles.append(job_titles[j].text.strip())
            companies.append(company_names[j].text.strip())
            locations.append(job_locations[j].text.strip())
            links.append(job_links[j].a['href'])
            dates.append(job_dates[j].text.strip())

            # Use Selenium to get additional details from the job link
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service)
            driver.get(job_links[j].a['href'])

            time.sleep(5)  # Wait for the page to load
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')

            # Extract job skills
            skills = soup.find_all('span', {'class': 'css-6to1q'})
            skill_list = [skill.get_text(strip=True) for skill in skills]
            job_skills.append(skill_list)

            # Extract job details (experience needed and salary)
            job_details = soup.find_all('span', {'class': 'css-4xky9y'})
            exp_needed.append(job_details[0].text.strip() if len(job_details) > 0 else "Not specified")
            salary.append(job_details[3].text.strip() if len(job_details) > 3 else "Not specified")

            # Close the browser
            driver.quit()
        except Exception as e:
            print(f"Error processing job {j} on page {i}: {e}")
            # Ensure all lists are aligned even in case of errors
            job_skills.append("Error fetching skills")
            exp_needed.append("Error fetching experience")
            salary.append("Error fetching salary")
            continue

# Save data to a DataFrame
df = pd.DataFrame({
    'title': titles,
    'company': companies,
    'location': locations,
    'link': links,
    'date': dates,
    'skills': job_skills,
    'experience_needed': exp_needed,
    'salary': salary
})

# Export to CSV
df.to_csv('jobs.csv', index=False)

print('Done')
