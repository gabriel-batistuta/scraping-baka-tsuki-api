import baka_tsuki

if __name__ == '__main__':
    soup = baka_tsuki.get_soup()
    list_novels_by_language = baka_tsuki.get_links_light_novels_by_language(soup)