import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

'''
progress_bar = tqdm(total=len(list_novels_by_language),colour='blue',desc=f'updating {language}')
'''

def get_soup(link):

    response = requests.get(link)
    if response.content: 
        content = response.content
    else:
        raise Exception(f"Sorry, bad request status_code: {0}".format(response))

    soup = BeautifulSoup(content, 'html.parser')

    return soup

def get_list_novels(list_novels_by_language:list[dict]):
    domain = 'https://www.baka-tsuki.org'

    def parse_title_novel(title:str, language:str):
        title = title.replace('~','')
        title = title.replace(language,'')
        title = title.strip()

        return title

    def get_novel_details(link_novel:str):
        soup = get_soup(link_novel)
        content = soup.find('div', attrs={'id':'mw-content-text'})

        def get_main_cover(link_novel:str):
            options = Options()
            options.add_argument("--headless")
            browser = webdriver.Firefox(options=options)
            browser.get(link_novel)
            html = browser.page_source
            browser.close()

            # html = link_novel
            
            soup = BeautifulSoup(html, 'html.parser')
            image = soup.find('img', attrs={'class':'thumbimage'})
            try:
                image = image['src']
                image = domain+str(image)
            except:
                image = 'Unknown'
            return image

        def get_synopsis(content:BeautifulSoup):
            synopsis = content.find_all(lambda tag: tag.name == 'p' 
                                        and len(list(tag.contents)) == 1 
                                        and tag.string != None)
            desc = ''
            for i in synopsis:
                desc += i.text.encode('utf-8')
            synopsis = desc.strip()
            
            return synopsis

        def get_ilustrations(chapters_links:list[str]):
            img_list = []

            def is_ilustration_page(page:str):
                if domain in page:
                    soup = get_soup(page)
                    try:
                        galery = soup.find('ul', attrs={'class':'gallery mw-gallery-traditional'})
                        if galery is not None:
                            return True
                    except:
                        return False 
                return False

            for chapter in chapters_links:
                if is_ilustration_page(chapter):
                    galery = soup.find('ul', attrs={'class':'gallery mw-gallery-traditional'})
                    imgs = galery.find_all('img')
                    for img in imgs:
                        img_list.append(img['src'])

            return img_list


        def get_novel_chapthers(content:BeautifulSoup):
            chapters = []

            def is_valid_chapter(tag):
                links = tag.find_all('a')
                for link in links:
                    if domain not in link['href']:
                        return False
                return True

            dl_list = content.find_all('dl')
            dl_list = list(filter(is_valid_chapter, dl_list))
            
            for tag in dl_list:
                links = tag.find_all('a')
                for link in links:
                    chapters.append(link['href'])
            
            return chapters

        synopsis = get_synopsis(content)
        cover = get_main_cover(link_novel)
        chapters_links = get_novel_chapthers(content)
        image_list = get_ilustrations(chapters_links)

        return synopsis, cover, chapters_links, image_list

    def get_list_of_novels_by_language(soup:BeautifulSoup, language:str):

        list_novels_by_language = []
        div_links_novels = soup.find('div', attrs={'class':'mw-content-ltr'})
        divs_novels_by_letter = div_links_novels.find_all('div', attrs={'class':'mw-category-group'})

        for div in divs_novels_by_letter:
            category_letter = div.find('h3').text.strip().lower()
            list_novels_by_category = div.find_all('a')
            for tag_a in list_novels_by_category:
                link = domain+tag_a['href']
                title = tag_a.text
                title = parse_title_novel(title, language)
                synopsis, cover, chapters_links, image_list = get_novel_details(link)
                list_novels_by_language.append(
                    {
                        'category_letter':category_letter,
                        'title':title,
                        'link':link,
                        'synopsis':synopsis,
                        'cover':cover,
                        'chapters_links':chapters_links,
                        'image_list':image_list
                    }
                )
                
        return list_novels_by_language

    def get_novels_with_language(list_novels_by_language:list[dict]):

        list_novels = []
        for dct_novel in list_novels_by_language:
            language = dct_novel['language']
            link = dct_novel['link']

            link_novels_by_language = domain + link
            soup = get_soup(link_novels_by_language)
            list_novels_by_language = get_list_of_novels_by_language(soup, language)
            list_novels.append({
                'language':language,
                'list_novels_by_language':list_novels_by_language
                })
        
        return list_novels
    
    def create_json_novel(list_novels:list[dict]):
        with open('./.novels.json', 'w') as file:
            json.dump(list_novels, file, indent=4, )

    list_novels = get_novels_with_language(list_novels_by_language)
    create_json_novel(list_novels)
