from bs4 import BeautifulSoup

'''

---> '-' <---

'''

def get_links_light_novels_by_language(soup:BeautifulSoup):

    def get_list_content(soup:BeautifulSoup):

        divs_content = soup.find_all('div', attrs={'class':'mw-content-ltr'})
        div_links = divs_content[1]
        links_novels_by_language = div_links.find_all('a')

        return links_novels_by_language

    def parse_language_in_string(language:str):

        language = language.strip()
        language = language.replace('Light novel ','')
        language = language.replace('(', '')
        language = language.replace(')','')

        return language

    def create_list_novels_by_language(links_novels_by_language:list[BeautifulSoup]):

        list_novels_by_language = []

        for tag_a in links_novels_by_language:
            link = tag_a['href']
            language = parse_language_in_string(tag_a.text)

            list_novels_by_language.append(
                {
                    'language':language,
                    'link':link
                }
            )

        return list_novels_by_language

    links_novels_by_language = get_list_content(soup)
    list_novels_by_language = create_list_novels_by_language(links_novels_by_language)

    return list_novels_by_language