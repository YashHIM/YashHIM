import requests
from bs4 import BeautifulSoup
import pandas as pd

#Providing Headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'https://www.google.com/',
    'DNT': '1',
}

#Make dictionary for storing data
Data = {'Agency': [], 'Location':[], 'Opening': [], 'Closing': []}
Table_titles = Data.keys()

#Give URL
url = 'https://www.bidnetdirect.com/solicitations/open-bids'

try:
    #Create connection
    page = requests.get(url, headers=headers)

    #Extract relevent data using BeautifulSoup
    soup = BeautifulSoup(page.text, 'html.parser')

    Table_elements = soup.find('table', class_='simpleSolResultsTable mets-table')

    df = pd.DataFrame(columns = Table_titles)

    #Finding and storing AGENCY NAME
    Agency_element = soup.find_all('span', class_='rowTitle')
    for element in Agency_element:
        Data['Agency'].append(element.text)

    #Finding and storing AGENCY LOCATION
    Location_element = Table_elements.find_all('span',class_='location')
    for x in Location_element:
        Data['Location'].append(x.text)

    #Finding AGENCIE'S OPENING AND CLOSING DATES
    OC_element = Table_elements.find_all('span', class_='dateValue')
    Opening_Closing = {'elements':[]}
    for x in OC_element:
        Opening_Closing['elements'].append(x.text)

    #Storing AGENCIE'S OPENING DATES
    Opening_element = Opening_Closing['elements'][::2]
    for element in Opening_element:
        Data['Opening'].append(element)

    #Storing AGENCIE'S CLOSING DATES
    Closing_element = Opening_Closing['elements'][1::2]
    for element in Closing_element:
        Data['Closing'].append(element)

    # Converting scraped data to Pandas DataFrame
    df = pd.DataFrame.from_dict(Data)

    # Storing the DataFrame in a structured format
    df.to_excel("SampleDatabase.xlsx", index=False)

except Exception as e:
    print(f"Error: {e}")