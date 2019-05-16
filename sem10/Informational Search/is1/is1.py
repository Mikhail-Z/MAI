import logging
import wikipediaapi
from datetime import datetime
from urllib.parse import urlparse, unquote
import os

logging.basicConfig(filename="sample.log", level=logging.INFO, filemode='w')


def get_articles_list(category_members, level=0, max_level=2):
    articles_list = []
    for c in category_members.values():
        if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
            articles_list += get_articles_list(c.categorymembers, level=level + 1, max_level=max_level)
        if c.ns == wikipediaapi.Namespace.MAIN:
            articles_list.append(c.title)
    return articles_list


if __name__ == "__main__":
    wiki_wiki = wikipediaapi.Wikipedia(
        language='ru',
        extract_format=wikipediaapi.ExtractFormat.WIKI
    )
    cat = wiki_wiki.page("Категория:Техника")

    logging.info("Downloading articles...")
    t1 = datetime.now()

    articles = get_articles_list(cat.categorymembers)

    article_counter = 0

    logging.info("Texts downloading...")
    for name in articles:
        article_counter += 1
        try:
            page = wiki_wiki.page(name)
            filename = os.path.basename(urlparse(unquote(page.fullurl)).path)
            with open("../Статьи/Техника/" + filename + '.txt', "w+", encoding='utf8') as f:
                text = page.text
                print(article_counter)
                f.write(text)
        except Exception as exc:
            logging.info(exc)
            continue

    logging.info("Timet spending: %s" % str(datetime.now() - t1))

    cat = wiki_wiki.page("Категория:Информация")

    logging.info("Downloading articles...")
    t1 = datetime.now()

    articles = get_articles_list(cat.categorymembers)

    article_counter = 0

    logging.info("Texts downloading...")
    for name in articles:
        try:
            page = wiki_wiki.page(name)
            filename = os.path.basename(urlparse(unquote(page.fullurl)).path)
            with open("../Статьи/Информация/" + filename + '.txt', "w+", encoding='utf8') as f:
                text = page.text
                f.write(text)
        except Exception as exc:
            logging.info(exc)
            continue

    logging.info("Timet spending: %s" % str(datetime.now() - t1))
