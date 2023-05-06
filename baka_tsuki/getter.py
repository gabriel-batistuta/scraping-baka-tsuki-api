import requests
from bs4 import BeautifulSoup

def get_soup():
    
    baka = 'https://www.baka-tsuki.org/project/index.php?title=Category:Light_novel'

    response = requests.get(baka)
    if response.content: 
        content = response.content
    else:
        raise Exception("Sorry, bad request")
    
    soup = BeautifulSoup(content, 'html.parser')

    return soup