import baka_tsuki
import time

category = 'https://www.baka-tsuki.org/project/index.php?title=Category:Light_novel'

if __name__ == '__main__':
    start_time = time.time()

    soup = baka_tsuki.get_soup(category)
    list_novels_by_language = baka_tsuki.get_links_light_novels_by_language(soup=soup)
    baka_tsuki.get_list_novels(list_novels_by_language=list_novels_by_language)
    
    print("--- %s seconds ---" % (time.time() - start_time))